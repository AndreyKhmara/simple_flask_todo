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
    print(data)

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_todo = Todo(
        title=data["title"],
        text=data["text"],
    )

    db.session.add(new_todo)
    db.session.commit()

    return jsonify(new_todo.to_dict()), 201

