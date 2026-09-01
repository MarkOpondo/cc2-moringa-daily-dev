from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import User, Profile
from app.utils import role_required

users_bp = Blueprint("users", __name__)

#--------------------- ADMIN ROUTES--------------
@users_bp.get("")
@jwt_required()
@role_required("Admin")
def list_all_users():
    users = User.query.all()
    return jsonify([{
        "id": user.UserID,
        "username": user.Username,
        "email": user.Email,
        "role": user.Role,
        "is_active": user.IsActive
    } for user in users]),200

@users_bp.post("")   
@jwt_required()
@role_required("Admin")
def admin_add_user():
    """ 
   Add a new user
    --- tags: 
    - Users 
    summary: Create a new user 
    description: > 
        Allows an authenticated administrator to create a new user account.
        The new user is assigned the specified role or defaults to "user" 
        when no role is provided.
    security: - Bearer: [] 
    consumes: - application/json 
    parameters:
        - name: body 
        in: body
        required: true 
        description: User information required to create the account. 
        schema:
         type: object 
         required: 
            - username 
            - email
             - password 
        properties: 
            username: 
            type: string 
            description: Unique username for the new account. 
            example: john_doe
                email: 
                type: string 
                format: email 
                description: Unique email address for the new account. 
                example: john@example.com 
             password: 
             type: string 
             format: password 
             description: Password for the new account. 
             example: Password123 
             role:
              type: string 
              description: Role assigned to the new user. 
              example: user 
              default: user 
    responses: 
    201: 
        description: User created successfully. 
        schema: 
            type: object 
            properties: 
            message: 
            type: string 
            example: User added successfully 
            user_id: 
            type: integer
            example: 245 
    400:
     description: Invalid request. Required fields are missing. 
    401:
     description: Authentication is required. 
    403:
     description: Access denied. Administrator privileges are required. 
     409: 
     description: Username or email already exists.
    """

    data = request.get_json() 
    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if not all ([
        data.get("username"),
         data.get("email"), 
         data.get("password")]):

        return jsonify({"error": "Username, email and password are required"}), 400
    existing = User.query.filter(
        (User.Username == data["username"]) | (User.Email ==  data["email"])
    ).first()
    
    if existing:
        return jsonify({"error": "Username or email already exists"}), 409

    new_user= User(
        Username = data["username"],
        Email=data["email"],
        Role=data.get("role", "user"),
        IsActive=True
    )    
    new_user.password_hash=data["password"]
    db.session.add(new_user)
    db.session.flush()

    db.session.add(Profile(UserID=new_user.UserID))
    db.session.commit()

    return jsonify({
        "message": "User added successfully",
        "user_id": new_user.UserID
    }), 201

@users_bp.patch("/<int:user_id>/deactivate")
@jwt_required()
@role_required("Admin")
def deactivate_user(user_id):
    user= User.query.get_or_404(user_id)
    user.IsActive = not user.IsActive
    db.session.commit()
    return jsonify({
        "message": f"User '{user.Username}' has been deactivated."}),200

#--------------------------CURRENT USER ROUTES -------
@users_bp.get("/me")
@jwt_required()
def get_current_user():
    """
    Get current authenticated user
    ---
    tags:
      - Users
    security:
      - Bearer: []
    responses:
      200:
        description: Current user details
      404:
        description: User not found
    """
    user= User.query.get(int(get_jwt_identity()))

    if not user:
        return jsonify({"error": "User not found."}),404

    return jsonify({
        "id": user.UserID,
        "username": user.Username,
        "email": user.Email,
        "role": user.Role,
        "is_active": user.IsActive
    }),200  

@users_bp.put("/me")
@jwt_required()
def update_current_user():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({
            "error": "User not found"
        }),404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required" }),400

    if "username" in data:
        # Checks for the uniqueness
        existing_username = User.query.filter(
            User.Username == data["username"],
            User.UserID != user.UserID
        ).first()

        if existing_username:
            return jsonify({"error": "Username already taken"}),409
        user.Username= data["username"]

    if "email" in data:
        existing_email= User.query.filter(
            User.Email==data["email"],
            User.UserID!= user.UserID
        ).first()
        if existing_email:
            return jsonify({
                "error": "Email already taken"
            }),409
        user.Email=data["email"]

    if "password" in data:
         user.password_hash=data["password"]

    db.session.commit()

    return jsonify({"message": "Account has been updated successfully"}),200                