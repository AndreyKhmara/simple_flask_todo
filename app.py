import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": "http://localhost:3000"}}
)
# flask run --debug - старт с перезапуском при измененнии
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://igor:123@localhost/flasktodo' - URL example (dbname - flasktodo; user - igor; dbPassword - 123)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)
from models import Todo


@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_todo = Todo(
        text=data["text"],
        isCompleted=data["isCompleted"],
    )

    db.session.add(new_todo)
    db.session.commit()

    return jsonify(new_todo.to_dict()), 201


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if not todo:
        jsonify({'error': f'Not found ID {todo_id}'}), 404

    try:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({
            "message": "Product deleted successfully",
            "deleted_id": todo_id
        }), 200

    except Exception as e:

        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


@app.route("/todos/<int:todo_id>", methods=["PATCH"])
def toggle_todo(todo_id):
    payload = request.get_json(silent=True)

    if not payload:
        return jsonify({"error": "Request body is required"}), 400

    is_completed = payload.get("isCompleted")

    try:
        todo = db.session.get(Todo, todo_id)

        if not todo:
            return jsonify({"error": "Todo not found"})

        todo.isCompleted = is_completed
        db.session.commit()
        return jsonify(todo.to_dict()), 200

    except Exception as e:

        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500


@app.route("/todos/update/<int:todo_id>", methods=["PATCH"])
def update_todo(todo_id):
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Request body is required"}), 400

    new_text = payload.get("text")

    try:
        todo = db.session.get(Todo, todo_id)

        if not todo:
            return jsonify({"error": "Todo not found"})

        todo.text = new_text
        db.session.commit()
        return jsonify(todo.to_dict()), 200

    except Exception as e:

        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500
