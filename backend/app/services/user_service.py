import logging
from pymongo.database import Database
from bson import ObjectId
from fastapi import HTTPException
from ..utils.security import get_password_hash, verify_password
from ..mongodb.models import UserModel

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_db_connection(db: Database):
    """Check if the database connection is working."""
    try:
        # Ping the database
        db.command('ping')
        return True
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return False

def ensure_indexes(db: Database):
    """Ensure necessary indexes exist for user collections."""
    try:
        # Create indexes for email and username to improve lookup performance
        db[UserModel.collection_name].create_index("email", unique=True)
        db[UserModel.collection_name].create_index("username", unique=True)
        logger.info("Indexes created/verified successfully")
        return True
    except Exception as e:
        logger.error(f"Index creation error: {str(e)}")
        return False

def get_user_by_email(db: Database, email: str):
    """Get a user by email."""
    logger.info(f"Looking up user with email: {email}")
    try:
        return db[UserModel.collection_name].find_one({"email": email})
    except Exception as e:
        logger.error(f"Error finding user by email: {str(e)}")
        raise

def get_user_by_username(db: Database, username: str):
    """Get a user by username."""
    logger.info(f"Looking up user with username: {username}")
    try:
        return db[UserModel.collection_name].find_one({"username": username})
    except Exception as e:
        logger.error(f"Error finding user by username: {str(e)}")
        raise

def get_user_by_id(db: Database, user_id: str):
    """Get a user by id."""
    logger.info(f"Looking up user with ID: {user_id}")
    try:
        return db[UserModel.collection_name].find_one({"_id": ObjectId(user_id)})
    except Exception as e:
        logger.error(f"Error finding user by ID: {str(e)}")
        raise

def create_user(db: Database, email: str, username: str, password: str):
    """Create a new user."""
    logger.info(f"Attempting to create user with email: {email}")

    # First check DB connection
    if not check_db_connection(db):
        logger.error("Database connection failed during user creation")
        raise HTTPException(status_code=503, detail="Database connection error")

    # Ensure indexes exist
    ensure_indexes(db)

    try:
        # Check if email already exists
        logger.info(f"Checking if email {email} already exists")
        existing_email = get_user_by_email(db, email)
        if existing_email:
            logger.warning(f"Email {email} already registered")
            raise HTTPException(status_code=400, detail="Email already registered")

        # Check if username already exists
        logger.info(f"Checking if username {username} already exists")
        existing_username = get_user_by_username(db, username)
        if existing_username:
            logger.warning(f"Username {username} already taken")
            raise HTTPException(status_code=400, detail="Username already taken")

        # Create new user
        logger.info("Creating password hash")
        hashed_password = get_password_hash(password)

        logger.info("Preparing user document")
        user_data = UserModel.to_document(
            email=email,
            username=username,
            hashed_password=hashed_password
        )

        logger.info("Inserting user into database")
        result = db[UserModel.collection_name].insert_one(user_data)
        user_data["_id"] = result.inserted_id
        logger.info(f"User created successfully with ID: {result.inserted_id}")

        return user_data
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"User creation failed: {str(e)}")

def authenticate_user(db: Database, email: str, password: str):
    """Authenticate a user."""
    logger.info(f"Attempting to authenticate user with email: {email}")

    try:
        user = get_user_by_email(db, email)
        if not user:
            logger.warning(f"No user found with email: {email}")
            return None

        logger.info("Verifying password")
        if not verify_password(password, user["hashed_password"]):
            logger.warning("Password verification failed")
            return None

        logger.info("User authenticated successfully")
        return user
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return None