import hashlib
from fastapi import FastAPI, HTTPException, Depends
import jwt
from pydantic import BaseModel, validator
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, String, Integer, Text, select, delete
from sqlalchemy.orm import declarative_base
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from haystack import Document
from haystack.components.readers import ExtractiveReader
import torch
from models import UserDB, FoodEntryDB

# Use the DATABASE_URL from the environment (injected via Docker Compose)
import os
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy Setup
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()
# Load model directly

tokenizer = AutoTokenizer.from_pretrained("deepset/tinyroberta-squad2")
model = AutoModelForQuestionAnswering.from_pretrained("deepset/tinyroberta-squad2")

# FoodEntry Model (Database Table)
class FoodEntryDB(Base):
    __tablename__ = "food_entries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    food_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    date = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    calories = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

# Pydantic Models
class FoodEntry(BaseModel):
    food_name: str
    category: str
    date: str
    quantity: str
    calories: Optional[str] = None
    notes: Optional[str] = None

class FoodEntryResponse(FoodEntry):
    id: int

class TextRequest(BaseModel):
    question: str
    context: str

class User(BaseModel):
    username: str
    password_hash: str
    email: str
    first_name: str
    last_name: str

# FastAPI App
app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# Define an endpoint for inference
@app.post("/predict/")
async def predict(request: TextRequest):
    docs = [
        Document(content="Python is a popular programming language"),
        Document(content="python ist eine beliebte Programmiersprache"),
    ]

    reader = ExtractiveReader(model="deepset/tinyroberta-squad2")
    reader.warm_up()

    # question = "What is a popular programming language?"
    result = reader.run(query=request.question, documents=docs)
    
    return {"result": result}

@app.post("/food/", response_model=FoodEntryResponse)
async def create_food_entry(entry: FoodEntry, db: AsyncSession = Depends(get_db)):
    food_entry = FoodEntryDB(**entry.dict())
    db.add(food_entry)
    await db.commit()
    await db.refresh(food_entry)
    return food_entry

@app.get("/food/", response_model=List[FoodEntryResponse])
async def list_food_entries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FoodEntryDB))
    return result.scalars().all()

@app.delete("/food/{entry_id}", status_code=204)
async def delete_food_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(FoodEntryDB).where(FoodEntryDB.id == entry_id))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Entry not found")
    await db.commit()

class UserSignIn(BaseModel):
    email: str
    password: str

# signin
@app.post("/signin/")
async def signin(user: UserSignIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserDB).where(UserDB.email == user.email))
    # verify the password hash
    if result.scalars().first().password_hash != hashlib.sha256(user.password.encode()).hexdigest():
        raise HTTPException(status_code=401, detail="Invalid username or password")
    # issue a token
    token = jwt.encode({"email": user.email}, "secret", algorithm="HS256")
    return {"token": token}

@app.post("/signup/")
async def signup(user: User, db: AsyncSession = Depends(get_db)):
    # take the password hash and hash it
    user.password_hash = hashlib.sha256(user.password_hash.encode()).hexdigest()
    user = UserDB(**user.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


