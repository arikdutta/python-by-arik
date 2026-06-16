from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# In-memory store (resets on restart)
todos = []
next_id = 1


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)


@app.route("/api/todos", methods=["POST"])
def create_todo():
    global next_id
    data = request.get_json()
    if not data or not data.get("text", "").strip():
        return jsonify({"error": "text is required"}), 400
    todo = {"id": next_id, "text": data["text"].strip(), "done": False}
    next_id += 1
    todos.append(todo)
    return jsonify(todo), 201


@app.route("/api/todos/<int:todo_id>", methods=["PATCH"])
def toggle_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        return jsonify({"error": "not found"}), 404
    todo["done"] = not todo["done"]
    return jsonify(todo)


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    before = len(todos)
    todos = [t for t in todos if t["id"] != todo_id]
    if len(todos) == before:
        return jsonify({"error": "not found"}), 404
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
