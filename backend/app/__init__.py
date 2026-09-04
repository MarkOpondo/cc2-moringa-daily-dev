from flask import Flask, jsonify

from app.extensions import bcrypt, cors, db, jwt, ma, migrate
from config import config_by_name


def create_app(config_class="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_class])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    @jwt.unauthorized_loader
    def missing_token(reason):
        return jsonify({"error": reason}), 401

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return jsonify({"error": reason}), 401

    @jwt.expired_token_loader
    def expired_token(_header, _payload):
        return jsonify({"error": "Token has expired"}), 401

    @jwt.token_verification_loader
    def verify_active_user(_header, payload):
        from app.models import User

        try:
            user = db.session.get(User, int(payload["sub"]))
        except (KeyError, TypeError, ValueError):
            return False
        return bool(user and user.IsActive)

    @jwt.token_verification_failed_loader
    def failed_token_verification(_header, _payload):
        return jsonify({"error": "Active user account required"}), 403

    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": app.config["FRONTEND_URL"],
            }
        },
    )
    ma.init_app(app)

    # Import models before registering routes so SQLAlchemy knows every table.
    with app.app_context():
        from app import models  # noqa: F401

    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp
    from app.routes.categories import categories_bp
    from app.routes.comment_reactions import comment_reactions_bp
    from app.routes.comments import comments_bp
    from app.routes.content import content_bp
    from app.routes.interactions import interactions_bp
    from app.routes.notifications import notifications_bp
    from app.routes.profile import profiles_bp
    from app.routes.reactions import reactions_bp
    from app.routes.reports import reports_bp
    from app.routes.subscriptions import subscriptions_bp
    from app.routes.users import users_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(profiles_bp, url_prefix="/api/profiles")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(content_bp, url_prefix="/api/content")
    app.register_blueprint(comments_bp, url_prefix="/api")
    app.register_blueprint(interactions_bp, url_prefix="/api")
    app.register_blueprint(reactions_bp, url_prefix="/api")
    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")
    app.register_blueprint(subscriptions_bp, url_prefix="/api/subscriptions")
    app.register_blueprint(comment_reactions_bp, url_prefix="/api")
    app.register_blueprint(reports_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    @app.get("/")
    def index():
        return jsonify({"message": "Moringa Daily Dev API"})

    return app
