import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS


from db import db
from routes.todos import todos_bp
from dotenv import load_dotenv
load_dotenv()


# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_NAME = os.getenv("DB_NAME")


app = Flask(__name__)

CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": "http://localhost:3000"}}
)
# flask run --debug - старт с перезапуском при измененнии
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://igor:123@localhost/flasktodo' - URL example (dbname - flasktodo; user - igor; dbPassword - 123)
#app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
Migrate(app, db)

app.register_blueprint(todos_bp)