from sqlalchemy import create_engine, text, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

DATABASE_URL = "postgresql://postgres:36863686@localhost:5432/work_db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    telegram_id = Column(String, nullable=False)

    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    renewal_date = Column(DateTime, nullable=False)
    cost = Column(Float, nullable=False)
    name = Column(String, nullable=False)

    user = relationship("User", back_populates="subscriptions")

def drop_all_tables_with_cascade():
    with engine.connect() as conn:
        # Удаляем все таблицы с каскадом
        conn.execute(text("DROP TABLE IF EXISTS reservations CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS fines CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS loans CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS comments CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS tasks CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS projects CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS books CASCADE;"))
        conn.commit()

#Base.metadata.drop_all(bind=engine)
#drop_all_tables_with_cascade()
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)