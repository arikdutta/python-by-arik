from flask import Flask, jsonify
 
app = Flask(__name__)
 
@app.route("/")
 
def home():
 
    return "REST API Running"
 
 
@app.route("/products")
 
def products():
 
    data = {
 
        "products": [
            "Laptop",
            "Phone",
            "Headphones"
        ]
    }
 
    return jsonify(data)
 
 
app.run(debug=True)