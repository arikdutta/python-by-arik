"""
Webhook receiver & validation in Python
========================================
Two complete examples: Flask and FastAPI
Covers: signature verification, idempotency, background tasks, error handling
"""

# ─────────────────────────────────────────────
# FLASK EXAMPLE
# pip install flask
# ─────────────────────────────────────────────

import hashlib
import hmac
import json
import time
import logging
from functools import wraps

from flask import Flask, request, jsonify, abort

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEBHOOK_SECRET = "your-webhook-secret"   # store in env var in production
TIMESTAMP_TOLERANCE = 300                # 5 minutes — reject replayed requests


# ── Signature verification helper ──────────────────────────────────────────

def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """
    Verify an HMAC-SHA256 webhook signature.
    Many providers (Stripe, GitHub, Shopify) use this pattern.
    """
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    # Use compare_digest to prevent timing attacks
    return hmac.compare_digest(f"sha256={expected}", signature)


def verify_timestamp(timestamp_str: str, tolerance: int = TIMESTAMP_TOLERANCE) -> bool:
    """Reject requests older than `tolerance` seconds (replay attack prevention)."""
    try:
        ts = int(timestamp_str)
        return abs(time.time() - ts) < tolerance
    except (ValueError, TypeError):
        return False


# ── Decorator: require valid signature ─────────────────────────────────────

def require_webhook_signature(secret: str):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            signature = request.headers.get("X-Signature-256", "")
            timestamp  = request.headers.get("X-Timestamp", "")

            if not signature:
                logger.warning("Webhook rejected: missing signature")
                abort(401, "Missing signature")

            if timestamp and not verify_timestamp(timestamp):
                logger.warning("Webhook rejected: stale timestamp")
                abort(401, "Timestamp out of tolerance")

            if not verify_signature(request.data, signature, secret):
                logger.warning("Webhook rejected: invalid signature")
                abort(403, "Invalid signature")

            return f(*args, **kwargs)
        return wrapper
    return decorator


# ── Idempotency store (swap for Redis/DB in production) ────────────────────

_seen_event_ids: set[str] = set()

def is_duplicate(event_id: str) -> bool:
    if event_id in _seen_event_ids:
        return True
    _seen_event_ids.add(event_id)
    return False


# ── Event router ───────────────────────────────────────────────────────────

def handle_payment_succeeded(data: dict):
    amount = data.get("amount")
    currency = data.get("currency", "usd").upper()
    logger.info(f"Payment succeeded: {amount} {currency}")
    # → update database, send receipt email, etc.

def handle_payment_failed(data: dict):
    reason = data.get("failure_reason", "unknown")
    logger.warning(f"Payment failed: {reason}")
    # → notify customer, retry logic, etc.

def handle_subscription_cancelled(data: dict):
    user_id = data.get("user_id")
    logger.info(f"Subscription cancelled for user {user_id}")

EVENT_HANDLERS = {
    "payment.succeeded":      handle_payment_succeeded,
    "payment.failed":         handle_payment_failed,
    "subscription.cancelled": handle_subscription_cancelled,
}


# ── Flask webhook endpoint ─────────────────────────────────────────────────

@app.route("/webhooks/stripe", methods=["POST"])
@require_webhook_signature(WEBHOOK_SECRET)
def stripe_webhook():
    try:
        payload = request.get_json(force=True)
    except Exception:
        abort(400, "Invalid JSON")

    event_id   = payload.get("id")
    event_type = payload.get("type")
    event_data = payload.get("data", {})

    # Idempotency check
    if event_id and is_duplicate(event_id):
        logger.info(f"Duplicate event ignored: {event_id}")
        return jsonify({"status": "duplicate"}), 200   # always 200 to stop retries

    # Route to handler
    handler = EVENT_HANDLERS.get(event_type)
    if handler:
        try:
            handler(event_data)
        except Exception as e:
            logger.error(f"Handler error for {event_type}: {e}")
            return jsonify({"status": "error"}), 500   # provider will retry
    else:
        logger.info(f"Unhandled event type: {event_type}")

    return jsonify({"status": "ok"}), 200   # respond fast; do heavy work async


# ── GitHub-style webhook (uses X-Hub-Signature-256) ────────────────────────

