from app import create_app
from app.extensions import db
from app.seed import seed_database

app = create_app(config_class="development")

if __name__ == "__main__":
    app.run(debug=True, port=5001)