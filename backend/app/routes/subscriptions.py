from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Subscription, Category

subscriptions_bp = Blueprint("subscriptions", __name__)

#------------------ SUBSCRIBE TO CATEGORY ------------------
@subscriptions_bp.post("")
@jwt_required()
def subscribe_to_category(category_id):
    user_id = int(get_jwt_identity())

    data=request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}),400
    
    category_id= data.get("category_id")
    if not category_id:
        return jsonify({"error": "category_id is required"}),400   

    # checking that the category exists
    category=Category.query.get_or_404(category_id)

    # Check if the user is already subscribed
    existing = Subscription.query.filter_by(
        UserID=user_id,
        CategoryID= category_id
    ).first()
    if existing:
        return jsonify({
            "error": "You already subscribed to this category"
        }),409
    subscription = Subscription(
        UserID = user_id,
        CategoryID = category_id
    )    
    db.session.add(subscription)
    db.session.commit()
    return jsonify({
        "message": "Subscribed successfully",
        "subscription_id": subscription.SubscriptionID,
        "category_id":category.CategoryID,
        "category_name": category.Name
    }),201

#--------------------------------GET MY SUBSCRIPTIONS-------------
@subscriptions_bp.get("")
 @jwt_required()
 def get_my_subscriptions():
    user_id= int(get_jwt_identity())

    subscriptions= Subscription.query.filter_by(
        UserID=user_id
    ).all()
    return jsonify([
        {
            "subscription_id": subscription.SubscriptionID,
            "category_id": subscription.CategoryID,
            "CreatedAt": (
                subscription.CreatedAt.isoformat()
                if subscription.CreatedAt
                else None
            )
        }
        for subscription in subscriptions
    ]),200   

#------------------------------ UNSUBSCRIBE -----------------------------
@subscriptions_bp.delete("/<int:category_id>")
@jwt_required()
def unsubscribe_from_category(category_id):
    user_id = int(get_jwt_identity())

    subscription = Subscription.query.filter_by(
        UserID= user_id,
        CategoryID=category_id,
    ).first()    
    if not subscription:
        return jsonify({
            "error": "You are not a subscriber to this cateory."
        }),404
    db.session.delete(subscription)
    db.session.commit()
        return jsonify({
            "message": "Unsubscribed successfully"
        }),200