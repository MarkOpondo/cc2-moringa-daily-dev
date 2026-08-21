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

@app.post("api/auth/logout")
def logout():
    return jsonify({
        "message": "Logout successful"
    }),200
    