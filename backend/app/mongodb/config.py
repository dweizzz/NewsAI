from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv
import os
from typing import Generator

# Load environment variables
load_dotenv()

# Get MongoDB connection string from environment variable
# MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_URI = "mongodb+srv://news:newsai@cluster0.z9tce3q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = os.getenv("MONGODB_DB_NAME", "newsai")

# Create MongoDB client with improved connection settings
client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=30000,  # Increase timeout to 30 seconds
    connectTimeoutMS=30000,
    socketTimeoutMS=30000,
    retryWrites=True,
    maxPoolSize=50,
    waitQueueTimeoutMS=30000
)

# Database instance
db = client[DB_NAME]

# Function to test connection
def test_connection():
    try:
        # The ping command is lightweight and doesn't require auth
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return True
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return False

# Dependency to get DB for FastAPI
def get_db() -> Generator[Database, None, None]:
    try:
        yield db
    finally:
        # No need to close connection here as it will be handled on app shutdown
        pass