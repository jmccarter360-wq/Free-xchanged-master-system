"""
Database initialization script
Creates all database tables and optionally seeds with sample data
"""
from database import Base, engine, SessionLocal
from models import Ambassador, Customer, Group, QRCode, CashbackBalance
import argparse


def init_db():
    """Initialize the database by creating all tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def seed_db():
    """Seed the database with sample data"""
    print("Seeding database with sample data...")
    
    db = SessionLocal()
    try:
        # Create groups
        group1 = Group(name="Gold Ambassadors")
        group2 = Group(name="Silver Ambassadors")
        db.add_all([group1, group2])
        db.commit()
        db.refresh(group1)
        db.refresh(group2)
        
        # Create ambassadors
        ambassador1 = Ambassador(
            name="John Ambassador",
            email="john.ambassador@example.com",
            group_id=group1.id
        )
        ambassador2 = Ambassador(
            name="Jane Ambassador",
            email="jane.ambassador@example.com",
            group_id=group1.id
        )
        db.add_all([ambassador1, ambassador2])
        db.commit()
        db.refresh(ambassador1)
        db.refresh(ambassador2)
        
        # Create QR codes
        qr1 = QRCode(code="QR-JOHN-001", ambassador_id=ambassador1.id)
        qr2 = QRCode(code="QR-JANE-001", ambassador_id=ambassador2.id)
        db.add_all([qr1, qr2])
        
        # Create customers
        customer1 = Customer(name="Alice Customer", email="alice@example.com")
        customer2 = Customer(name="Bob Customer", email="bob@example.com")
        customer3 = Customer(name="Charlie Customer", email="charlie@example.com")
        db.add_all([customer1, customer2, customer3])
        db.commit()
        db.refresh(customer1)
        db.refresh(customer2)
        db.refresh(customer3)
        
        # Create cashback balances
        balance1 = CashbackBalance(customer_id=customer1.id, balance=0)
        balance2 = CashbackBalance(customer_id=customer2.id, balance=0)
        balance3 = CashbackBalance(customer_id=customer3.id, balance=0)
        db.add_all([balance1, balance2, balance3])
        
        db.commit()
        print("Database seeded successfully!")
        print(f"Created {len(db.query(Group).all())} groups")
        print(f"Created {len(db.query(Ambassador).all())} ambassadors")
        print(f"Created {len(db.query(Customer).all())} customers")
        print(f"Created {len(db.query(QRCode).all())} QR codes")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


def reset_db():
    """Reset the database by dropping and recreating all tables"""
    print("Resetting database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database reset successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database management script")
    parser.add_argument(
        "command",
        choices=["init", "seed", "reset"],
        help="Command to execute: init (create tables), seed (add sample data), reset (drop and recreate)"
    )
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_db()
    elif args.command == "seed":
        init_db()
        seed_db()
    elif args.command == "reset":
        reset_db()
