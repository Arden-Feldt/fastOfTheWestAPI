from app.db.database import SessionLocal, engine, Base
from app.models import User, Item, Order

# Vibe Coded:

def seed_database():
    # 1. Create tables if they don't exist
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 2. Check if we already have data (to avoid duplicates)
        if db.query(User).first():
            print("Database already seeded. Skipping...")
            return

        print("Seeding data...")
        
        # 3. Create Users
        frodo = User(name="Frodo", password="password")
        galadriel = User(name="Galadriel", password="password")
        db.add_all([frodo, galadriel])
        db.flush()  # Flushes to DB to get IDs without committing yet

        # 4. Create Items
        ring = Item(name="ring", cost=10)
        sting = Item(name="sting", cost=15)
        palantir = Item(name="palantir", cost=25)
        db.add_all([ring, sting, palantir])
        db.flush()

        # 5. Create Orders (Using the IDs from flushed objects)
        orders = [
            Order(user_id=frodo.id, item_id=ring.id),
            Order(user_id=frodo.id, item_id=sting.id),
            Order(user_id=galadriel.id, item_id=palantir.id),
        ]
        db.add_all(orders)

        # 6. Final Commit
        db.commit()
        print("Seeding complete!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()