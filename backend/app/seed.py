import sys
import random
from faker import Faker
from app import create_app
from app.extensions import db
from app.models import (User, Profile, Category,Content, Comment, CommentReaction, ContentReaction,
                    Subscription,Wishlist,Share,Notification,ContentReport, content_categories
                    )

def seed_database():
    fake = Faker()

    # Choices dictated by the CheckConstraints
    content_statuses = ['Draft', 'Published', 'Archived']
    content_types = ['Article', 'Video', 'Audio', 'Image']
    reaction_types = ['Like', 'Love', 'Haha', 'Wow', 'Sad', 'Angry']

    print("Initializing seeding process...")

    try: 
        # Clear existing tables child nodes first in exact safety order
        print("Clearing data from all tables")

        db.session.execute(content_categories.delete())
        CommentReaction.query.delete()
        ContentReaction.query.delete()

        Comment.query.delete()
        Content.query.delete()
        Category.query.delete()

        Profile.query.delete()
        User.query.delete()

        db.session.commit()
        print("Existing data cleared successfully.")

        print("Seeding users and profiles...")
        users = []
        for i in range(10):
            role = 'Admin' if i == 0 else 'Member'

            user = User(
                Username=fake.user_name(),
                Email=fake.unique.email(),
                Role=role,
                IsActive=True
            )

            user.password_hash = "password12345"

            profile = Profile(
                Bio=fake.paragraph(nb_sentences=3),
                ProfileImage=fake.image_url(width=200, height=200),
                Interests=", ".join(fake.words(nb=5))
            )

            user.profile = profile

            db.session.add(user)
            users.append(user)

        # Flush to generate database IDs for next steps
        db.session.flush()

        print("Seeding content categories...")

        categories = []
        predefined_categories = ["Tech", "Health", "Lifestyle", "Finance", "Gaming"]

        for name in predefined_categories:
            category = Category(
                Name = name,
                Description = fake.sentence(),
                CreatedBy = random.choice(users).UserID
            )

            db.session.add(category)
            categories.append(category)

        db.session.flush()

        # 5. Create Seed Content (with category links)
        print("📦 Seeding 15 content items...")
        contents = []
        for _ in range(15):
            content_item = Content(
                UserID=random.choice(users).UserID,
                Title=fake.sentence(nb_words=6),
                Description=fake.text(max_nb_chars=500),
                ContentType=random.choice(content_types),
                ContentURL=fake.url(),
                Status=random.choice(content_statuses),
                IsApproved=random.choice([True, False])
            )
            
            # Assign 1 to 2 random tags using the many-to-many relationship
            assigned_categories = random.sample(categories, k=random.randint(1, 2))
            content_item.categories.extend(assigned_categories)
            
            db.session.add(content_item)
            contents.append(content_item)

        db.session.flush()

        # 6. Create Seed Comments & Top-level Replies
        print("💬 Seeding comments and nested replies...")
        comments = []
        for _ in range(25):
            comment = Comment(
                UserID=random.choice(users).UserID,
                ContentID=random.choice(contents).ContentID,
                Text=fake.sentence()
            )
            db.session.add(comment)
            comments.append(comment)
            
        db.session.flush()

        # Generate nested child comment replies (self-referencing check)
        for _ in range(10):
            parent = random.choice(comments)
            reply = Comment(
                UserID=random.choice(users).UserID,
                ContentID=parent.ContentID,
                ParentCommentID=parent.CommentID,  # Threaded reply link
                Text=fake.sentence()
            )
            db.session.add(reply)

        db.session.flush()

        # 7. Create Reactions (respecting unique constraints)
        print("👍 Seeding safe Unique Reactions...")
        
        # Content Reactions
        unique_content_likes = set()
        while len(unique_content_likes) < 30:
            u_id = random.choice(users).UserID
            c_id = random.choice(contents).ContentID
            
            if (u_id, c_id) not in unique_content_likes:
                unique_content_likes.add((u_id, c_id))
                rxn = ContentReaction(
                    UserID=u_id,
                    ContentID=c_id,
                    Reaction=random.choice(reaction_types)
                )
                db.session.add(rxn)

        # Comment Reactions
        unique_comment_likes = set()
        while len(unique_comment_likes) < 20:
            u_id = random.choice(users).UserID
            m_id = random.choice(comments).CommentID
            
            if (u_id, m_id) not in unique_comment_likes:
                unique_comment_likes.add((u_id, m_id))
                rxn = CommentReaction(
                    UserID=u_id,
                    CommentID=m_id,
                    Reaction=random.choice(reaction_types)
                )
                db.session.add(rxn)

        # Final Database Save
        db.session.commit()
        print("🎉 Database successfully seeded with safe sample structures!")

    except Exception as e:
        print(f"❌ Error occurred during execution: {e}")
        db.session.rollback()
        sys.exit(1)