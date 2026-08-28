from flask import Flask, jsonify

from app.extensions import db, migrate,jwt,bcrypt,cors,ma


from config import DevelopmentConfig

def create_app(config_class=DevelopmentConfig):
    app=Flask(__name__)

    # load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*":{"origins":"*"}})
    ma.init_app(app)

    # Import models
    with app.app_context():
        from app import models

    # Import route Blueprints
    #-------------------Blueprints----------------#
    from app.Routes.auth import auth_bp
    from app.Routes.users import users_bp
    from app.Routes.profile import profiles_bp
    from app.Routes.categories import categories_bp
    from app.Routes.content import content_bp
    from app.Routes.comments import comments_bp
    from app.Routes.interactions import interactions_bp
    from app.Routes.notifications import notifications_bp
    from app.Routes.reports import reports_bp
    from app.Routes.subcriptions import subscriptions_bp
    from app.Routes.comment_reactions import comment_reactions_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(profiles_bp, url_prefix="/api/profiles")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(content_bp, url_prefix="/api/content")
    app.register_blueprint(comments_bp, url_prefix="/api")
    app.register_blueprint(interactions_bp, url_prefix="/api")
    app.register_blueprint(notifications_bp, url_prefix="/api/users/me/notifications")
    app.register_blueprint(subscriptions_bp,url_prefix="/api")
    app.register_blueprint(comment_reactions_bp,url_prefix="/api")
    app.register_blueprint(reports_bp, url_prefix="/api")

    @app.get('/')
    def index():
        return jsonify({"message": "My Moringa Daily app"})

    return app