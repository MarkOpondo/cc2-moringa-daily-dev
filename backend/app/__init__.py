import os
from datetime import timedelta
from flask import Flask, send_from_directory, request, make_response
from flask_cors import CORS
from config import DevelopmentConfig, config_by_name
from app.extensions import db, jwt, migrate


def create_app(config_name=None):
    app = Flask(__name__, static_folder="../static")

    # 1. Enable Global CORS to allow cross-origin React requests
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )

    # 2. Intercept and resolve HTTP OPTIONS preflight requests cleanly
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add(
                "Access-Control-Allow-Headers", "Content-Type, Authorization"
            )
            response.headers.add(
                "Access-Control-Allow-Methods",
                "GET, POST, PUT, PATCH, DELETE, OPTIONS",
            )
            return response, 200

    # Serve uploaded static media files
    @app.route("/static/uploads/<path:filename>")
    def serve_upload(filename):
        upload_dir = os.path.join(app.root_path, "..", "static", "uploads")
        return send_from_directory(upload_dir, filename)

    # Load configuration from config.py
    if not config_name:
        config_name = os.getenv("FLASK_ENV", "development")

    config_class = config_by_name.get(config_name, DevelopmentConfig)
    app.config.from_object(config_class)

    # Fallback default if DATABASE_URL is missing in .env
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
            app.root_path, "app.db"
        )
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)

    # Initialize Flask Extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app,
    resources={r"/api/*": {"origins": "*"}},
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True)

   # Import Blueprints matching all files in app/routes/
    from app.routes.admin import admin_bp
    from app.routes.auth_profile import auth_profile_bp
    from app.routes.categories import categories_bp
    from app.routes.comment_reactions import comment_reactions_bp
    from app.routes.comments import comments_bp
    from app.routes.content import content_bp
    from app.routes.interactions import interactions_bp
    from app.routes.notifications import notifications_bp
    from app.routes.reports import reports_bp
    from app.routes.subscriptions import subscriptions_bp

    # Disable strict slashes globally
    app.url_map.strict_slashes = False

    # Register Blueprints with correct API URL prefixes matching your frontend requests
    app.register_blueprint(auth_profile_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(content_bp, url_prefix="/api/content")
    app.register_blueprint(comments_bp, url_prefix="/api")
    app.register_blueprint(comment_reactions_bp, url_prefix="/api")
    app.register_blueprint(interactions_bp, url_prefix="/api")
    app.register_blueprint(notifications_bp, url_prefix="/api/users/me/notifications")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")
    app.register_blueprint(subscriptions_bp, url_prefix="/api/users/me/subscriptions")

    # Ensure database tables exist upon app startup
    with app.app_context():
        db.create_all()

    
    return app

   
