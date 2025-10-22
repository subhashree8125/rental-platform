import os
import json
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, Blueprint, current_app
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

# Ensure imports work whether run as module (python -m backend.app)
# or as script inside backend directory (python app.py)
try:
    from backend.db import db
    from backend.config import Config
    # Models
    from backend.models.users import Users
    from backend.models.properties import Property
    # Blueprints
    from backend.routes.property_routes import property_routes
except ModuleNotFoundError:
    import sys
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from backend.db import db
    from backend.config import Config
    # Models
    from backend.models.users import Users
    from backend.models.properties import Property
    # Blueprints
    from backend.routes.property_routes import property_routes

# ------------------------
# Blueprints
# ------------------------

# ------------------------
# Property APIs
# ------------------------
@property_routes.route("/api/properties", methods=["GET"])
def get_properties():
    query = Property.query.filter_by(status="Available")

    # Parse filters from query string
    filters_param = request.args.get("filters")
    if filters_param:
        try:
            filters = json.loads(filters_param)

            # Cities
            if filters.get("cities"):
                query = query.filter(Property.city.in_(filters["cities"]))

            # Districts
            if filters.get("districts"):
                query = query.filter(Property.district.in_(filters["districts"]))

            # Areas (using the dedicated area column)
            if filters.get("areas"):
                query = query.filter(Property.area.in_(filters["areas"]))

            # Property Types
            if filters.get("propertyTypes"):
                query = query.filter(Property.property_type.in_(filters["propertyTypes"]))

            # BHK
            if filters.get("bhk"):
                query = query.filter(Property.house_type.in_(filters["bhk"]))

            # Budget
            if filters.get("minBudget") and filters.get("maxBudget"):
                query = query.filter(
                    Property.rent_price.between(filters["minBudget"], filters["maxBudget"])
                )

            # Car Parking
            if filters.get("carParking"):
                query = query.filter(Property.car_parking == filters["carParking"])

            # Pets
            if filters.get("pets"):
                query = query.filter(Property.pets == filters["pets"])

            # Facing (multiple allowed)
            if filters.get("facing"):
                query = query.filter(Property.facing.in_(filters["facing"]))

            # Furnishing (multiple allowed)
            if filters.get("furnishing"):
                query = query.filter(Property.furnishing.in_(filters["furnishing"]))

        except Exception as e:
            print("Filter parsing error:", e)

    # Final query
    all_props = query.order_by(Property.property_id.desc()).all()

    # Convert to dict list
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
            city=form_data.get("city"),
            area=form_data.get("area"),
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
            "city": p.city,
            "area": p.area,
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


## Status update route is defined in blueprint file to avoid duplication


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
        try:
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "message": "No data received"}), 400

            fullname = data.get("full_name")
            email = data.get("email")
            mobile = data.get("mobile_number")
            password = data.get("password")  # ✅ expect plain password from frontend

            # Validation
            if not all([fullname, email, mobile, password]):
                return jsonify({"success": False, "error": "All fields are required"}), 400

            if Users.query.filter_by(email=email).first():
                return jsonify({"success": False, "error": "Email already exists"}), 400

            new_user = Users(full_name=fullname, email=email, mobile_number=mobile)
            new_user.set_password(password)  # ✅ hashes internally
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"success": True, "message": "Signup successful"})
        except Exception as e:
            db.session.rollback()
            print(f"Signup error: {str(e)}")  # Log to console
            return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500

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
                    "email": user.email,
                    "mobile_number": user.mobile_number
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
        user = db.session.get(Users, user_id)
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
        user = db.session.get(Users, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Email uniqueness check
        if "email" in data and data["email"] != user.email:
            if Users.query.filter_by(email=data["email"]).first():
                return jsonify({"error": "Email already exists"}), 400

        # Update user fields
        user.full_name = data.get("full_name", user.full_name)
        user.email = data.get("email", user.email)
        user.mobile_number = data.get("mobile_number", user.mobile_number)
        if data.get("password"):
            user.set_password(data["password"])

        db.session.commit()

        # Update session with new data
        session["user"] = {
            "user_id": user.user_id,
            "full_name": user.full_name,
            "email": user.email,
            "mobile_number": user.mobile_number
        }

        return jsonify({"success": True, "message": "Profile updated successfully"})

    @app.route("/api/profile", methods=["DELETE"])
    def delete_profile():
        if "user" not in session:
            return jsonify({"error": "Unauthorized"}), 401

        user_id = session["user"]["user_id"]
        user = db.session.get(Users, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        session.pop("user", None)

        return jsonify({"success": True, "message": "Account deleted successfully"})

    # ------------------------
    # Register Blueprint
    # ------------------------

    print("[DEBUG] Registering property_routes blueprint")
    app.register_blueprint(property_routes)
    print("[DEBUG] property_routes blueprint registered successfully")

    # profile_routes blueprint removed; contact owner handled in property routes

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5002, debug=True)
