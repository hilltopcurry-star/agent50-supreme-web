# computer_vision.py
import cv2
import numpy as np
import base64
from PIL import Image
import io
import os
import logging
from flask import jsonify, request

class ComputerVision:
    def __init__(self):
        self.uploads_dir = 'cv_uploads'
        os.makedirs(self.uploads_dir, exist_ok=True)
        
    def process_image(self, image_data):
        """Process uploaded image for basic computer vision"""
        try:
            # Decode base64 image
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Basic image analysis
            height, width, channels = cv_image.shape
            file_size = len(image_bytes)
            
            analysis = {
                'dimensions': {'width': width, 'height': height},
                'file_size_kb': round(file_size / 1024, 2),
                'format': image.format,
                'mode': image.mode
            }
            
            # Edge detection
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            
            # Color analysis
            colors = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            dominant_color = self.get_dominant_color(colors)
            
            analysis['edge_detection'] = True
            analysis['dominant_color_rgb'] = dominant_color
            
            # Save processed image
            processed_path = os.path.join(self.uploads_dir, 'processed_edges.jpg')
            cv2.imwrite(processed_path, edges)
            
            return {'status': 'success', 'analysis': analysis}
            
        except Exception as e:
            logging.error(f"CV Processing Error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_dominant_color(self, image, k=1):
        """Extract dominant color from image"""
        try:
            pixels = image.reshape(-1, 3)
            pixels = np.float32(pixels)
            
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
            _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            dominant_color = centers[0].astype(int)
            return dominant_color.tolist()
        except:
            return [0, 0, 0]
    
    def detect_faces(self, image_data):
        """Simple face detection"""
        try:
            # Decode image
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Load face cascade
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            result = {
                'faces_detected': len(faces),
                'face_locations': []
            }
            
            for (x, y, w, h) in faces:
                result['face_locations'].append({
                    'x': int(x), 'y': int(y), 
                    'width': int(w), 'height': int(h)
                })
            
            return {'status': 'success', 'result': result}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def image_to_ascii(self, image_data, width=100):
        """Convert image to ASCII art"""
        try:
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to grayscale
            image = image.convert('L')
            
            # Resize
            height = int(width * image.height / image.width)
            image = image.resize((width, height))
            
            # ASCII characters (from dark to light)
            ascii_chars = '@%#*+=-:. '
            
            # Convert to ASCII
            pixels = image.getdata()
            ascii_str = ''
            for i, pixel in enumerate(pixels):
                ascii_str += ascii_chars[pixel // 32]
                if (i + 1) % width == 0:
                    ascii_str += '\n'
            
            return {'status': 'success', 'ascii_art': ascii_str}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

# Flask routes integration
def setup_cv_routes(app, cv_system):
    @app.route('/api/cv/analyze', methods=['POST'])
    def analyze_image():
        data = request.get_json()
        image_data = data.get('image', '')
        result = cv_system.process_image(image_data)
        return jsonify(result)
    
    @app.route('/api/cv/faces', methods=['POST'])
    def detect_faces():
        data = request.get_json()
        image_data = data.get('image', '')
        result = cv_system.detect_faces(image_data)
        return jsonify(result)
    
    @app.route('/api/cv/ascii', methods=['POST'])
    def image_to_ascii():
        data = request.get_json()
        image_data = data.get('image', '')
        result = cv_system.image_to_ascii(image_data)
        return jsonify(result)