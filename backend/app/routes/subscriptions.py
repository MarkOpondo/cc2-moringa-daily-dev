from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Category, Subscription


subscriptions_bp = Blueprint("subscriptions", __name__)


@subscriptions_bp.get("")
@jwt_required()
def get_my_subscriptions():
    subscriptions = Subscription.query.filter_by(UserID=int(get_jwt_identity())).all()
    return jsonify(
        [
            {
                "id": subscription.SubscriptionID,
                "categoryId": subscription.CategoryID,
                "createdAt": subscription.CreatedAt.isoformat()
                if subscription.CreatedAt
                else None,
            }
            for subscription in subscriptions
        ]
    ), 200


@subscriptions_bp.post("")
@jwt_required()
def subscribe_to_category():
    data = request.get_json(silent=True) or {}
    category_id = data.get("categoryId", data.get("category_id"))
    if not category_id:
        return jsonify({"error": "categoryId is required"}), 400

    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    subscription = Subscription(
        UserID=int(get_jwt_identity()),
        CategoryID=category.CategoryID,
    )
    db.session.add(subscription)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Already subscribed to this category"}), 409

    return jsonify(
        {
            "id": subscription.SubscriptionID,
            "categoryId": category.CategoryID,
            "categoryName": category.Name,
        }
    ), 201


@subscriptions_bp.delete("/<int:category_id>")
@jwt_required()
def unsubscribe_from_category(category_id):
    subscription = Subscription.query.filter_by(
        UserID=int(get_jwt_identity()), CategoryID=category_id
    ).first()
    if not subscription:
        return jsonify({"error": "Subscription not found"}), 404

    db.session.delete(subscription)
    db.session.commit()
    return jsonify({"message": "Unsubscribed successfully"}), 200
