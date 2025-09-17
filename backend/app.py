# backend/app.py
from flask import Blueprint, Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_cors import CORS

# Relative imports
from .db import db
from .config import Config

# Models
from backend.models.users import Users
from .models.properties import Property

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    # Enable CORS for frontend dev server
    CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

    # Initialize DB
    db.init_app(app)
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

    @app.route("/postproperty", methods=["GET", "POST"], endpoint="postproperty_page")
    def postproperty():
        if "user" not in session:
            flash("Please login to post a property.", "warning")
            return redirect(url_for("login_page"))

        if request.method == "POST":
            full_name = request.form.get("full_name")
            mobile_number = request.form.get("mobile_number")
            address = request.form.get("address")
            property_type = request.form.get("property_type")
            house_type = request.form.get("house_type")
            rent_price = request.form.get("rent_price")
            car_parking = request.form.get("car_parking")
            pets = request.form.get("pets")
            facing = request.form.get("facing")
            furnishing = request.form.get("furnishing")
            description = request.form.get("description")
            images = request.files.getlist("images")

            image_filenames = []
            for image in images:
                if image:
                    filename = image.filename
                    image.save(f"{Config.UPLOAD_FOLDER}/{filename}")
                    image_filenames.append(filename)

            user = Users.query.filter_by(email=session["user"]).first()
            new_property = Property(
                owner=user,
                full_name=full_name,
                mobile_number=mobile_number,
                address=address,
                property_type=property_type,
                house_type=house_type,
                rent_price=rent_price,
                car_parking=car_parking,
                pets=pets,
                facing=facing,
                furnishing=furnishing,
                description=description,
                images=",".join(image_filenames),
            )

            db.session.add(new_property)
            db.session.commit()
            flash("Property posted successfully!", "success")
            return redirect(url_for("explore_page"))

        return render_template("postproperty.html")

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        flash("You have been logged out.", "info")
        return redirect(url_for("index"))

    @app.route("/ping")
    def ping():
        return {"status": "ok", "message": "BrokLink backend is running 🚀"}

    # ------------------------
    # API Routes (for JS fetch)
    # ------------------------
    
    @app.route("/auth/signup", methods=["POST"])
    def signup():
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data received"}), 400

        fullname = data.get("full_name")
        email = data.get("email")
        mobile = data.get("mobile_number")
        password = data.get("password")

        if Users.query.filter_by(email=email).first():
            return jsonify({"success": False, "message": "Email already exists"}), 400

        new_user = Users(
            full_name=fullname,
            email=email,
            mobile_number=mobile
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"success": True, "message": "Signup successful"})
            
    @app.route("/auth/login", methods=["POST"])
    def login_api():
        data = request.get_json()
        identifier = data.get("identifier")
        password = data.get("password")

        if "@" in identifier:
            user = Users.query.filter_by(email=identifier).first()
        else:
            user = Users.query.filter_by(mobile_number=identifier).first()

        if user and user.check_password(password):
            session["user"] = user.email
            return jsonify({"message": "Login successful!", "user": {"fullname": user.full_name, "email": user.email}}), 200
        else:
            return jsonify({"message": "Invalid credentials, try again."}), 401

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)








