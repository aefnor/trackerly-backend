import hashlib
from fastapi import FastAPI, HTTPException, Depends
import jwt
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, String, Integer, Text, select, delete
from sqlalchemy.orm import declarative_base
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from haystack import Document
from haystack.components.readers import ExtractiveReader
from backend.models import UserDB, FoodEntryDB
import json

# Use the DATABASE_URL from the environment (injected via Docker Compose)
import os
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "postgresql+asyncpg://fooduser:foodpass@localhost:5432/foodtracker"

print(DATABASE_URL)
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

class User(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    password_hash: str = Field(default=None, exclude=True)

    @property
    def hashed_password(self):
        return hashlib.sha256(self.password.encode()).hexdigest()

    class Config:
        orm_mode = True

# Define the nested models
class FoodNutrientSource(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    description: Optional[str] = None


class FoodNutrientDerivation(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    foodNutrientSource: Optional[FoodNutrientSource] = None


class Nutrient(BaseModel):
    id: int
    number: str
    name: str
    rank: int
    unitName: str


class FoodNutrient(BaseModel):
    type: Optional[str] = None
    id: Optional[int] = None
    nutrient: Optional[Nutrient] = None
    dataPoints: Optional[int] = None # Make this field optional
    foodNutrientDerivation: Optional[FoodNutrientDerivation] = None
    median: Optional[float] = None     # Make this field optional
    amount: Optional[float] = None
    max: Optional[float] = None        # Make this field optional
    min: Optional[float] = None         # Make this field optional


class FoundationFood(BaseModel):
    foodClass: str
    description: str
    foodNutrients: List[FoodNutrient]


class FoodData(BaseModel):
    FoundationFoods: List[FoundationFood]

# FastAPI App
app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# Define the Request Model
class TextRequest(BaseModel):
    question: str

# we need to index the foundationDownload.json data
with open('foundationDownload.json') as f:
    print("data found")
    print(f)
    data = json.load(f)
documents = []  # list to hold the indexed documents
# Function to print parsed data
# def print_food_data(data):
#     print(FoodData(**data))
#     for food in data.get("FoundationFoods", []):
#         # print(f"Food Class: {food.get('foodClass')}")
#         documents.append(Document(content=str(food.get('foodClass')))) # adding the indexed document to documents list
#         # print(f"Description: {food.get('description')}")
        
#         # for nutrient in food.get("foodNutrients", []):
#             # nutrient_info = nutrient.get("nutrient", {})
#             # print(f"  Nutrient Name: {nutrient_info.get('name')}")
#             # print(f"  Nutrient ID: {nutrient_info.get('id')}")
#             # print(f"  Amount: {nutrient.get('amount')} {nutrient_info.get('unitName')}")
#             # print(f"  Median: {nutrient.get('median')} {nutrient_info.get('unitName')}")
#             # print(f"  Data Points: {nutrient.get('dataPoints')}")
#             # derivation = nutrient.get("foodNutrientDerivation", {})
#             # print(f"    Source Code: {derivation.get('code')}")
#             # print(f"    Source Description: {derivation.get('description')}")
#             # food_source = derivation.get("foodNutrientSource", {})
#             # print(f"      Source ID: {food_source.get('id')}")
#             # print(f"      Source Description: {food_source.get('description')}")
#             # # add it to documents
for foundation_food in FoodData(**data).FoundationFoods:
    # Convert FoundationFood object to string content for indexing
    food_class_content = foundation_food.foodClass
    food_description_content = foundation_food.description
    nutrients_content = ", ".join(
        f"{nutrient.nutrient.name} ({nutrient.nutrient.unitName}): {nutrient.amount}" for nutrient in foundation_food.foodNutrients if nutrient.amount is not None
    )
    
    # Create a content string that includes the foodClass, description, and nutrient details
    content = f"Class: {food_class_content}, Description: {food_description_content}, Nutrients: {nutrients_content}"
    
    # Append as Document to documents list
    documents.append(Document(content=content))

# Call the function to print the data
# print_food_data(data)
# for i, record in enumerate(data): # directly iterate over records and create index from 0 automatically
#     if not isinstance(record, dict): # if a record isn't dictionary then skip it
#         print(f"Skipping invalid data at position {i}: {record}")
#         continue
#     flat_dict = {} # create a flat dictionary for each record
#     for key, value in record.items():
#         # process 'foodClass' and 'description' directly without prefixing them with 'food_' 
#         if key in ('foodClass', 'description'):
#             flat_dict[key] = str(value)  
#             continue
#         elif isinstance(value, dict): # if value is a dictionary then add its content to our flat dictionary  
#             for subkey, subvalue in value.items():
#                 # adding prefix 'food_' for clarity 
#                 flat_dict['food_'+subkey] = str(subvalue)
#         elif isinstance(value, list): # for handling the nested foodNutrients
#             for j, nutrient in enumerate(value): # iterate over each foodNutrient and create a new key-value pair for it
#                 if not isinstance(nutrient, dict): continue  # if a nutrient isn't dictionary then skip it
#                 for subkey, subvalue in nutrient.items():
#                     flat_dict['foodNutrients'+str(j)+'_'+subkey] = str(subvalue) # adding prefix for clarity and suffix with index of the nutrient
#         else:
#             flat_dict[key] = value  # add other key-values to our flat dictionary without converting it into a string
#     document = Document(content=str(flat_dict), id=i) # create a document with the flat dictionary and assign index as its id
#     documents.append(document) 

print(len(documents))
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
    result = reader.run(query=request.question, documents=documents)
    
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
    print(user)
    user_data = user.dict(exclude={"password"})
    user_data["password_hash"] = hashlib.sha256(user.password.encode()).hexdigest()
    user_db = UserDB(**user_data)
    db.add(user_db)
    await db.commit()
    await db.refresh(user_db)
    return user_db


