import firebase_admin
from firebase_admin import credentials

SERVICE_ACCOUNT_KEY_PATH = "pulzion-app.appspot.com"

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'pulzion-app.appspot.com'  # Replace with your Firebase project ID
        })

