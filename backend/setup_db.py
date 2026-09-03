"""Safe database setup — works for fresh clones AND existing databases.

- Fresh / missing DB        -> creates all tables from the models, then
                              stamps alembic to the latest migration head.
- Existing DB, alembic run  -> applies any pending migrations.
- Existing DB, never stamped (created with db.create_all before)
                             -> stamps head first, then upgrades.

Also seeds default categories + an admin account the very first time
(only when the users table is completely empty), so you can log in
immediately instead of hunting for credentials.

Run from the backend/ folder:  python setup_db.py
"""
import os

from flask_migrate import stamp, upgrade

from app import create_app
from app.extensions import db
from app.models import Category, Profile, User

DEFAULT_CATEGORIES = [
    "Software Engineering",
    "Data Science",
    "Cybersecurity",
    "DevOps",
    "Fullstack",
    "Frontend",
    "Backend",
    "Mobile",
    "Career",
    "AI/ML",
]

ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@moringa.com"
ADMIN_PASSWORD = "Admin123!"


def database_is_empty(app):
    with app.app_context():
        inspector = db.inspect(db.engine)
        return len(inspector.get_table_names()) == 0


def has_alembic_version(app):
    with app.app_context():
        inspector = db.inspect(db.engine)
        return "alembic_version" in inspector.get_table_names()


def main():
    app = create_app("development")

    if database_is_empty(app):
        print("→ No database found — creating tables from models…")
        with app.app_context():
            db.create_all()
            stamp(revision="head")
        print("✓ Database created and stamped at the latest migration.")
    elif not has_alembic_version(app):
        print("→ Database exists but was never migrated — stamping head…")
        with app.app_context():
            stamp(revision="head")
        print("✓ Stamped. Applying any pending migrations…")
        with app.app_context():
            upgrade()
    else:
        print("→ Existing database — applying pending migrations…")
        with app.app_context():
            upgrade()
        print("✓ Migrations up to date.")

    # ---- First-run seed: categories + admin ----
    with app.app_context():
        seeded = False

        if Category.query.count() == 0:
            for name in DEFAULT_CATEGORIES:
                db.session.add(Category(Name=name, Description=f"{name} content"))
            db.session.commit()
            print(f"✓ Seeded {len(DEFAULT_CATEGORIES)} default categories.")
            seeded = True

        if User.query.count() == 0:
            admin = User(
                Username=ADMIN_USERNAME,
                Email=ADMIN_EMAIL,
                Role="Admin",
                IsActive=True,
                is_admin=True,
            )
            admin.password_hash = ADMIN_PASSWORD
            db.session.add(admin)
            db.session.flush()  # assigns admin.UserID
            db.session.add(Profile(UserID=admin.UserID))
            db.session.commit()
            print("✓ Seeded default admin account:")
            print(f"    username: {ADMIN_USERNAME}")
            print(f"    password: {ADMIN_PASSWORD}")
            seeded = True

        if not seeded:
            print("✓ Data already present — nothing to seed.")


if __name__ == "__main__":
    main()
