from flask import jsonify, Blueprint, request
from db import db
from models import Todo

todos_bp = Blueprint('todos', __name__, url_prefix='/todos')

@todos_bp.route("", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

# до рефакторинга - @todos_bp.route("/todos", methods=["POST"])
@todos_bp.route("", methods=["POST"])
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


@todos_bp.route("/<int:todo_id>", methods=["DELETE"])
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


@todos_bp.route("/<int:todo_id>", methods=["PATCH"])
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


@todos_bp.route("/update/<int:todo_id>", methods=["PATCH"])
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
