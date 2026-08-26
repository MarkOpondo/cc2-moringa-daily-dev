from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Content, User, Subscription, Notification
from app.utils import role_required

content_bp = Blueprint("content", __name__)

#----------------------------- NOTIFY SUBSCRIBERS-----
def _notify_subscribers(content_item):
    """ Send notifications to users subscribed to this content's category."""
     notifications=[]
    for category in content_item.categories:
        subscriptions = Subscription.query.filter_by(CategoryID=category.CategoryID).all()
    for sub in subscriptions:
        if sub.UserID != content_item.UserID:
            Notification.append(
                Notification(
                    UserID= sub.UserID,
                    ContentID=content_item.ContentID,
                    message=f"New content in your feed: '{content_item.Title}'"
                )
            )
      
    if notifications:
        db.session.add_all(notifications)
        db.session.commit()

#-------------------------PUBLIC CONTENT ROUTES ----------
#------------------------- GET A LIST OF CONTENT----------
@content_bp.get("")
def list_content():
    category_id = request.args.get("category_id", type=int)
    status = request.args.get("status")
    content_type = request.args.get("type")

    query = Content.query

# Filter by category through the many to many relationship
    if category_id:
        query = query.filter(Content.categories.any(Category.CategoryID==category_id)
    )

    if content_type:
        query = query.filter_by(ContentType= content_type)

    if status:    
        query=query.filter_by(Status=status)

    items = query.order_by(Content.CreatedAt.desc()).all() 
    return jsonify([{
        "id": content.ContentID,
        "title": content.Title,
        "description": content.Description,
        "type": content.ContentType,
        "url": content.ContentURL,
        "status":content.Status,
        "author_id":content.UserID,

        "category":[
            {
                "id": category.CategoryID,
                "name": category.Name
            }
        ],
        "created_at": (
            content.created_at.isoformat()
         if created_at else None
         )
    }for content in items]), 200

#----------------------------------- GET A SPECIFIC CONTENT--------------
@content_bp.get("/<int: content_id>")
def get_single_content(content_id):
    item = Content.query.get_or_404(content_id)

    return jsonify({
        "id": item.ContentID,
        "title": item.Title,
        "description": item.Description,
        "type": item.ContentType,
        "url": item.ContentURL,
        "status": item.Status,
        "auth_id": item.UserID,
        "category_id": [
            {
                "id": category.CategoryID,
                "name": category.Name
            }
            for category in item.categories
        ],
        "created_at": (
            item.created_at.isoformat()
         if item.created_at else None
        )
    }), 200

#--------------------------- CREATE CONTENT-----------
@content_bp.post("")
@jwt_required()
@role_required("tech_writer", "user")
def create_content():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No input data provided"
        })

    user_id= int(get_jwt_identity())

    user= User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}),404

    required = ["title", "type", "category_id"]

    if not all(data.get(field) for field in required):
        return jsonify({"error": "title, type and category_id are required."}), 400

    category = Category.query.get(data["catgeory_id"])
    if not category:
        return jsonify({"error":"Category not found"}),404
    status = "pending"
        # Auto-approve for admin/tech-writer: pending for regular users
    new_content = Content(
        UserID=user_id,
        Title=data["title"],
        Description=data.get("description"),
        ContentType=data["type"],
        ContentURL= data.get("url"),
        Status=status,
        IsApproved=False
    )  
   
   # Add the category through the many-to-many relationship
   new_content.categories.append(category)
   db.session.add(new_content)
   db.session.commit()

   return jsonify({
    "id": new_content.ContentID,
    "message": "Content submitted successfully"
   }),201 

#------------------------------ MODIFICATION------
@content_bp.put("<int: content_id>")
@jwt_required()
@role_required("tech_writer")
def edit_content(content_id):
    item = Content.query.get_or_404(content_id)
    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user:
        return jsonify({
            "error": "user not found"
        }),404

    if item.UserID != current_user.UserID:
        retrun jsonify({"error": "Forbidden"}),403

    data= request.get_json()

    item.Title=data.get("title",item.Title)
    item.Description= data.get("body", item.Description)
    item.ContentURL=data.get("url", item.ContentURL)
    item.ContentType= data.get("type", item.ContentType)
    
    #update category if provided
    if "category_id" in data:
        category = Category.query.get(
            data["category_id"]
        )
    if not category:
        return jsonify({
            "Error": "Category is not found"
        }) ,404

    item.categories=[category]   

    db.session.commit()
    return jsonify({"message": "Content updated."}),200

#-------------------------- DELETE/REMOVE CONTENT--------
@content_bp.delete("/<int:content_id>")
@jwt_required()
def delete_content(content_id):
    item= Content.query.get_or_404(content_id)

    current_user = User.query.get(int(get_jwt_identity()))
    if not current_user:
        return jsonify({
            "error": "User not found"
        }),404

    if item.author_id != current_user.id and current_user.role != "admin":
        return jsonify({"error": "Forbidden."}),403
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Content deleted"}), 200

#------------------------APPROVE CONTENT -----------------
@content_bp.patch("<int: content_id>/approve")
@jwt_required()
@role_required("admin", "tech_writer")
def approve_content(content_id):
    item= Content.query.get_or_404(content_id)

    item.status="Published"
    item.IsApproved= True

    db.session.commit()

    _notify_subscribers(item)
    return jsonify({"message": "Content approved"}),200

#--------------------------------- FLAG CONTENT ------------
@content_bp.patch("/<int:content_id>/flag")
@jwt_required()
@role_required("admin", "tech_writer")
def flag_content(content_id):
    item= Content.query.get_or_404(content_id)
    #The current Content model does not have a Flagged status
    item.IsApproved =False
    db.session.commit()
    
    return jsonify({"message": "Content flagged."}),200                   





        