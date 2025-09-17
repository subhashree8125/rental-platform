from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from ..db import db

property_bp = Blueprint("properties", __name__)

# Example Property model
class Property(db.Model):
    __tablename__ = "properties"

    property_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    address = db.Column(db.Text, nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    rent_price = db.Column(db.Numeric(10,2), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Property {self.property_id}>"

# Dummy routes
@property_bp.route("/list", methods=["GET"])
def list_properties():
    return jsonify({"message": "List of properties (dummy)"})

@property_bp.route("/add", methods=["POST"])
def add_property():
    data = request.json
    return jsonify({"message": "Property added (dummy)", "data": data})
