from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.extensions import db
from app.models import Profile

profiles_bp=Blueprint("profiles", __name__)

@profiles_bp.get("/<int:user_id>")
@jwt_required()
def get_profile(user_id):
    profile = Profile.query.filter_by(UserID=user_id).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify({
        "profile_id": profile.ProfileID,
        "user_id": profile.UserID,
        "bio": profile.Bio,
        "interests": profile.Interests,
        "profile_image": profile.ProfileImage
    }),200

@profiles_bp.put("/<int:user_id>")
@jwt_required()
def update_profile(user_id):
    # Users can edit their own profile\
    current_user_id=int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"Error": "You can only edit your own profile."}),403

    profile = Profile.query.filter_by(UserID=user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404 

    data = request.get_json()
    
    if not data:
        return jsonify({
            "error": "No input data provided"
        }),400

    profile.Bio=data.get("bio", profile.Bio)
    profile.Interests= data.get("interests", profile.Interests)
    profile.ProfileImage=data.get("profile_image", profile.ProfileImage)
    db.session.commit()
    
    return jsonify({"message": "Profile updated successfully."}), 200
    
