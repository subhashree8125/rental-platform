# backend/routes/property_routes.py
from flask import Blueprint, request, jsonify, session
from backend.db import db
from backend.models.properties import Property
from backend.models.users import Users
from backend.config import Config
import os

property_routes = Blueprint("property_routes", __name__)

@property_routes.route("/api/properties", methods=["POST"])
def create_property():
    if "user" not in session:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

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
    images = request.files.getlist("images")

    filenames = []
    for image in images:
        if image:
            filename = image.filename
            save_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            image.save(save_path)
            filenames.append(filename)

    # Find the logged-in user
    user = Users.query.filter_by(email=session["user"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_property = Property(
        owner=user,
        full_name=full_name,
        mobile_number=mobile_number,
        address=address,
        district = district,
        property_type=property_type,
        house_type=house_type,
        rent_price=rent_price,
        car_parking=car_parking,
        pets=pets,
        facing=facing,
        furnishing=furnishing,
        description=description,
        images=",".join(filenames)
    )

    db.session.add(new_property)
    db.session.commit()

    return jsonify({"success": True, "message": "Property posted successfully!"}), 201
