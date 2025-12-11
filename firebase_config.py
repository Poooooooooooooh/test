import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import json

# Initialize Firebase Admin SDK
# Try multiple methods to find credentials
cred = None

# Method 1: Check for environment variable with JSON content (for cloud hosting)
firebase_credentials_json = os.environ.get('FIREBASE_CREDENTIALS_JSON')
if firebase_credentials_json:
    try:
        cred_dict = json.loads(firebase_credentials_json)
        cred = credentials.Certificate(cred_dict)
        print("Using Firebase credentials from FIREBASE_CREDENTIALS_JSON environment variable")
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error parsing FIREBASE_CREDENTIALS_JSON: {e}")

# Method 2: Check for file path in environment variable
if not cred:
    service_account_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if service_account_path and os.path.exists(service_account_path):
        try:
            cred = credentials.Certificate(service_account_path)
            print(f"Using Firebase credentials from file: {service_account_path}")
        except Exception as e:
            print(f"Error loading credentials from {service_account_path}: {e}")

# Method 3: Try default location in project directory
if not cred:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_path = os.path.join(current_dir, "serviceAccountKey.json")
    if os.path.exists(default_path):
        try:
            cred = credentials.Certificate(default_path)
            print(f"Using Firebase credentials from default location: {default_path}")
        except Exception as e:
            print(f"Error loading credentials from {default_path}: {e}")

# Method 4: Try Google Cloud default credentials (for Cloud Run, App Engine, etc.)
if not cred:
    try:
        # This will use the default credentials from the environment
        # Works on Google Cloud Run, App Engine, Compute Engine, etc.
        cred = credentials.ApplicationDefault()
        print("Using Google Cloud default application credentials")
    except Exception as e:
        print(f"Error using default credentials: {e}")

# Initialize the app (only if not already initialized)
if cred:
    try:
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully")
    except ValueError:
        # App already initialized
        print("Firebase Admin SDK already initialized")
else:
    raise Exception("Could not initialize Firebase Admin SDK. Please provide credentials via FIREBASE_CREDENTIALS_JSON environment variable, GOOGLE_APPLICATION_CREDENTIALS file path, or serviceAccountKey.json file.")

db = firestore.client()
