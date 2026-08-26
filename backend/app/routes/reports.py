from flask import Blueprint, request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.extensions import db
from app.models import ContentReport
from app.utils import role_required

reports_bp= Blueprint("reports", __name__)

@reports_bp.post("/content/<int:content_id>/report")
@jwt_required()
def report_content(content_id):
    data = request.get_json()
    if not data:
        data={}

    report = ContentReport(
        ReportedBy= int(get_jwt_identity()),
        ContentID=content_id,
        Reason= data.get("reason", "No reason provided"),
        Status="Pending"
    )

    db.session.add(report)
    db.session.commit()
    return jsonify({"message": "Report submitted. "}),201
#------------------------- LIST REPORTS-------------------
@reports_bp.get("/reports")
@jwt_required()
@role_required("admin")
def list_reports():
    # default show unresolved. ?resolved=true for all
    status= request.args.get("status")

    query = ContentReport.query
    
    if status:
        query=query.filter_by(Status=status)
    reports =query.order_by(
        ContentReport.CreatedAt.desc()
    ).all()    
    
    return jsonify([{
        "id": report.ContentReport.id,
        "content_id": report.contentID,
        "user_id": report.ReportedBy,
        "reason": report.Reason,
        "status": report.Status
    }for report in reports]),200

#------------------------------------ Resolve reports-------
@reports_bp.patch("/reports/<int:report_id>")
@jwt_required()
@role_required("admin")
def resolve_report(report_id):

    report = ContentReport.query.get_or_404(report_id)
    report.Status="resolved"
    
    db.session.commit()
    return jsonify({"message": "Report resolved."}),200

