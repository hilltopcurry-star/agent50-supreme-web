import jwt
import datetime
from flask import current_app
from extensions import bcrypt

# --- CONFIGURATION ---
# Agar config file mein key na mile to yeh fallback use karega (Development ke liye)
DEFAULT_SECRET_KEY = "agent50_supreme_secret_key_change_in_prod"
TOKEN_EXPIRATION_HOURS = 24  # Token 24 ghante baad expire hoga

def hash_password(password):
    """
    Password ko strong hash mein convert karta hai.
    Input: Plain password (e.g., 'password123')
    Output: Encrypted Hash string
    """
    # Generate hash and decode to utf-8 string for storage
    return bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(password_hash, password):
    """
    Check karta hai ke user ka password sahi hai ya nahi.
    Input: Database ka hash, User ka diya hua password
    Output: True / False
    """
    return bcrypt.check_password_hash(password_hash, password)

def generate_token(user_id):
    """
    User ke liye ek secure JWT Token generate karta hai.
    Includes: User ID, Issued Time (iat), Expiration Time (exp)
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRATION_HOURS),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        
        # Secret Key App Config se uthayega
        secret_key = current_app.config.get('SECRET_KEY', DEFAULT_SECRET_KEY)
        
        # Token Encode karein
        token = jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )
        return token
    except Exception as e:
        print(f"[AUTH ERROR] Token generation failed: {str(e)}")
        return None

def verify_token(token):
    """
    Aane wale token ko verify karta hai.
    Returns: User ID (agar valid hai) ya Error Message
    """
    try:
        secret_key = current_app.config.get('SECRET_KEY', DEFAULT_SECRET_KEY)
        
        # Token Decode karein
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=['HS256']
        )
        return payload['sub'] # Valid User ID return karega

    except jwt.ExpiredSignatureError:
        return "Token Expired" # Token purana ho gaya
    except jwt.InvalidTokenError:
        return "Invalid Token" # Token ghalat ya fake hai
    except Exception as e:
        return f"Auth Error: {str(e)}"