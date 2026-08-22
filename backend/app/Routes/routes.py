from flask import Flask, Blueprint, jsonify, request
from app import db
from app.models import User, Profile
# from app.schemas import

bp=Blueprint("api", __name__)

#---------------------Authentication =>ROUTE ----------------#
@bp.post("/api/auth/register")
def signup():
    data = request.get_json()

    username=data.get("username")
    email=data.get("email")
    password=data.get("password")
    # Checks for any blank spot
    if not username or not email or not password:
        return jsonify({
            "error":"Username, email and password are required."
        }),400

        # Check if the username already exists
    existing_user = User.query.filter((User.username==username) | (User.email==email)).first()

    if existing_user:
        return jsonify({
            "error": "Username or email already Exists"
        }),409  

    # Create new user 
    new_user=User(
        username=username,
        email=email,
        role="user",
        is_active=True, 
    ) 
    # Hash the password
    new_user.set_password(password)  

    db.session.add(new_user)
    db.session.flush()
    new_profile=Profile(user_id=new_user.id)
    db.session.add(new_profile)
    db.session.commit()

    return jsonify({
        "message": "User created successfully."
    }),201 

@bp.post("/api/auth/login")
def login():
    data=request.get_json()

    username=data.get("username")
    password=data.get("password")

    user=User.query.filter_by(username=username).first()
   
    # checks existing users
    if not user:
        return jsonify({
            "error": "Invalid username or password"
        }),401

    if not user.check_password(password):
        return jsonify({
            "error": "Invalid username or password"
        }),401 
    if not user.is_active:
        return jsonify({
            "error": "Account is inactive"
        }),403

    access_token=create_access_token(
        identity=str(user.id)
    )  
    return jsonify({
        "token": access_token,
        "message": "Login successful"
    }),200

@bp.post("api/auth/logout")
def logout():
    return jsonify({
        "message": "Logout successful"
    }),200
    

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