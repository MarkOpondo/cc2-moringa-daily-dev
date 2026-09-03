from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Profile

profiles_bp = Blueprint("profiles", __name__)


@profiles_bp.get("/me")
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())

    profile = Profile.query.filter_by(UserID=user_id).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify({
        "profile_id": profile.ProfileID,
        "user_id": profile.UserID,
        "bio": profile.Bio,
        "interests": profile.Interests,
        "profile_image": profile.ProfileImage
    }), 200


@profiles_bp.put("/me")
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())

    profile = Profile.query.filter_by(UserID=user_id).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    profile.Bio = data.get("bio", profile.Bio)
    profile.Interests = data.get("interests", profile.Interests)
    profile.ProfileImage = data.get(
        "profile_image",
        profile.ProfileImage
    )

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully."
    }), 200
