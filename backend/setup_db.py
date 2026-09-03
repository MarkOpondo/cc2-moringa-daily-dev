"""Safe database setup & repair — works for fresh clones AND old databases.

Why this exists
---------------
Databases created from the previous models are missing columns the code now
uses (content.Summary / Duration / LikesCount / RejectionReason, users.is_admin)
and their `content` status check-constraint doesn't allow 'Pending', which made
every new learner post fail with a 500. Plain `flask db upgrade` can't fix an
unstamped (create_all-created) database, so this script repairs the schema
directly:

  1. missing tables        -> created
  2. missing columns       -> ALTER TABLE ... ADD COLUMN (any engine)
  3. old status constraint -> content table rebuilt with the 'Pending'
                              constraint (SQLite) / constraint swapped (Postgres)

Everything is idempotent — run it as many times as you like. Existing data is
preserved. On first run with an empty database it also seeds default categories
and an admin account.

Run from the backend/ folder:  python setup_db.py
"""
import os

from flask_migrate import stamp, upgrade
from sqlalchemy import CheckConstraint, MetaData, Table, text

from app import create_app
from app.extensions import db
from app.models import Category, Content, Profile, User

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

PENDING_STATUS_CONSTRAINT = (
    "\"Status\" IN ('Draft', 'Pending', 'Published', 'Archived')"
)


def _table_names(engine):
    return set(db.inspect(engine).get_table_names())


def _has_alembic_version(engine):
    return "alembic_version" in _table_names(engine)


def add_missing_columns(engine):
    """ALTER TABLE ... ADD COLUMN for every model column the DB is missing."""
    inspector = db.inspect(engine)
    existing_tables = set(inspector.get_table_names())
    preparer = engine.dialect.identifier_preparer
    added = []

    for table in db.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue  # brand-new tables are handled by create_all
        existing_cols = {c["name"] for c in inspector.get_columns(table.name)}

        for col in table.columns:
            if col.name in existing_cols:
                continue
            col_type = col.type.compile(engine.dialect)
            quoted = f"{preparer.quote(table.name)}.{preparer.quote(col.name)}"
            with engine.begin() as conn:
                conn.execute(text(
                    f"ALTER TABLE {preparer.quote(table.name)} "
                    f"ADD COLUMN {preparer.quote(col.name)} {col_type}"
                ))
            added.append(quoted)

    return added


def _rebuild_content_table_sqlite(engine):
    """Recreate `content` from the model definition (adds the 'Pending'
    status constraint) while copying all existing rows.

    Used when the old table's CHECK constraint doesn't allow 'Pending' —
    SQLite can't alter constraints in place, so the table is rebuilt.
    """
    import sqlite3

    from sqlalchemy.schema import CreateTable

    inspector = db.inspect(engine)
    old_cols = {c["name"] for c in inspector.get_columns("content")}

    # A copy of the model's content table under a temporary name
    scratch = MetaData(naming_convention=db.metadata.naming_convention)
    new_table = Table("content_rebuild", scratch)
    for col in Content.__table__.columns:
        new_table.append_column(col._copy())
    for constraint in Content.__table__.constraints:
        if isinstance(constraint, CheckConstraint):
            new_table.append_constraint(constraint._copy())

    preparer = engine.dialect.identifier_preparer
    common = [c.name for c in new_table.columns if c.name in old_cols]
    common_quoted = ", ".join(preparer.quote(c) for c in common)

    create_ddl = str(CreateTable(new_table).compile(engine))
    insert_sql = (
        f"INSERT INTO content_rebuild ({common_quoted}) "
        f"SELECT {common_quoted} FROM content"
    )

    # Release pooled connections so nothing holds the old schema mid-rebuild
    engine.dispose()

    # Raw sqlite3 connection in autocommit mode: PRAGMAs take effect
    # immediately (they are no-ops inside a transaction) and we control
    # the transaction boundaries explicitly.
    conn = sqlite3.connect(engine.url.database)
    try:
        conn.isolation_level = None
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys=OFF")
        cur.execute("PRAGMA legacy_alter_table=ON")
        cur.execute("BEGIN")
        cur.execute(create_ddl)
        cur.execute(insert_sql)
        cur.execute("DROP TABLE content")
        cur.execute("ALTER TABLE content_rebuild RENAME TO content")
        cur.execute("COMMIT")
        cur.execute("PRAGMA legacy_alter_table=OFF")
        cur.execute("PRAGMA foreign_keys=ON")

        issues = cur.execute("PRAGMA foreign_key_check").fetchall()
        if issues:
            print(f"⚠ foreign_key_check reported {len(issues)} issue(s) — "
                  "review them before deploying.")
        cur.close()
    finally:
        conn.close()


def fix_content_status_constraint(engine):
    """Make sure the content status constraint allows 'Pending'."""
    if engine.dialect.name == "sqlite":
        with engine.connect() as conn:
            ddl = conn.execute(text(
                "SELECT sql FROM sqlite_master "
                "WHERE type='table' AND name='content'"
            )).scalar()
        if ddl and "Pending" not in ddl:
            _rebuild_content_table_sqlite(engine)
            return True
        return False

    # Postgres & friends: swap the constraint directly (best effort)
    try:
        with engine.begin() as conn:
            conn.execute(text(
                "ALTER TABLE content DROP CONSTRAINT IF EXISTS check_valid_content_status"
            ))
            conn.execute(text(
                f"ALTER TABLE content ADD CONSTRAINT check_valid_content_status "
                f"CHECK ({PENDING_STATUS_CONSTRAINT})"
            ))
        return True
    except Exception as exc:  # pragma: no cover
        print(f"⚠ could not update the status constraint: {exc}")
        return False


def repair_schema(engine):
    """Bring an existing database up to the current model schema."""
    print("→ Repairing schema (idempotent)…")
    db.create_all()  # adds any missing tables, never touches existing ones

    added = add_missing_columns(engine)
    for col in added:
        print(f"  ✓ added missing column {col}")

    if fix_content_status_constraint(engine):
        print("  ✓ content status constraint now allows 'Pending'")

    if not added:
        print("  ✓ schema already up to date.")


def main():
    app = create_app("development")

    with app.app_context():
        engine = db.engine

        if len(_table_names(engine)) == 0:
            print("→ No database found — creating tables from models…")
            db.create_all()
            stamp(revision="head")
            print("✓ Database created and stamped at the latest migration.")
        else:
            if _has_alembic_version(engine):
                print("→ Existing database — applying pending migrations…")
                try:
                    upgrade()
                    print("✓ Migrations up to date.")
                except Exception as exc:
                    print(f"⚠ migration step failed ({exc}) — "
                          "falling back to schema repair…")
            else:
                print("→ Existing database (no migration history) — "
                      "repairing schema directly…")

            repair_schema(engine)

            with app.app_context():
                stamp(revision="head")

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
