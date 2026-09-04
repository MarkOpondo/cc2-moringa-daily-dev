import os

from flask_migrate import upgrade

from app import create_app


app = create_app("development")


if __name__ == "__main__":
    # Keep a local development database in sync before serving requests.
    # Production deployments should run `flask db upgrade` as a release step.
    with app.app_context():
        upgrade(directory=os.path.join(os.path.dirname(__file__), "migrations"))
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5001")))
