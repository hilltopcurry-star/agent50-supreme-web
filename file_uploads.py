import os
from werkzeug.utils import secure_filename
from flask import current_app

# Allowed file types (Images aur Code files)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf', 'py', 'html', 'css', 'js'}

def allowed_file(filename):
    """Check karta hai ke file ki extension valid hai ya nahi"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_file_upload(file):
    """
    File ko 'static/uploads' folder mein save karta hai.
    Returns: Filename agar success ho, warna None
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Upload folder ka path banayen (Main folder > static > uploads)
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        
        # Agar folder nahi hai to khud bana dein
        os.makedirs(upload_folder, exist_ok=True)
        
        # File save karein
        file.save(os.path.join(upload_folder, filename))
        return filename
    return None

def get_uploaded_files():
    """Upload folder mein majood saari files ki list deta hai"""
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    if not os.path.exists(upload_folder):
        return []
    return os.listdir(upload_folder)