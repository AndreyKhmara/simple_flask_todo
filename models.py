from datetime import datetime
from db import db


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), nullable=False)
    isCompleted = db.Column(
        db.Boolean(),
        nullable=False,
        default=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "isCompleted": self.isCompleted,
            "created_at": self.created_at.isoformat()
        }

# Для перренаката ->
# меняем модель,
# накатываем новую миграцию: flask db migrate -m "replace title with isCompleted"
# применить: flask db upgrade
