#----------------------------------Profile => ROUTES---------#
@bp.get("/api/profiles")
@jwt_required()
def get_profile():
    current_user_id=get_jwt_identity()

    profile=Profile.query.filter_by(user_id=current_user_id).first()

    if not profile:
        return jsonify({
            "error": "Profile not found"
        }),404
    return jsonify({
        "profile_id": profile.id,
        "user_id": profile.user_id,
        "bio": profile.bio,
        "skills": profile.skills,
        "github_url": profile.github_url
    }),200

@bp.put("/api/profiles")
@jwt_required()
def update_profile():
    current_user_id=get_jwt_identity()

    profile = Profile.query.filter_by(user_id=current_user_id).first()
    if not profile:
        return jsonify({
            "error": "Profile not found"
        }),404
    data=request.get_json()
    profile.bio=data.get("bio", profile.bio)
    profile.skills=data.get("skills", profile.skills)
    profile.github_url=data.get("github_url", profile.github_url)
    
    
    db.session.commit()
    return jsonify({
        "message": "Profile updated successfully"
    }),200

#--------------------------------------------------   