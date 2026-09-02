import os
from flask import current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename
from app import db
from app.models import Category, Content
from . import content_bp


@content_bp.post("/content")
@jwt_required()
def create_content():
    current_user_id = get_jwt_identity()

    title = request.form.get("title")
    description = request.form.get("description") or request.form.get("summary")
    content_type = request.form.get("content_type", "article")
    duration = request.form.get("duration")
    hashtags = request.form.get("hashtags")
    category_id = request.form.get("category_id") or request.form.get("category")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    content_url = request.form.get("content_url")
    upload_folder = os.path.join(current_app.root_path, "static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    if "media_file" in request.files:
        file = request.files["media_file"]
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, filename))
            content_url = f"/static/uploads/{filename}"

    new_content = Content(
        UserID=current_user_id,
        Title=title,
        Description=description,
        ContentType=content_type,
        ContentURL=content_url,
        Duration=int(duration) if duration and str(duration).isdigit() else None,
        ViewsCount=0,
        LikesCount=0,
        Hashtags=hashtags,
        Status="Pending",
    )

    if category_id:
        try:
            cat_ids = [int(category_id)]
            cats = Category.query.filter(Category.CategoryID.in_(cat_ids)).all()
            new_content.categories.extend(cats)
        except ValueError:
            pass

    db.session.add(new_content)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Content submitted for review successfully",
                "content_id": new_content.ContentID,
            }
        ),
        201,
    )