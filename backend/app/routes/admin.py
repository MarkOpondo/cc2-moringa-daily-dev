from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Content, ContentReport, Profile, User
from app.routes.content import _notify_subscribers, _status_value
from app.serializers import serialize_content, serialize_user
from app.utils import role_required


admin_bp = Blueprint("admin", __name__)


def _report_payload(report):
    return {
        "id": report.ReportID,
        "contentId": report.ContentID,
        "content": {"id": report.content.ContentID, "title": report.content.Title}
        if report.content
        else None,
        "reporter": {"id": report.reporter.UserID, "username": report.reporter.Username}
        if report.reporter
        else None,
        "reason": report.Reason,
        "status": (report.Status or "pending").lower(),
        "createdAt": report.CreatedAt.isoformat() if report.CreatedAt else None,
    }


@admin_bp.get("/content")
@jwt_required()
@role_required("admin")
def list_pending_content():
    status = request.args.get("status", "draft")
    model_status = _status_value(status)
    if not model_status:
        return jsonify({"error": "Invalid content status"}), 400
    items = Content.query.filter_by(Status=model_status).order_by(Content.CreatedAt.desc()).all()
    return jsonify([serialize_content(item) for item in items]), 200


@admin_bp.patch("/content/<int:content_id>/status")
@jwt_required()
@role_required("admin")
def update_content_status(content_id):
    content = db.session.get(Content, content_id)
    if not content:
        return jsonify({"error": "Content not found"}), 404

    data = request.get_json(silent=True) or {}
    status = _status_value(data.get("status"))
    if not status:
        return jsonify({"error": "status must be draft, published, or archived"}), 400

    was_public = content.Status == "Published" and content.IsApproved
    content.Status = status
    content.IsApproved = status == "Published"
    if status == "Published" and not was_public:
        content.RejectionReason = None
        _notify_subscribers(content)
    elif status == "Archived":
        content.RejectionReason = str(data.get("reason") or "Content was archived").strip()
    else:
        content.RejectionReason = None
    db.session.commit()
    return jsonify(serialize_content(content)), 200


@admin_bp.delete("/content/<int:content_id>")
@jwt_required()
@role_required("admin")
def delete_admin_content(content_id):
    content = db.session.get(Content, content_id)
    if not content:
        return jsonify({"error": "Content not found"}), 404
    db.session.delete(content)
    db.session.commit()
    return jsonify({"message": "Content deleted"}), 200


@admin_bp.get("/users")
@jwt_required()
@role_required("admin")
def list_users():
    return jsonify([serialize_user(user) for user in User.query.order_by(User.Username).all()]), 200


@admin_bp.post("/users")
@jwt_required()
@role_required("admin")
def add_user():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username") or "").strip()
    email = str(data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = str(data.get("role", "user") or "user").strip().lower()
    if not username or not email or not isinstance(password, str) or len(password) < 8:
        return jsonify({"error": "username, email, and a password of at least 8 characters are required"}), 400
    if role not in {"admin", "tech_writer", "user"}:
        return jsonify({"error": "Invalid role"}), 400
    if User.query.filter((User.Username == username) | (User.Email == email)).first():
        return jsonify({"error": "Username or email already exists"}), 409

    user = User(Username=username, Email=email, Role=role, IsActive=True)
    user.password_hash = password
    db.session.add(user)
    db.session.flush()
    db.session.add(Profile(UserID=user.UserID))
    db.session.commit()
    return jsonify(serialize_user(user)), 201


@admin_bp.patch("/users/<int:user_id>/status")
@jwt_required()
@role_required("admin")
def toggle_user_status(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.UserID == int(get_jwt_identity()):
        return jsonify({"error": "You cannot deactivate your own account"}), 400
    user.IsActive = not user.IsActive
    db.session.commit()
    return jsonify(serialize_user(user)), 200


@admin_bp.get("/reports")
@jwt_required()
@role_required("admin")
def list_reports():
    reports = ContentReport.query.order_by(ContentReport.CreatedAt.desc()).all()
    return jsonify([_report_payload(report) for report in reports]), 200


@admin_bp.patch("/reports/<int:report_id>")
@jwt_required()
@role_required("admin")
def resolve_report(report_id):
    report = db.session.get(ContentReport, report_id)
    if not report:
        return jsonify({"error": "Report not found"}), 404
    report.Status = "Resolved"
    db.session.commit()
    return jsonify(_report_payload(report)), 200
