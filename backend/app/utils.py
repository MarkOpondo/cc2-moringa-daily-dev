from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.extensions import db

def role_required(*allowed_roles):
    """
    Decorator that checks if the cureent user's role is in the list of allowed_roles.
    Usage:
    @role_required("Admin")
    @role_required("Admin","tech_writer","user")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            from app.models import User

            user_id = get_jwt_identity()
            user = db.session.get(User, int(user_id))

            print("========== ROLE DEBUG ==========")
            print("JWT USER ID:", user_id)
            print("DATABASE USER:", user)
            print("DATABASE ROLE:", user.Role if user else None)
            print("ALLOWED ROLES:", allowed_roles)
            print("================================")

            if not user:
                return jsonify({"error": "User not found"}), 404

            if user.Role not in allowed_roles:
                return jsonify({
                    "error": "Forbidden. Insufficient permissions.",
                    "your_role": user.Role,
                    "allowed_roles": allowed_roles
                }), 403

            return fn(*args, **kwargs)

        return wrapper
    return decorator    
