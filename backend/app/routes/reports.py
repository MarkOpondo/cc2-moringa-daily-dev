from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Content, ContentReport, User


reports_bp = Blueprint("reports", __name__)


@reports_bp.post("/content/<int:content_id>/report")
@jwt_required()
def report_content(content_id):
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    reason = str(data.get("reason") or "").strip()
    content = db.session.get(Content, content_id)
    if not content or content.Status != "Published" or not content.IsApproved:
        return jsonify({"error": "Published content not found"}), 404
    if not reason:
        return jsonify({"error": "Reason is required"}), 400

    report = ContentReport(
        ReportedBy=user_id,
        ContentID=content_id,
        Reason=reason,
        Status="Pending",
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({"id": report.ReportID, "status": "pending"}), 201
