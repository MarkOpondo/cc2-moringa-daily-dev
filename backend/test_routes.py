import pytest
from app import app, db
from app.models import Category, Content

@pytest.fixture
def client():
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
                category_id=cat.id
            )
            db.session.add(post)
            db.session.commit()
            
        yield client
        with app.app_context():
            db.drop_all()

def test_get_categories(client):
    response = client.get('/api/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    category_names = [cat['name'] for cat in data]
    assert 'Technology' in category_names

def test_get_content(client):
    response = client.get('/api/content')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Flask Testing Guide'