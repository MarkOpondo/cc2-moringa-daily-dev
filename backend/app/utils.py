from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models import User, normalized_role


def current_user():
    """Return the user represented by the current JWT, or None."""
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return None
    return db.session.get(User, user_id)


def role_required(*allowed_roles):
    """Require the current user to have one of the supplied roles."""
    allowed = {role.lower() for role in allowed_roles}

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user:
                return jsonify({"error": "User not found"}), 404
            if not user.IsActive:
                return jsonify({"error": "Active user account required"}), 403

            role = normalized_role(user.Role)
            if role not in allowed:
                return jsonify({"error": "Forbidden. Insufficient permissions."}), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator
