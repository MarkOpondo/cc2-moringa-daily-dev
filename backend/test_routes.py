import pytest
from app import app, db
from app.models import Category, Content


@pytest.fixture
def client():
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # Seed mock data for testing
            cat = Category(name='Technology')
            db.session.add(cat)
            db.session.commit()

            post = Content(
                title='Flask Testing Guide',
                summary='Learning how to test APIs using pytest',
                category_id=cat.id,
            )
            db.session.add(post)
            db.session.commit()

        yield client

        # Teardown database session and tables
        with app.app_context():
            db.session.remove()
            db.drop_all()


# --- CATEGORY TESTS ---


def test_get_categories(client):
    """Test retrieving all categories."""
    response = client.get('/api/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    category_names = [cat['name'] for cat in data]
    assert 'Technology' in category_names


def test_create_category(client):
    """Test creating a new category."""
    payload = {'name': 'Science'}
    response = client.post('/api/categories', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Science'
    assert 'id' in data


def test_create_category_missing_data(client):
    """Test category creation failure on invalid/missing payload."""
    response = client.post('/api/categories', json={})
    assert response.status_code == 400


# --- CONTENT TESTS ---


def test_get_content(client):
    """Test retrieving all content posts."""
    response = client.get('/api/content')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Flask Testing Guide'


def test_get_single_content(client):
    """Test retrieving a single content item by ID."""
    response = client.get('/api/content/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Flask Testing Guide'
    assert data['summary'] == 'Learning how to test APIs using pytest'


def test_get_single_content_not_found(client):
    """Test 404 response for non-existent content ID."""
    response = client.get('/api/content/999')
    assert response.status_code == 404


def test_create_content(client):
    """Test creating a new content post."""
    payload = {
        'title': 'Pytest Fixtures Overview',
        'summary': 'Understanding fixture scopes and test isolation',
        'category_id': 1,
    }
    response = client.post('/api/content', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Pytest Fixtures Overview'
    assert data['category_id'] == 1


def test_update_content(client):
    """Test updating an existing content post."""
    payload = {
        'title': 'Updated Flask Testing Guide',
        'summary': 'Updated description for testing endpoints',
    }
    response = client.put('/api/content/1', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Updated Flask Testing Guide'


def test_delete_content(client):
    """Test deleting a content post."""
    response = client.delete('/api/content/1')
    assert response.status_code == 200

    # Confirm item no longer exists
    get_response = client.get('/api/content/1')
    assert get_response.status_code == 404