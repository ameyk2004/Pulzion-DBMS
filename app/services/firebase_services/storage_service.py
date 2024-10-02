from firebase_admin import storage

from app.services.firebase_services.firebase_config import initialize_firebase

initialize_firebase()

def upload_image_to_storage(file_path, file_name):
    
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_path)
        blob.make_public()
        public_url = blob.public_url

        print(f"File uploaded successfully: {public_url}")
        return public_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
