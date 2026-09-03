from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/', methods=['GET'])
@notifications_bp.route('/notifications', methods=['GET'])
@notifications_bp.route('/users/me/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    # Frontend expects a DIRECT list []
    return jsonify([]), 200