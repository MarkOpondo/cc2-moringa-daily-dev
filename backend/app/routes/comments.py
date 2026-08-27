from flask import Blueprint,request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db

comments_bp =Blueprint("comments", __name__)

def _build_comment_tree(comment):
    """ Recursively serialize a comment and its replies. """
    return(
        "id": comment.CommentID,
        "body": comment.Text,
        "user_id": comment.UserID,
        "parent_id": comment.ParentCommentID,
        "created_at": (comment.created_at.isoformat()
         if comment.CreatedAt else None),
        "replies": [_build_comment_tree(reply) for reply in comment.replies]
    )

#--------------------- GET COMMENTS FROM CONTENT -----
@comments_bp.get("/content/<int:content_id>/comments")
def get_comments(content_id):
    # Fetch only top-level comments: 
    #replies nest via relationship
    top_level= Comment.query.filter_by(
        ContentID= content_id,
        ParentCommentID=None
    
    ).order_by(Comment.CreatedAt.asc()).all()
    return jsonify([_build_comment_tree(comment) for coment in top_level]),200 

#--------------------- CREATE A COMMENT ---------------
@comments_bp.post("/content/<int:content_id>/comments")
@jwt_required()
def add_comment(content_id):

    data = request.get_json()

    if not data or not data.get("body"):
        return jsonify({"error": "Comment body is required"}), 400
    
    new_comment = Comment(
        Text =data["body"],
        ContentID=content_id,
        UserID=int(get_jwt_identity())
        ParentCommentID=data.get("parent_comment_id")
    )   

    db.session.add(new_comment)
    db.session.commit()
    return jsonify({
        "id": new_comment.CommentID,
        "message": "Comment added."
    }),201

#--------------------- MODIFY A COMMENT -----------
@comments_bp.put("/comments/<int:comment_id>")
@jwt_required()  
def edit_comment(comment_id):

    comment= Comment.query.get_or_404(comment_id)

    if comment.UserID != int(get_jwt_identity()):
        return jsonify({"error": "You can only edit your own comments"}), 403
    
    data = request.get_json()   
    if not data:
        return jsonify({
            "error": "Request body is required"
        }),400

    comment.Text = data.get("body", comment.Text)
    db.session.commit()
    return jsonify({
        "message": "Comment has been updated successfully"
    }),200

#---------------------------- DELETE A COMMENT ----------------
@comments_bp.delete("/comments/<int:comment_id>")
@jwt_required()
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if comment.UserID != int(get_jwt_identity()):
        return jsonify({"error": "You can only delete your own comments."}),403
    
    db.session.delete(comment)
    db.session.commit() 
    return jsonify({"message": "Comment deleted"}), 200     





#------------------------ GET A LIST OF COMMENTS FROM A CONTENT--------
#------------------------ GET A SPECIFIC COMENT FROM A CONTENT---------
#------------------------ CREATE A COMMENT-------------------
#------------------------ MODIFCATION -----------------------
#------------------------  DELETE A COMMENT---------------------