import os

from app import create_app

# FLASK_ENV=production on Render/Heroku-style hosts; defaults to development
config_name = os.environ.get("FLASK_ENV", "development")

# create_app supports both config_class and config_name
app = create_app(config_name=config_name)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=(config_name != "production"),
        port=5001
    )