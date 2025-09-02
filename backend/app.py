from flask import Flask, jsonify
from flask_cors import CORS
from config import db
from flask_jwt_extended import JWTManager
from routes.user_routes import user_routes
from config import JWT_SECRET

app = Flask(__name__)
CORS(app)  # allow frontend requests

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Rental Platform Backend is running!"})


app.config["JWT_SECRET_KEY"] = JWT_SECRET
jwt = JWTManager(app)

# Register routes
app.register_blueprint(user_routes, url_prefix="/api/user")

if __name__ == "__main__":
    app.run(debug=True)

