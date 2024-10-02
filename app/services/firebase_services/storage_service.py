from firebase_admin import storage, credentials, initialize_app
from firebase_admin import credentials

cred = credentials.Certificate("app/pulzion-app-firebase-adminsdk-s7c7d-e8362f219f.json")
initialize_app(cred, {
    'storageBucket': 'pulzion-app.appspot.com'
})

def store_to_firebasebase(img_buffer, file_name):
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_file(img_buffer, content_type='image/png')
    blob.make_public()

    public_url = blob.public_url
    print(f"File uploaded successfully: {public_url}")