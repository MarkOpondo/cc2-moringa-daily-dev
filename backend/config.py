import os

class Config:
    SECRET_KEY=os.environ.get(
        "SECRET_KEY",
         "dev-secret-key-change-in-production"
    )

    JWT_SECRET_KEY=os.environ.get(
        "JWT_SECRET_KEY", 
        "jwt-secret-change-me"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    debug=True
     SQLALCHEMY_DATABASE_URI=os.environ.get(
        'DATABASE_URL',
        "postgresql://postgres:postgres@localhost:5432/tech-space"
    )

config_by_name = {
    'development' : DevelopmentConfig
}