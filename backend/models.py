import hashlib
from pydantic import validator
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class FoodEntryDB(Base):
    __tablename__ = "food_entries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    food_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    date = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    calories = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
