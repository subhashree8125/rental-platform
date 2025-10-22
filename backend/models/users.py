from ..db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    __tablename__ = "users"   # ✅ better convention (all lowercase)

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=True)  # ✅ nullable for phone-auth users
    mobile_number = db.Column(db.String(15), nullable=False)
    profile_image = db.Column(db.String(200), nullable=True, default=None)  # ✅ profile photo path
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to properties (if you have Property model)
    properties = db.relationship(
        "Property",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    # ✅ set password (store hash only)
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    # ✅ verify password
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User id={self.user_id}, email={self.email}, profile_image={self.profile_image}>"
