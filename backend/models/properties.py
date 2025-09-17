from ..db import db
from datetime import datetime

class Property(db.Model):
    __tablename__ = "properties"
    __table_args__ = {'extend_existing': True}  # In case the table already exists
    property_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    full_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    house_type = db.Column(db.String(50), nullable=False)
    rent_price = db.Column(db.Numeric(10, 2), nullable=False)
    car_parking = db.Column(db.Enum('Any', 'Available', 'NotAvailable'), nullable=False)
    pets = db.Column(db.Enum('Any', 'Allowed', 'Strictly Not Allowed'), nullable=False)
    facing = db.Column(db.String(50), nullable=False)
    furnishing = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    images = db.Column(db.Text)  # Can store comma-separated filenames
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    # Relationship to User
    owner = db.relationship("Users", back_populates="properties")

    def __repr__(self):
        return f"<Property {self.property_id} - {self.full_name}>"
