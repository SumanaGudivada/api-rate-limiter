from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://gudivadasumana_db_user:<db_password>@cluster0.kincsgz.mongodb.net/?appName=Cluster0"

client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000  # prevents long hangs
)

db = client["rate_limiter_db"]
collection = db["logs"]