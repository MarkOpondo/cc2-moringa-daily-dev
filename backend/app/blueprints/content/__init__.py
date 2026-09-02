from flask import Blueprint

content_bp = Blueprint("content", __name__, url_prefix="/api")

# Import sub-modules so their routes register with the blueprint
from app.blueprints.content import admin, comments, creation, feed, reactions