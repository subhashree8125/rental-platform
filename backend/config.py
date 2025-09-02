from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
JWT_SECRET = os.getenv("JWT_SECRET")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.get_database()  # rental_platform DB
