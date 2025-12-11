import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import json

# Try to get Firebase credentials from environment variable first (for production/Render)
# If not found, fall back to serviceAccountKey.json file (for local development)
firebase_credentials = None

# Check for environment variable (used in Render/production)
if os.getenv('FIREBASE_CREDENTIALS'):
    try:
        # Parse JSON from environment variable
        firebase_credentials = json.loads(os.getenv('FIREBASE_CREDENTIALS'))
    except json.JSONDecodeError:
        print("Warning: FIREBASE_CREDENTIALS environment variable contains invalid JSON")
        firebase_credentials = None

# If no environment variable, try to load from file
if firebase_credentials is None:
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    service_account_path = os.path.join(current_dir, "serviceAccountKey.json")
    
    if os.path.exists(service_account_path):
        # Use file path directly
        cred = credentials.Certificate(service_account_path)
    else:
        # File not found - try environment variable path
        env_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if env_path and os.path.exists(env_path):
            cred = credentials.Certificate(env_path)
        else:
            raise FileNotFoundError(
                f"Firebase credentials not found. Please either:\n"
                f"1. Set FIREBASE_CREDENTIALS environment variable with JSON content, or\n"
                f"2. Place serviceAccountKey.json in the project root, or\n"
                f"3. Set GOOGLE_APPLICATION_CREDENTIALS to the file path"
            )
else:
    # Use credentials from environment variable
    cred = credentials.Certificate(firebase_credentials)

# Initialize Firebase Admin (only if not already initialized)
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    # App already initialized, which is fine
    pass

db = firestore.client()