@app.route("/webhooks/github", methods=["POST"])
def github_webhook():
    sig_header = request.headers.get("X-Hub-Signature-256", "")
    if not sig_header.startswith("sha256="):
        abort(403, "Missing or malformed signature")

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        request.data,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(sig_header[7:], expected):
        abort(403, "Signature mismatch")

    event = request.headers.get("X-GitHub-Event", "unknown")
    payload = request.get_json()

    if event == "push":
        branch = payload.get("ref", "").replace("refs/heads/", "")
        pusher = payload.get("pusher", {}).get("name")
        logger.info(f"Push to {branch} by {pusher}")

    elif event == "pull_request":
        action = payload.get("action")
        pr     = payload.get("pull_request", {}).get("title")
        logger.info(f"PR '{pr}' → {action}")

    return jsonify({"status": "ok"}), 200


# ─────────────────────────────────────────────────────────────────────────────
# FASTAPI EXAMPLE
# pip install fastapi uvicorn
# Run: uvicorn webhooks_python:fastapi_app --reload
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import FastAPI, Request, Header, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional
import asyncio

fastapi_app = FastAPI(title="Webhook Receiver")


# ── Async signature verification ───────────────────────────────────────────

async def verify_webhook(
    body: bytes,
    x_signature_256: str,
    x_timestamp: Optional[str],
    secret: str = WEBHOOK_SECRET,
) -> None:
    """Raise HTTPException if the request is invalid."""
    if not x_signature_256:
        raise HTTPException(status_code=401, detail="Missing signature header")

    if x_timestamp and not verify_timestamp(x_timestamp):
        raise HTTPException(status_code=401, detail="Timestamp out of tolerance")

    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(f"sha256={expected}", x_signature_256):
        raise HTTPException(status_code=403, detail="Invalid signature")


# ── Background task: do heavy work after responding ────────────────────────

async def process_event(event_type: str, data: dict):
    """Run in background so webhook responds immediately (<5 s)."""
    await asyncio.sleep(0)           # yield to event loop
    handler = EVENT_HANDLERS.get(event_type)
    if handler:
        handler(data)                # call sync handler from async context
    logger.info(f"Background processing done for {event_type}")


# ── FastAPI webhook endpoint ────────────────────────────────────────────────

@fastapi_app.post("/webhooks/stripe")
async def fastapi_stripe_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_signature_256: str = Header(default=""),
    x_timestamp: Optional[str] = Header(default=None),
):
    body = await request.body()
    await verify_webhook(body, x_signature_256, x_timestamp)

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    event_id   = payload.get("id")
    event_type = payload.get("type")
    event_data = payload.get("data", {})

    if event_id and is_duplicate(event_id):
        return JSONResponse({"status": "duplicate"}, status_code=200)

    # Enqueue background task — respond to provider immediately
    background_tasks.add_task(process_event, event_type, event_data)

    return JSONResponse({"status": "accepted"}, status_code=202)


# ── Shopify-style HMAC (base64, not hex) ───────────────────────────────────

import base64

@fastapi_app.post("/webhooks/shopify")
async def shopify_webhook(
    request: Request,
    x_shopify_hmac_sha256: str = Header(default=""),
):
    body = await request.body()

    expected = base64.b64encode(
        hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).digest()
    ).decode()

    if not hmac.compare_digest(expected, x_shopify_hmac_sha256):
        raise HTTPException(status_code=403, detail="Invalid Shopify signature")

    payload = json.loads(body)
    topic   = request.headers.get("X-Shopify-Topic", "unknown")
    logger.info(f"Shopify event: {topic}")

    return JSONResponse({"status": "ok"})


# ─────────────────────────────────────────────────────────────────────────────
# LOCAL TESTING — simulate an incoming webhook
# ─────────────────────────────────────────────────────────────────────────────

def simulate_webhook(url: str = "http://localhost:5000/webhooks/stripe"):
    """Send a test webhook to your local server."""
    import requests as req

    payload = json.dumps({
        "id":   "evt_test_001",
        "type": "payment.succeeded",
        "data": {"amount": 4200, "currency": "eur"},
    }).encode()

    ts  = str(int(time.time()))
    sig = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()

    resp = req.post(
        url,
        data=payload,
        headers={
            "Content-Type":    "application/json",
            "X-Signature-256": sig,
            "X-Timestamp":     ts,
        },
    )
    print(f"Status: {resp.status_code} — {resp.json()}")


# ─────────────────────────────────────────────────────────────────────────────
# Run Flask:   python webhooks_python.py
# Run FastAPI: uvicorn webhooks_python:fastapi_app --port 8000 --reload
# Test:        python webhooks_python.py --test
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        simulate_webhook()
    else:
        app.run(debug=True, port=5000)
