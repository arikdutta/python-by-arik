"""
Flask API + Webhook Demo
========================
Runs a Flask server in a background thread, then fires a webhook
call at it from the same process — no external tools needed.

Run:  python flask-webhook-demo.py
"""

import json
import time
import threading
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ── API endpoints ────────────────────────────────────────────────────────────

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "service": "demo-api"})


@app.route("/api/items", methods=["GET"])
def list_items():
    items = [
        {"id": 1, "name": "Apple",  "price": 0.99},
        {"id": 2, "name": "Banana", "price": 0.49},
        {"id": 3, "name": "Cherry", "price": 2.99},
    ]
    return jsonify({"items": items, "count": len(items)})


@app.route("/api/items", methods=["POST"])
def create_item():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400
    new_item = {"id": 4, "name": data["name"], "price": data.get("price", 0.0)}
    return jsonify({"created": new_item}), 201


# ── Webhook endpoint ─────────────────────────────────────────────────────────

@app.route("/webhook/events", methods=["POST"])
def receive_webhook():
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "empty payload"}), 400

    event_type = payload.get("event")
    data       = payload.get("data", {})

    print(f"\n[webhook] Received event: {event_type!r}")
    print(f"[webhook] Payload: {json.dumps(data, indent=2)}")

    # Route by event type
    if event_type == "order.created":
        print(f"[webhook] New order #{data.get('order_id')} for ${data.get('total'):.2f}")
    elif event_type == "user.signup":
        print(f"[webhook] New user: {data.get('email')}")
    else:
        print(f"[webhook] Unhandled event type: {event_type}")

    return jsonify({"received": True, "event": event_type}), 200


# ── Webhook sender (caller) ──────────────────────────────────────────────────

BASE_URL = "http://localhost:5050"

def send_webhook(event_type: str, data: dict):
    payload = {"event": event_type, "data": data}
    resp = requests.post(
        f"{BASE_URL}/webhook/events",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    print(f"[sender]  POST /webhook/events → {resp.status_code} {resp.json()}")
    return resp


def demo_api_calls():
    time.sleep(1)  # wait for Flask to start

    print("\n── GET /api/status ─────────────────────────────")
    resp = requests.get(f"{BASE_URL}/api/status")
    print(resp.json())

    print("\n── GET /api/items ──────────────────────────────")
    resp = requests.get(f"{BASE_URL}/api/items")
    print(resp.json())

    print("\n── POST /api/items ─────────────────────────────")
    resp = requests.post(f"{BASE_URL}/api/items", json={"name": "Dragonfruit", "price": 3.49})
    print(resp.json())

    print("\n── Sending webhooks ────────────────────────────")
    send_webhook("order.created", {"order_id": 1001, "total": 14.97, "items": 3})
    send_webhook("user.signup",   {"email": "alice@example.com", "plan": "free"})
    send_webhook("unknown.event", {"foo": "bar"})

    print("\nDemo complete. Press Ctrl+C to stop the server.")


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Start Flask in a daemon thread so Ctrl+C stops everything
    server_thread = threading.Thread(
        target=lambda: app.run(port=5050, debug=False, use_reloader=False),
        daemon=True,
    )
    server_thread.start()

    demo_api_calls()

    # Keep main thread alive so the server stays up
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down.")
