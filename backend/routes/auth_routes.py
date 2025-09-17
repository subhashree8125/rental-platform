from flask import Blueprint, request, jsonify
from models import db, Users

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    # Extract payload
    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    mobile_number = data.get("mobile_number")

    # Basic validation
    if not all([full_name, email, password, mobile_number]):
        return jsonify({"error": "All fields are required"}), 400

    # Check if email exists
    if Users.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    try:
        # Create user
        user = Users(
            full_name=full_name,
            email=email,
            mobile_number=mobile_number
        )
        user.set_password(password)  # hash password

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "Signup successful",
            "user_id": user.user_id
        }), 201

    except Exception as e:
        print("Signup error:", e)  # ✅ see exact error in console
        db.session.rollback()
        return jsonify({"error": "Signup failed"}), 500
