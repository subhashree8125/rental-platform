import os
import json
from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.utils import secure_filename
from db import db
from .models.property import Property  # Use proper model class name

property_routes = Blueprint('property_routes', __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@property_routes.route("/api/properties", methods=["POST"])
def post_property():
    # Check user session
    user = session.get("user")
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # --- Extract form data ---
        full_name = request.form.get("full_name")
        mobile_number = request.form.get("mobile_number")
        address = request.form.get("address")
        district = request.form.get("district")
        property_type = request.form.get("property_type")
        house_type = request.form.get("house_type")
        rent_price = request.form.get("rent_price")
        car_parking = request.form.get("car_parking")
        pets = request.form.get("pets")
        facing = request.form.get("facing")
        furnishing = request.form.get("furnishing")
        description = request.form.get("description")

        # --- Handle uploaded images ---
        images_files = request.files.getlist("images")
        saved_images = []
        for file in images_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                file.save(save_path)
                saved_images.append(filename)

        # --- Create new property ---
        new_property = Property(
            owner_id=user["user_id"],
            full_name=full_name,
            mobile_number=mobile_number,  # Ensure column exists in DB
            address=address,
            district=district,
            property_type=property_type,
            house_type=house_type,
            rent_price=rent_price,
            car_parking=car_parking,
            pets=pets,
            facing=facing,
            furnishing=furnishing,
            description=description,
            images=",".join(saved_images),
            status="Available"
        )

        db.session.add(new_property)
        db.session.commit()

        # --- Return updated properties for Explore ---
        all_props = Property.query.filter_by(status="Available").order_by(Property.property_id.desc()).all()
        props_list = [{
            "property_id": p.property_id,
            "full_name": p.full_name,
            "address": p.address,
            "district": p.district,
            "property_type": p.property_type,
            "house_type": p.house_type,
            "rent_price": str(p.rent_price),
            "car_parking": p.car_parking,
            "pets": p.pets,
            "facing": p.facing,
            "furnishing": p.furnishing,
            "description": p.description,
            "images": p.images.split(",") if p.images else [],
            "status": p.status
        } for p in all_props]

        return jsonify({"success": True, "properties": props_list})

    except Exception as e:
        current_app.logger.error(f"Post Property Error: {e}")
        return jsonify({"error": "Failed to post property"}), 500
