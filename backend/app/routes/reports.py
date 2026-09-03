from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Content, ContentReport, User
from app.utils import iso_utc, role_required

reports_bp = Blueprint("reports", __name__)


def safe_get_user_id():
    """Extract integer user ID safely from JWT identity."""
    identity = get_jwt_identity()
    if isinstance(identity, dict):
        return int(identity.get("id"))
    return int(identity)


# --------------------- USER ENDPOINTS --------------------- #

# Endpoint: POST /api/content/<int:content_id>/report
# (alias: POST /api/content/<int:content_id> kept for older clients)
@reports_bp.post("/content/<int:content_id>/report")
@reports_bp.post("/content/<int:content_id>")
@jwt_required()
def report_content(content_id):
    content = db.session.get(Content, content_id)
    if not content:
        return jsonify({"error": "Content not found."}), 404

    data = request.get_json(silent=True) or {}
    reason = data.get("reason")

    if not reason or not str(reason).strip():
        return jsonify({"error": "Reason is required."}), 400

    try:
        user_id = safe_get_user_id()
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid user identity."}), 400

    report = ContentReport(
        ReportedBy=user_id,
        ContentID=content_id,
        Reason=reason.strip(),
        Status="Pending",
    )

    db.session.add(report)
    db.session.commit()

    return jsonify({"message": "Report submitted successfully."}), 201


# --------------------- ADMIN ENDPOINTS --------------------- #

# Endpoint: GET /api/reports (with optional ?status=Pending)
@reports_bp.get("/reports")
@jwt_required()
@role_required("Admin")
def list_reports():
    status = request.args.get("status")

    query = ContentReport.query
    if status:
        query = query.filter_by(Status=status)

    reports = query.order_by(ContentReport.CreatedAt.desc()).all()

    result = []
    for report in reports:
        content = db.session.get(Content, report.ContentID)
        reporter = db.session.get(User, report.ReportedBy)
        created_at = iso_utc(report.CreatedAt) if report.CreatedAt else None
        status = report.Status or "Pending"
        result.append({
            "id": report.ReportID,
            "content_id": report.ContentID,
            "contentId": report.ContentID,
            "user_id": report.ReportedBy,
            "reason": report.Reason,
            "status": status,
            "created_at": created_at,
            "createdAt": created_at,
            "content": {"id": report.ContentID, "title": content.Title if content else f"Content #{report.ContentID}"},
            "reporter": {"id": report.ReportedBy, "username": reporter.Username if reporter else f"User #{report.ReportedBy}"},
        })

    return (
        jsonify(result),
        200,
    )


# Endpoint: PATCH /api/reports/<int:report_id>
@reports_bp.patch("/reports/<int:report_id>")
@jwt_required()
@role_required("Admin")
def resolve_report(report_id):
    report = db.session.get(ContentReport, report_id)
    if not report:
        return jsonify({"error": "Report not found."}), 404

    report.Status = "Resolved"
    db.session.commit()

    return jsonify({"message": "Report resolved successfully."}), 200