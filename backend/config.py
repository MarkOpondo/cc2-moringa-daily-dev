import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    debug=True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/tech_space'


config_by_name = {
    'development' : DevelopmentConfig
}