"""
Role-Based Access Control Decorators for Agent 50 Supreme
"""

from functools import wraps
from flask import session, jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt
import functools

def get_current_user():
    """
    Unified function to get current user from either session or JWT
    Returns: user_id or None
    """
    # Try JWT first (for API requests)
    try:
        verify_jwt_in_request(optional=True)
        jwt_data = get_jwt()
        if jwt_data:
            return jwt_data.get('sub')  # user_id from JWT
    except:
        pass
    
    # Fall back to session (for web requests)
    return session.get('user_id')

def get_current_user_role():
    """Get current user's role from either session or JWT"""
    # Try JWT
    try:
        verify_jwt_in_request(optional=True)
        jwt_data = get_jwt()
        if jwt_data:
            return jwt_data.get('role')
    except:
        pass
    
    # Fall back to session or database lookup
    from extensions import db
    from models import User
    
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return user.role if user else None
    
    return None

def jwt_or_session_required(f):
    """
    Decorator that works with both JWT (API) and session (web)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_current_user()
        
        if not user_id:
            # Check if this is an API request
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Authentication required'}), 401
            else:
                from flask import redirect, url_for
                return redirect(url_for('main_bp.login'))
        
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    """
    Decorator to require specific role
    Usage: @role_required('admin')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # First check authentication
            user_id = get_current_user()
            if not user_id:
                if request.is_json or request.path.startswith('/api/'):
                    return jsonify({'error': 'Authentication required'}), 401
                else:
                    from flask import redirect, url_for
                    return redirect(url_for('main_bp.login'))
            
            # Check role
            user_role = get_current_user_role()
            if user_role != required_role:
                if request.is_json or request.path.startswith('/api/'):
                    return jsonify({'error': 'Insufficient permissions'}), 403
                else:
                    from flask import redirect, url_for, flash
                    flash('You do not have permission to access this page.', 'danger')
                    return redirect(url_for('main_bp.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Convenience decorators
def admin_required(f):
    return role_required('admin')(f)

def driver_required(f):
    return role_required('driver')(f)

def restaurant_required(f):
    return role_required('restaurant')(f)

def customer_required(f):
    return role_required('customer')(f)

def login_required(f):
    """
    Compatibility decorator - uses JWT for API, session for web
    """
    return jwt_or_session_required(f)