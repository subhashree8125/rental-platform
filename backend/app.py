import os
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, Blueprint, current_app
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

from backend.db import db
from backend.config import Config

# Models
from backend.models.users import Users
from backend.models.properties import Property

# ------------------------
# Blueprints
# ------------------------
property_routes = Blueprint("property_routes", __name__)

# ------------------------
# Property APIs
# ------------------------
@property_routes.route("/api/properties", methods=["GET"])
def get_properties():
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
    return jsonify(props_list)


@property_routes.route("/api/properties", methods=["POST"])
def create_property():
    user_data = session.get("user")
    if not user_data or not isinstance(user_data, dict):
        return jsonify({"error": "Unauthorized"}), 401

    form_data = request.form.to_dict()

    car_parking = form_data.get("car_parking")
    pets = form_data.get("pets")
    if car_parking not in ("Any", "Available", "NotAvailable"):
        return jsonify({"error": "Invalid car_parking value"}), 400
    if pets not in ("Any", "Allowed", "Strictly Not Allowed"):
        return jsonify({"error": "Invalid pets value"}), 400

    files = request.files.getlist("images")
    image_filenames = []
    for f in files:
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            image_filenames.append(filename)

    try:
        new_property = Property(
            owner_id=user_data.get("user_id"),
            full_name=form_data.get("full_name"),
            mobile_number=form_data.get("mobile_number"),
            address=form_data.get("address"),
            district=form_data.get("district"),
            property_type=form_data.get("property_type"),
            house_type=form_data.get("house_type"),
            rent_price=form_data.get("rent_price"),
            car_parking=car_parking,
            pets=pets,
            facing=form_data.get("facing"),
            furnishing=form_data.get("furnishing"),
            description=form_data.get("description"),
            images=",".join(image_filenames),
            status="Available"
        )

        db.session.add(new_property)
        db.session.commit()

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

        return jsonify(props_list), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@property_routes.route("/api/properties/<int:property_id>/status", methods=["PATCH"])
def update_property_status(property_id):
    user_data = session.get("user")
    if not user_data:
        return jsonify({"error": "Unauthorized"}), 401

    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"error": "Property not found"}), 404

    if prop.owner_id != user_data.get("user_id"):
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    new_status = data.get("status")
    if new_status not in ["Available", "Unavailable"]:
        return jsonify({"error": "Invalid status"}), 400

    prop.status = new_status
    db.session.commit()
    return jsonify({"success": True, "status": prop.status})


# ------------------------
# App factory
# ------------------------
def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static/uploads")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    CORS(app, supports_credentials=True)

    with app.app_context():
        db.create_all()

    # ------------------------
    # HTML Pages
    # ------------------------
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/signup", methods=["GET", "POST"])
    def signup_page():
        return render_template("signup.html")

    @app.route("/login", methods=["GET", "POST"])
    def login_page():
        return render_template("login.html")

    @app.route("/explore")
    def explore_page():
        return render_template("explore.html")

    @app.route("/postproperty", methods=["GET", "POST"])
    def postproperty_page():
        if "user" not in session:
            flash("Please login to post a property.", "warning")
            return redirect(url_for("login_page"))
        return render_template("postproperty.html")

    @app.route("/profile")
    def profile_page():
        if "user" not in session:
            flash("Please login to view your profile.", "warning")
            return redirect(url_for("login_page"))
        return render_template("profile.html", user=session["user"])

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        flash("Logged out successfully.", "success")
        return redirect(url_for("index"))

    # ------------------------
    # Auth APIs
    # ------------------------
    @app.route("/auth/signup", methods=["POST"])
    def signup_api():
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data received"}), 400

        fullname = data.get("full_name")
        email = data.get("email")
        mobile = data.get("mobile_number")
        password = data.get("password")  # ✅ expect plain password from frontend

        if Users.query.filter_by(email=email).first():
            return jsonify({"success": False, "message": "Email already exists"}), 400

        new_user = Users(full_name=fullname, email=email, mobile_number=mobile)
        new_user.set_password(password)  # ✅ hashes internally
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"success": True, "message": "Signup successful"})

    @app.route("/auth/login", methods=["POST"])
    def login():
        try:
            data = request.get_json(force=True)
            if not data:
                return jsonify({"success": False, "message": "No data received"}), 400

            identifier = data.get("identifier")
            password = data.get("password")  # ✅ expect plain password from frontend

            if not identifier or not password:
                return jsonify({"success": False, "message": "Email/Phone and Password required"}), 400

            user = Users.query.filter(
                (Users.email == identifier) | (Users.mobile_number == identifier)
            ).first()

            if not user:
                return jsonify({"success": False, "message": "User not found"}), 401

            if not user.password_hash:  # ✅ fix here
                return jsonify({"success": False, "message": "Password not set for this user"}), 500

            if check_password_hash(user.password_hash, password):  # ✅ fix here
                session["user"] = {
                    "user_id": user.user_id,
                    "full_name": user.full_name,
                    "email": user.email
                }
                return jsonify({"success": True, "user": session["user"]})

            return jsonify({"success": False, "message": "Invalid credentials"}), 401

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

    @app.route("/api/session")
    def check_session():
        if "user" in session and isinstance(session["user"], dict):
            return jsonify({"loggedIn": True, "user": session["user"]})
        return jsonify({"loggedIn": False}), 401

    # ------------------------
    # Profile APIs
    # ------------------------
    @app.route("/api/profile", methods=["GET"])
    def get_profile():
        if "user" not in session:
            return jsonify({"error": "Unauthorized"}), 401

        user_id = session["user"]["user_id"]
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "user_id": user.user_id,
            "full_name": user.full_name,
            "email": user.email,
            "mobile_number": user.mobile_number
        })

    @app.route("/api/profile", methods=["PUT"])
    def update_profile():
        if "user" not in session:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json()
        user_id = session["user"]["user_id"]
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        if "full_name" in data:
            user.full_name = data["full_name"]
        if "mobile_number" in data:
            user.mobile_number = data["mobile_number"]
        if "password" in data and data["password"]:
            user.set_password(data["password"])  # ✅ update with hash

        db.session.commit()
        session["user"]["full_name"] = user.full_name
        session["user"]["mobile_number"] = user.mobile_number

        return jsonify({"success": True, "message": "Profile updated successfully"})

    @app.route("/api/profile", methods=["DELETE"])
    def delete_profile():
        if "user" not in session:
            return jsonify({"error": "Unauthorized"}), 401

        user_id = session["user"]["user_id"]
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        session.pop("user", None)

        return jsonify({"success": True, "message": "Account deleted successfully"})

    # ------------------------
    # Register Blueprint
    # ------------------------
    app.register_blueprint(property_routes)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=4000)
