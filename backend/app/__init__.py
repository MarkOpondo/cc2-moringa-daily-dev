from flask import Flask, jsonify
import os

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
    from app.routes.auth_profile import auth_profile_bp
    from app.routes.profile import profiles_bp
    from app.routes.categories import categories_bp
    from app.routes.content import content_bp
    from app.routes.comments import comments_bp
    from app.routes.interactions import interactions_bp
    from app.routes.notifications import notifications_bp
    from app.routes.reports import reports_bp
    from app.routes.subscriptions import subscriptions_bp
    from app.routes.comment_reactions import comment_reactions_bp
    from app.routes.admin import admin_bp
    from app.routes.ai_routes import ai_bp

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
    # FIX: subscriptions used to sit under /api with "" routes, so
    # /api/subscriptions 404'd (and its CORS preflight failed).
    app.register_blueprint(
        subscriptions_bp,
        url_prefix="/api/subscriptions"
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

    # ------------------------------------------------------------------
    # JSON error handling
    # ------------------------------------------------------------------
    # Without this, an unhandled exception in debug mode escalates to the
    # Werkzeug debugger page, which carries NO CORS headers — the browser
    # then reports a misleading CORS error instead of the real problem.
    # Returning JSON keeps flask-cors's headers on every error response.
    from werkzeug.exceptions import HTTPException

    from app.schema_doctor import looks_like_schema_drift, schema_drift_hint

    @app.errorhandler(Exception)
    def handle_uncaught_error(error):
        if isinstance(error, HTTPException):
            return jsonify({"error": error.description}), error.code

        app.logger.exception("Unhandled exception")

        details = str(error)
        message = "Internal server error"
        if looks_like_schema_drift(details):
            message = schema_drift_hint()

        return jsonify({"error": message, "details": details}), 500

    # ------------------------------------------------------------------
    # Startup schema self-check (dev server)
    # ------------------------------------------------------------------
    # `python run.py` sets MORINGA_AUTO_REPAIR so an old local database is
    # repaired automatically on boot. Skipped for tests / alembic commands.
    if os.environ.get("MORINGA_AUTO_REPAIR") == "1" and not app.config.get("TESTING"):
        try:
            from app.schema_doctor import check_and_repair

            if check_and_repair(app, verbose=False):
                print("ℹ schema was out of date — repaired automatically "
                      "(run `python setup_db.py` for full output)")
        except Exception:
            app.logger.exception("Startup schema self-check failed")

    @app.get("/")
    def index():
        return jsonify({
            "message": "My Moringa Daily app"
        })

    return app
