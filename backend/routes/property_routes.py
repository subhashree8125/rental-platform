import os
from flask import Blueprint, request, jsonify, session
from ..db import db
from ..models.properties import Property

property_routes = Blueprint('property_routes', __name__)

# Note: The GET/POST /api/properties endpoints are defined on the blueprint
# within the main app factory to avoid duplication here.

# ------------------------------
# Fetch current user's properties
# ------------------------------
@property_routes.route("/api/myproperties", methods=["GET"])
def my_properties():
    print("[DEBUG] my_properties route is registered and accessed")
    user = session.get("user")
    if not user:
        print("[DEBUG] Session Error: User not logged in")
        return jsonify({"error": "Unauthorized"}), 401

    try:
        print("[DEBUG] Session User:", user)
        props = Property.query.filter_by(owner_id=user["user_id"]).order_by(Property.property_id.desc()).all()
        print("[DEBUG] Properties fetched for user:", props)
        props_list = [{
            "property_id": p.property_id,
            "full_name": p.full_name,
            "address": p.address,
            "city": p.city,
            "area": p.area,
            "district": p.district,
            "property_type": p.property_type,
            "house_type": p.house_type,
            "rent_price": str(p.rent_price),
            "car_parking": p.car_parking,
            "pets": p.pets,
            "furnishing": p.furnishing,
            "facing": p.facing,
            "status": p.status,
            "description": p.description,
            "images": [img for img in p.images.split(",") if img]
        } for p in props]
        return jsonify({"success": True, "properties": props_list})
    except Exception as e:
        print("[DEBUG] Get Properties Error:", e)
        return jsonify({"error": "Failed to fetch properties"}), 500

# ------------------------------
# Update property status (Available/Unavailable)
# ------------------------------
@property_routes.route("/api/property/<int:property_id>/status", methods=["PUT"])
def update_property_status(property_id):
    user = session.get("user")
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        prop = Property.query.get(property_id)
        if not prop or prop.owner_id != user["user_id"]:
            return jsonify({"error": "Property not found or unauthorized"}), 404

        new_status = request.json.get("status")
        if new_status not in ["Available", "Unavailable"]:
            return jsonify({"error": "Invalid status"}), 400

        prop.status = new_status
        db.session.commit()
        return jsonify({"success": True, "message": f"Property status updated to {new_status}"})
    except Exception as e:
        print("Update Property Status Error:", e)
        return jsonify({"error": "Failed to update status"}), 500

# ------------------------------
# Update property details (owner only)
# ------------------------------
@property_routes.route("/api/property/<int:property_id>", methods=["PUT"])
def update_property(property_id):
    user = session.get("user")
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        prop = Property.query.get(property_id)
        if not prop or prop.owner_id != user["user_id"]:
            return jsonify({"error": "Property not found or unauthorized"}), 404

        data = request.get_json() or {}

        # Allow updating a subset of fields
        updatable_fields = [
            "address", "city", "area", "district", "property_type", "house_type", "rent_price",
            "car_parking", "pets", "facing", "furnishing", "description", "full_name", "mobile_number"
        ]
        for field in updatable_fields:
            if field in data and data[field] is not None:
                setattr(prop, field, data[field])

        db.session.commit()
        return jsonify({"success": True, "message": "Property updated successfully"})
    except Exception as e:
        print("Update Property Error:", e)
        return jsonify({"error": "Failed to update property"}), 500

# ------------------------------
# Contact owner (returns phone when logged-in)
# ------------------------------
@property_routes.route("/api/property/<int:property_id>/contact", methods=["GET"])
def contact_owner(property_id):
    user = session.get("user")
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        prop = Property.query.get(property_id)
        if not prop:
            return jsonify({"error": "Property not found"}), 404

        return jsonify({"success": True, "mobile_number": prop.mobile_number})
    except Exception as e:
        print("Contact Owner Error:", e)
        return jsonify({"error": "Failed to fetch contact"}), 500

# ------------------------------
# Delete a property
# ------------------------------
@property_routes.route("/api/property/<int:property_id>", methods=["DELETE"])
def delete_property(property_id):
    user = session.get("user")
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        prop = Property.query.get(property_id)
        if not prop or prop.owner_id != user["user_id"]:
            return jsonify({"error": "Property not found or unauthorized"}), 404

        db.session.delete(prop)
        db.session.commit()
        return jsonify({"success": True, "message": "Property deleted successfully"})
    except Exception as e:
        print("Delete Property Error:", e)
        return jsonify({"error": "Failed to delete property"}), 500
