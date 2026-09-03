from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # get_jwt_identity() will now work because @jwt_required() ran first
            identity = get_jwt_identity() 
            
            # Extract user role depending on how your JWT token is structured
            user_role = identity.get("role") if isinstance(identity, dict) else None
            
            # If user_role isn't in token, fetch from DB or check identity
            if user_role and user_role not in allowed_roles:
                return jsonify({"error": "Unauthorized access for this role"}), 403
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator    
