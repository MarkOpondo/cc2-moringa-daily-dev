import os
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename
from app import db
from app.models import Content, Profile, User

profile_bp = Blueprint("profile", __name__, url_prefix="/api")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@profile_bp.get("/profiles/<int:user_id>")
def get_public_profile(user_id):
    """Public route: Anyone can view a user's public profile and avatar."""
    user = User.query.get_or_404(user_id)
    profile = Profile.query.filter_by(UserID=user_id).first()

    return (
        jsonify({
            "user_id": user_id,
            "username": getattr(user, "Username", getattr(user, "username", "")),
            "bio": profile.Bio if profile else "",
            "profile_image": profile.ProfileImage if profile else "",
        }),
        200,
    )


@profile_bp.get("/profiles")
@jwt_required()
def get_profile():
    raw_identity = get_jwt_identity()
    try:
        current_user_id = int(raw_identity)
    except (ValueError, TypeError):
        current_user_id = raw_identity

    user = User.query.get_or_404(current_user_id)

    profile = Profile.query.filter_by(UserID=current_user_id).first()
    if not profile:
        profile = Profile(
            UserID=current_user_id, Bio="", Interests="", ProfileImage=""
        )
        db.session.add(profile)
        db.session.commit()

    user_posts = Content.query.filter_by(UserID=current_user_id).all()
    posts_data = [
        {
            "id": getattr(p, "ContentID", getattr(p, "id", None)),
            "title": getattr(p, "Title", getattr(p, "title", "Untitled Post")),
            "category": getattr(
                p, "Category", getattr(p, "category", "General")
            ),
            "created_at": (
                p.CreatedAt.strftime("%d %b %Y")
                if hasattr(p, "CreatedAt") and p.CreatedAt
                else ""
            ),
        }
        for p in user_posts
    ]

    return (
        jsonify({
            "profile_id": profile.ProfileID,
            "user_id": profile.UserID,
            "username": getattr(user, "Username", getattr(user, "username", "")),
            "email": getattr(user, "Email", getattr(user, "email", "")),
            "role": getattr(user, "Role", getattr(user, "role", "user")),
            "bio": profile.Bio or "",
            "interests": profile.Interests or "",
            "profile_image": profile.ProfileImage or "",
            "followers_count": getattr(user, "FollowersCount", 0),
            "following_count": getattr(user, "FollowingCount", 0),
            "posts_count": len(user_posts),
            "posts": posts_data,
            "member_since": (
                user.CreatedAt.strftime("%d %b %Y")
                if hasattr(user, "CreatedAt") and user.CreatedAt
                else ""
            ),
        }),
        200,
    )


@profile_bp.put("/profiles")
@jwt_required()
def update_profile():
    raw_identity = get_jwt_identity()
    try:
        current_user_id = int(raw_identity)
    except (ValueError, TypeError):
        current_user_id = raw_identity

    profile = Profile.query.filter_by(UserID=current_user_id).first()
    if not profile:
        profile = Profile(UserID=current_user_id)
        db.session.add(profile)

    data = request.get_json() or {}

    if "bio" in data:
        profile.Bio = data["bio"]
    if "interests" in data:
        profile.Interests = data["interests"]
    if "profile_image" in data or "profileImage" in data:
        profile.ProfileImage = data.get("profile_image") or data.get(
            "profileImage"
        )

    db.session.commit()

    return (
        jsonify({
            "message": "Profile updated successfully",
            "profile": {
                "profile_id": profile.ProfileID,
                "bio": profile.Bio or "",
                "interests": profile.Interests or "",
                "profile_image": profile.ProfileImage or "",
            },
        }),
        200,
    )


@profile_bp.patch("/profiles/avatar")
@jwt_required()
def update_profile_avatar():
    """Endpoint for uploading avatar files directly."""
    raw_identity = get_jwt_identity()
    try:
        current_user_id = int(raw_identity)
    except (ValueError, TypeError):
        current_user_id = raw_identity

    profile = Profile.query.filter_by(UserID=current_user_id).first()
    if not profile:
        profile = Profile(UserID=current_user_id)
        db.session.add(profile)

    if "profile_picture" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["profile_picture"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        filename = f"avatar_user_{current_user_id}_{secure_filename(file.filename)}"
        upload_folder = os.path.join(
            current_app.root_path, "static", "uploads", "avatars"
        )
        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        profile.ProfileImage = f"/static/uploads/avatars/{filename}"
        db.session.commit()

        return (
            jsonify({
                "message": "Profile picture updated successfully",
                "profile_image": profile.ProfileImage,
            }),
            200,
        )

    return jsonify({"error": "Invalid file format"}), 400