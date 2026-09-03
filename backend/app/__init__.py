from flask import Flask, jsonify

from app.extensions import db, migrate, jwt, bcrypt, cors, ma
from config import config_by_name


def create_app(config_class=None, config_name=None):
    # Accept either kwarg (`config_class` or `config_name`) so callers
    # like run.py's create_app(config_name="development") don't crash.
    if config_class is None:
        config_class = config_name or "development"
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_by_name[config_class])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": "*"
            }
        }
    )
    ma.init_app(app)

    # Import models
    with app.app_context():
        from app import models

    # Import route Blueprints
    from app.Routes.auth_profile import auth_profile_bp
    from app.Routes.profile import profiles_bp
    from app.Routes.categories import categories_bp
    from app.Routes.content import content_bp
    from app.Routes.comments import comments_bp
    from app.Routes.interactions import interactions_bp
    from app.Routes.notifications import notifications_bp
    from app.Routes.reports import reports_bp
    from app.Routes.subscriptions import subscriptions_bp
    from app.Routes.comment_reactions import comment_reactions_bp
    from app.Routes.admin import admin_bp
    from app.Routes.ai_routes import ai_bp

    # Register Blueprints
    # auth_profile_bp carries /auth/register, /auth/login, /auth/logout,
    # /auth/forgot-password, /auth/reset-password, /auth/change-password,
    # /me and /auth/me (profile of the logged-in user).
    app.register_blueprint(auth_profile_bp, url_prefix="/api")
    app.register_blueprint(profiles_bp, url_prefix="/api/profiles")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(content_bp, url_prefix="/api/content")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(comments_bp, url_prefix="/api")
    app.register_blueprint(interactions_bp, url_prefix="/api")
    app.register_blueprint(
        notifications_bp,
        url_prefix="/api/users/me/notifications"
    )
    app.register_blueprint(
        subscriptions_bp,
        url_prefix="/api"
    )
    app.register_blueprint(
        comment_reactions_bp,
        url_prefix="/api"
    )
    app.register_blueprint(
        reports_bp,
        url_prefix="/api"
    )
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    @app.get("/")
    def index():
        return jsonify({
            "message": "My Moringa Daily app"
        })

    return app
