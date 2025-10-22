from flask import Blueprint, jsonify, session

profile_routes = Blueprint("profile_routes", __name__)

# Keep only non-duplicated, ancillary routes here. Core profile and auth
# endpoints are implemented in the main app to avoid duplication.

@profile_routes.route("/api/contact_owner", methods=["POST"])
def contact_owner():
    user = session.get("user")
    if not user:
        return jsonify({"error": "Unauthorized. Please log in to contact the owner."}), 401

    # Placeholder for contact owner logic (e.g., send email/notification)
    return jsonify({"success": True, "message": "Contact request sent successfully."})
