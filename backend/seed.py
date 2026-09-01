from app import create_app, db
from app.models import Category

app = create_app()

def seed_categories_only():
    with app.app_context():
        print("📂 Seeding core navigation categories from Figma...")

        # Only seed the structural categories required for the sidebar navigation
        category_names = ["DevOps", "Fullstack", "Frontend", "Backend", "Mobile", "Career", "AI/ML"]
        
        for name in category_names:
            existing = Category.query.filter_by(Name=name).first()
            if not existing:
                cat = Category(
                    Name=name, 
                    Description=f"Discussions and resources for {name}"
                )
                db.session.add(cat)
        
        db.session.commit()
        print("✅ Categories seeded! The posts feed remains 100% empty, waiting for your real data.")

if __name__ == '__main__':
    seed_categories_only()