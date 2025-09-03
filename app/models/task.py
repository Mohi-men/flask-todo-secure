from datetime import datetime
from ..extensions import db

class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ New fields
    deadline = db.Column(db.DateTime, nullable=True)   # optional deadline
    priority = db.Column(db.String(10), nullable=False, default="medium")  
    # values: "high", "medium", "low"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))