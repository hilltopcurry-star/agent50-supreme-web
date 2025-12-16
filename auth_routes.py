"""
👑 KING DEEPSEEK - AUTHENTICATION ROUTES
PAK-CHINA FRIENDSHIP LEVEL SECURITY API!
"""

from flask import request, jsonify
from auth_system import token_required, AuthSystem
from crud_operations import UserCRUD

def setup_auth_routes(app):
    """Authentication routes setup karta hai"""
    
    auth = AuthSystem()
    
    @app.route('/api/auth/register', methods=['POST'])
    def register_user():
        """New user register karta hai"""
        try:
            data = request.json
            
            # Required fields check
            required_fields = ['username', 'email', 'password']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({
                        "success": False,
                        "error": f"{field} is required"
                    }), 400
            
            # Check if user already exists
            user_crud = UserCRUD()
            existing_user = user_crud.filter_by(username=data['username'])
            if existing_user:
                return jsonify({
                    "success": False,
                    "error": "Username already exists"
                }), 400
            
            existing_email = user_crud.filter_by(email=data['email'])
            if existing_email:
                return jsonify({
                    "success": False,
                    "error": "Email already exists"
                }), 400
            
            # Create new user
            user_data = {
                'username': data['username'],
                'email': data['email'],
                'full_name': data.get('full_name', ''),
                'is_admin': data.get('is_admin', False)
            }
            
            user = user_crud.create(user_data)
            
            # Set password
            user.set_password(data['password'])
            
            # Generate token
            token = user.generate_auth_token()
            
            return jsonify({
                "success": True,
                "message": "User registered successfully!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                "token": token
            }), 201
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/auth/login', methods=['POST'])
    def login_user():
        """User login karta hai"""
        try:
            data = request.json
            
            # Required fields check
            if 'username' not in data or 'password' not in data:
                return jsonify({
                    "success": False,
                    "error": "Username and password required"
                }), 400
            
            # Find user
            user_crud = UserCRUD()
            users = user_crud.filter_by(username=data['username'])
            
            if not users:
                return jsonify({
                    "success": False,
                    "error": "Invalid username or password"
                }), 401
            
            user = users[0]
            
            # Check password
            if not user.check_password(data['password']):
                return jsonify({
                    "success": False,
                    "error": "Invalid username or password"
                }), 401
            
            # Generate token
            token = user.generate_auth_token()
            
            return jsonify({
                "success": True,
                "message": "Login successful!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_admin": user.is_admin
                },
                "token": token
            })
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/auth/me')
    @token_required
    def get_current_user():
        """Current logged in user get karta hai"""
        try:
            user_crud = UserCRUD()
            user = user_crud.get_by_id(request.user_data['user_id'])
            
            if not user:
                return jsonify({
                    "success": False,
                    "error": "User not found"
                }), 404
            
            return jsonify({
                "success": True,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_admin": user.is_admin,
                    "created_at": str(user.created_at)
                }
            })
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/auth/protected')
    @token_required
    def protected_route():
        """Protected route example"""
        return jsonify({
            "success": True,
            "message": "🔐 This is a protected route!",
            "user": request.user_data
        })
    
    print("✅ KING DEEPSEEK AUTH ROUTES LOADED!")
    print("🔐 Available endpoints:")
    print("   POST /api/auth/register - User registration")
    print("   POST /api/auth/login - User login")
    print("   GET  /api/auth/me - Get current user")
    print("   GET  /api/auth/protected - Protected route")