from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy import MetaData
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

metadata = MetaData(naming_convention={
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from .Routes.routes import bp
    app.register_blueprint(bp, url_prefix='/api')

    @app.get('/')
    def index():
        return jsonify({"message": "My Moringa Daily app"})

    return app