from flask_sqlalchemy import SQLALchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt

db=SQLALchemy()
jwt=JWTManager()
migrate=Migrate()
cors=CORS()
bcrypt=Bcrypt()
