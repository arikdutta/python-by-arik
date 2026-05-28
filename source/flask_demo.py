import time
import threading
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return "REST API Running"


@app.route("/products")
def products():
    data = {
        "products": [
            {"id": 1, "name": "Laptop",     "price": 999.99},
            {"id": 2, "name": "Phone",      "price": 699.99},
            {"id": 3, "name": "Headphones", "price": 149.99},
        ]
    }
    return jsonify(data)


@app.route("/add", methods=["POST"])
def add_product():
    data = request.json
    product = data.get("product")
    return jsonify({"message": f"{product} added successfully"})


# ── Demo caller ───────────────────────────────────────────────────────────────

BASE_URL = "http://localhost:5000"

def demo_calls():
    time.sleep(1)  # wait for Flask to start

    print("\n── GET / ───────────────────────────────────────")
    resp = requests.get(f"{BASE_URL}/")
    print(resp.text)

    print("\n── GET /products ───────────────────────────────")
    resp = requests.get(f"{BASE_URL}/products")
    data = resp.json()
    print(f"{'ID':<5} {'Name':<15} {'Price':>8}")
    print("-" * 30)
    for p in data["products"]:
        print(f"{p['id']:<5} {p['name']:<15} ${p['price']:>7.2f}")

    print("\n── POST /add ───────────────────────────────────")
    resp = requests.post(f"{BASE_URL}/add", json={"product": "Tablet"})
    print(resp.json()["message"])

    print("\nDemo complete. Press Ctrl+C to stop the server.")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    server_thread = threading.Thread(
        target=lambda: app.run(port=5000, debug=False, use_reloader=False),
        daemon=True,
    )
    server_thread.start()

    demo_calls()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down.")
