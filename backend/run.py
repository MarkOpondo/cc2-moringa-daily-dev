import os

from app import create_app
from app.extensions import db


app = create_app("development")


if __name__ == "__main__":
    # create_all is intentionally limited to bootstrapping a local empty
    # database; production schema changes should use Flask-Migrate.
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5001")))
