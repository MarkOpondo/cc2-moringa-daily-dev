from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db=SQLAlchemy(metadata=metadata)
jwt=JWTManager()
migrate=Migrate()
cors=CORS()
bcrypt=Bcrypt()
ma=Marshmallow()
