from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Profile, User
from app.serializers import serialize_user


profiles_bp = Blueprint("profiles", __name__)


def _profile_payload(user, profile):
    return {
        "user": serialize_user(user),
        "bio": profile.Bio,
        "interests": profile.Interests,
        "skills": profile.Skills,
        "githubUrl": profile.GithubURL,
        "profileImage": profile.ProfileImage,
        "createdAt": profile.CreatedAt.isoformat() if profile.CreatedAt else None,
        "updatedAt": profile.UpdatedAt.isoformat() if profile.UpdatedAt else None,
    }


def _get_profile():
    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return None, None
    profile = Profile.query.filter_by(UserID=user.UserID).first()
    if not profile:
        profile = Profile(UserID=user.UserID)
        db.session.add(profile)
        db.session.flush()
    return user, profile


@profiles_bp.get("/me")
@jwt_required()
def get_profile():
    user, profile = _get_profile()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(_profile_payload(user, profile)), 200


@profiles_bp.put("/me")
@jwt_required()
def update_profile():
    user, profile = _get_profile()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True) or {}
    profile.Bio = data.get("bio", profile.Bio)
    profile.Interests = data.get("interests", profile.Interests)
    profile.Skills = data.get("skills", profile.Skills)
    profile.GithubURL = data.get("githubUrl", data.get("github_url", profile.GithubURL))
    profile.ProfileImage = data.get(
        "profileImage", data.get("profile_image", profile.ProfileImage)
    )
    db.session.commit()
    return jsonify(_profile_payload(user, profile)), 200
