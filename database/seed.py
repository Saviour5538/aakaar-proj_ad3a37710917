import uuid
from datetime import datetime, timedelta
from database.models import Base, engine, SessionLocal, User, Task, TokenBlacklist

def seed_database():
    session = SessionLocal()
    try:
        # Clear existing data
        session.query(Task).delete()
        session.query(User).delete()
        session.query(TokenBlacklist).delete()
        session.commit()

        # Insert sample users
        user1 = User(
            id=uuid.uuid4(),
            email="alice@example.com",
            password_hash="hashed_password_1",
            created_at=datetime.utcnow()
        )
        user2 = User(
            id=uuid.uuid4(),
            email="bob@example.com",
            password_hash="hashed_password_2",
            created_at=datetime.utcnow()
        )
        session.add_all([user1, user2])
        session.commit()

        # Insert sample tasks
        task1 = Task(
            id=uuid.uuid4(),
            user_id=user1.id,
            title="Buy groceries",
            description="Milk, eggs, bread",
            completed=False,
            created_at=datetime.utcnow()
        )
        task2 = Task(
            id=uuid.uuid4(),
            user_id=user2.id,
            title="Read a book",
            description="Finish reading '1984'",
            completed=False,
            created_at=datetime.utcnow()
        )
        session.add_all([task1, task2])
        session.commit()

        # Insert sample token blacklist entries
        token1 = TokenBlacklist(
            id=uuid.uuid4(),
            token="sample_token_1",
            expires_at=datetime.utcnow() + timedelta(days=1),
            created_at=datetime.utcnow()
        )
        token2 = TokenBlacklist(
            id=uuid.uuid4(),
            token="sample_token_2",
            expires_at=datetime.utcnow() + timedelta(days=1),
            created_at=datetime.utcnow()
        )
        session.add_all([token1, token2])
        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_database()