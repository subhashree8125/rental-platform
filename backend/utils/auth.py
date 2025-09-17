from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from db import db

# Define Blueprint
auth_bp = Blueprint("auth", __name__)

# Example User model
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    mobile_number = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User {self.user_id} - {self.email}>"

# Example route
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    return jsonify({"message": "Register route working!", "data": data})
