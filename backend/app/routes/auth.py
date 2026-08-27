from flask import Blueprint, request,jsonify
from flask_jwt_extended import create_access_token
from app.extensions import db, bcrypt
from app.models import User, Profile

auth_bp=Blueprint("auth", __name__)

#------------------------------ Signup-----------
@auth_bp.post("/register")
def register():
    data=request.get_json()

    if not data:
        return jsonify({"Error": "No input data provided."}),400

    username= data.get("username")
    email=data.get("email")
    password=data.get("password")

    if not all([username,email,password]):
        return jsonify({"error": "username, email, password are required"}),400
        existing= User.query.filter(
            (User.Username == username) | (User.Email == email)
        ).first()

    if existing:
        return jsonify({"error": "Username or email already exists."}), 400

    password_Hash= bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(
        Username = username,
        Email= email,
        _password_Hash= password_Hash,
        Role = "user",
        IsActive=True
    )        
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.flush()

    new_profile=Profile(userID= new_user.UserID)
    db.session.add(new_profile)
    db.session.commit()
    return jsonify({
        "message": "User created successfully.",
        "user_id": new_user.UserID
    }), 201

#------------------------------ login -----------------
@auth_bp.post("/login")
def login():
    data = reqquest.get_json()

    if not data:
        return jsonify({"error": "No input data provided."}), 400
    username=data.get("username")
    password=data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    user =  User.query.filter_by(Username=username).first()

    if not user or not bcrypt.check_password_hash(user._Password_Hash,password):
        return jsonify({"error": " Invalid Username or password"}), 401
    
    if not user.IsActive:
        retrun jsonify({"error": "Account is inacive. Contact the admin"}), 403
    access_token= create_access_token(identity=str(user.UserID))

    return jsonify({
        "token": access_token,
        "user":{
            "id": user. UserID,
            "username": user.Username,
            "email": user.Email,
            "role": user.Role
        },
        "message": "Login successful"
    }), 200
#--------------------------------logout----------------------
@auth_bp.post("/logout")
def logout():
    return jsonify({"message": "Logout successful."}), 200





