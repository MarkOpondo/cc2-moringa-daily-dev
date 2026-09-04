import pytest

from app import create_app
from app.extensions import db
from app.models import Category, Profile, User


@pytest.fixture
def client():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        category = Category(Name="Backend", Description="Backend engineering")
        db.session.add(category)
        db.session.commit()

    with app.test_client() as test_client:
        yield test_client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def register(client, username, email, password="password123"):
    response = client.post(
        "/api/auth/register",
        json={"username": username, "email": email, "password": password},
    )
    assert response.status_code == 201
    return response.get_json()["token"]


def login(client, identifier, password="password123"):
    response = client.post(
        "/api/auth/login",
        json={"identifier": identifier, "password": password},
    )
    assert response.status_code == 200
    return response.get_json()["token"]


def headers(token):
    return {"Authorization": f"Bearer {token}"}


def make_admin(client):
    with client.application.app_context():
        admin = User(
            Username="admin",
            Email="admin@example.com",
            Role="admin",
            IsActive=True,
        )
        admin.password_hash = "password123"
        db.session.add(admin)
        db.session.flush()
        db.session.add(Profile(UserID=admin.UserID))
        db.session.commit()
    return login(client, "admin")


def test_auth_and_profile(client):
    token = register(client, "alice", "alice@example.com")

    response = client.get("/api/auth/me", headers=headers(token))
    assert response.status_code == 200
    assert response.get_json()["username"] == "alice"

    response = client.get("/api/profiles/me", headers=headers(token))
    assert response.status_code == 200
    assert response.get_json()["user"]["username"] == "alice"

    response = client.put(
        "/api/profiles/me",
        headers=headers(token),
        json={"bio": "Backend developer", "skills": "Python", "githubUrl": "https://github.com/alice"},
    )
    assert response.status_code == 200
    assert response.get_json()["skills"] == "Python"
    assert response.get_json()["githubUrl"] == "https://github.com/alice"


def test_content_lifecycle_and_interactions(client):
    author_token = register(client, "alice", "alice@example.com")
    subscriber_token = register(client, "bob", "bob@example.com")
    admin_token = make_admin(client)

    category_id = client.get("/api/categories").get_json()[0]["id"]
    response = client.post(
        "/api/subscriptions",
        headers=headers(subscriber_token),
        json={"categoryId": category_id},
    )
    assert response.status_code == 201

    response = client.post(
        "/api/content",
        headers=headers(author_token),
        json={
            "title": "Testing Flask APIs",
            "body": "A practical guide to API tests.",
            "type": "article",
            "categoryId": category_id,
        },
    )
    assert response.status_code == 201
    content = response.get_json()
    assert content["status"] == "draft"
    content_id = content["id"]

    # Drafts are private until moderation approves them.
    assert client.get("/api/content").get_json() == []
    assert client.get(f"/api/content/{content_id}", headers=headers(author_token)).status_code == 200

    response = client.patch(
        f"/api/admin/content/{content_id}/status",
        headers=headers(admin_token),
        json={"status": "published"},
    )
    assert response.status_code == 200
    assert response.get_json()["status"] == "published"
    assert client.get("/api/content").get_json()[0]["id"] == content_id

    response = client.post(
        f"/api/content/{content_id}/reactions",
        headers=headers(author_token),
        json={"type": "like"},
    )
    assert response.status_code == 200
    assert response.get_json()["likes"] == 1
    assert client.get(f"/api/content/{content_id}/reactions").get_json()["likes"] == 1

    response = client.post(
        f"/api/content/{content_id}/comments",
        headers=headers(author_token),
        json={"body": "Helpful article"},
    )
    assert response.status_code == 201
    comment_id = response.get_json()["id"]
    assert client.get(f"/api/content/{content_id}/comments").get_json()[0]["body"] == "Helpful article"

    response = client.patch(
        f"/api/comments/{comment_id}",
        headers=headers(author_token),
        json={"body": "Updated comment"},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/wishlist",
        headers=headers(author_token),
        json={"contentId": content_id},
    )
    assert response.status_code == 201
    assert client.get("/api/wishlist", headers=headers(author_token)).get_json()[0]["id"] == content_id
    assert client.delete(f"/api/wishlist/{content_id}", headers=headers(author_token)).status_code == 200

    response = client.post(
        f"/api/content/{content_id}/report",
        headers=headers(author_token),
        json={"reason": "This is a test report"},
    )
    assert response.status_code == 201
    assert client.get("/api/admin/reports", headers=headers(admin_token)).status_code == 200

    response = client.patch(
        f"/api/admin/reports/{response.get_json()['id']}",
        headers=headers(admin_token),
    )
    assert response.status_code == 200
    assert response.get_json()["status"] == "resolved"

    notifications = client.get("/api/notifications", headers=headers(subscriber_token))
    assert notifications.status_code == 200
    assert len(notifications.get_json()) == 1


def test_admin_and_subscription_authorization(client):
    user_token = register(client, "alice", "alice@example.com")
    category_id = client.get("/api/categories").get_json()[0]["id"]

    assert client.get("/api/admin/users", headers=headers(user_token)).status_code == 403
    assert client.post(
        "/api/subscriptions",
        headers=headers(user_token),
        json={"categoryId": category_id},
    ).status_code == 201
    assert client.get("/api/subscriptions", headers=headers(user_token)).get_json()[0]["categoryId"] == category_id
    assert client.delete(
        f"/api/subscriptions/{category_id}", headers=headers(user_token)
    ).status_code == 200
