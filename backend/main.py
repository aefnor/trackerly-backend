import hashlib
from backend import schema
from fastapi import FastAPI, HTTPException, Depends
import jwt
from sqlalchemy.ext.asyncio.session import (
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import select
from sqlalchemy.orm import declarative_base
from backend.models import User
import datetime
from backend.food import analyze_food_query
from typing import AsyncGenerator
from fastapi.middleware.cors import CORSMiddleware


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

# FastAPI App
app = FastAPI()

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; adjust in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


# signin
@app.post("/signin/")
async def signin(user: schema.UserSignIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    if getattr(db_user, "password_hash") != hashed_password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = jwt.encode(
        {
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        },
        "secret",
        algorithm="HS256",
    )

    return {"token": token}


@app.post("/signup/")
async def signup(user: schema.User, db: AsyncSession = Depends(get_db)):
    print(user)
    user_data = user.dict(exclude={"password"})
    user_data["password_hash"] = hashlib.sha256(user.password.encode()).hexdigest()
    user_db = User(**user_data)
    db.add(user_db)
    await db.commit()
    await db.refresh(user_db)
    return user_db


@app.post("/forgot-password/")
async def forgot_password(
    user: schema.UserForgotPassword, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == user.email))
    user_db = result.scalars().first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    # issue a token
    token = jwt.encode(
        {
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        },
        "secret",
        algorithm="HS256",
    )
    return {"token": token}


# check if user token is valid
@app.get("/check-user-token-valid/{token}")
async def check_user_token_valid(token: str):
    try:
        decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
        print(decoded_token)
        # check if token is expired
        if (
            datetime.datetime.utcfromtimestamp(decoded_token["exp"])
            < datetime.datetime.utcnow()
        ):
            raise HTTPException(status_code=401, detail="Token has expired")

        return {
            "valid": True,
            "email": jwt.decode(token, "secret", algorithms=["HS256"])["email"],
        }
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        print("Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print("Token validation failed")
        raise HTTPException(status_code=401, detail="Token validation failed")


@app.post("/analyze-food-sentence/")
async def analyze_food_sentence(request: schema.TextRequest):
    food_name_list_response = analyze_food_query(
        request.sentence
    )  # ['turkey sandwich']
    if True:
        return {
            "result": "success",
            "food_name_list_response": {
                "food_name": "Grilled Chicken Salad",
                "portion_size": {"amount": 250, "unit": "grams"},
                "calories_per_portion": 350,
                "macronutrients": {"carbohydrates": 20, "proteins": 30, "fats": 10},
                "micronutrients": {
                    "vitamin_a": "500 IU",
                    "vitamin_c": "20 mg",
                    "iron": "2 mg",
                },
                "fiber_content": "5 g",
                "sugar": {"added": "2 g", "natural": "5 g"},
                "cholesterol": "70 mg",
                "sodium": "400 mg",
                "fats": {"saturated_fats": "2 g", "trans_fats": "0 g"},
                "common_allergens": ["dairy", "nuts"],
                "dietary_tags": ["low-carb", "keto", "gluten-free"],
                "custom_recipes": [
                    {
                        "name": "Chicken Caesar Salad",
                        "calories": 450,
                        "macronutrients": {
                            "carbohydrates": 15,
                            "proteins": 35,
                            "fats": 20,
                        },
                    }
                ],
                "favorite_foods": ["Grilled Chicken", "Quinoa Bowl", "Smoothies"],
                "user_notes": "Had this for lunch after workout",
                "meal_type": "lunch",
                "time_and_date": "2024-12-08T12:30:00Z",
                "location": "Home",
                "barcode_scanner": "0123456789012",
                "photo_upload": "base64_encoded_image_string",
                "ingredient_breakdown": [
                    {"ingredient": "Chicken Breast", "quantity": "150g"},
                    {"ingredient": "Lettuce", "quantity": "50g"},
                    {"ingredient": "Dressing", "quantity": "50g"},
                ],
                "historical_data": [
                    {"date": "2024-12-01", "calories": 2000},
                    {"date": "2024-12-02", "calories": 2200},
                ],
                "ai_recommendations": [
                    "Add avocado for healthy fats",
                    "Try quinoa for variety",
                ],
                "wearables_integration": {
                    "fitness_tracker": "Fitbit",
                    "heart_rate": "85 bpm",
                },
                "grocery_list": ["Chicken Breast", "Lettuce", "Dressing"],
                "api_support": ["USDA Food Database", "MyFitnessPal API"],
                "hydration_tracking": {"water_intake": "2.5 liters"},
                "energy_level_correlation": {
                    "energy_level": "High",
                    "time_after_meal": "2 hours",
                },
                "symptoms_tracking": {
                    "GI_issues": "None",
                    "mood_changes": "Feeling energetic",
                },
                "sharing_options": {"recipes": True, "logs": False},
                "progress_sharing": ["Facebook", "Instagram"],
                "streaks_and_achievements": {
                    "streak_days": 7,
                    "achievements": ["Logged meals for 7 days in a row"],
                },
                "daily_goals": {
                    "calories": 2000,
                    "macronutrients": {"carbs": 250, "proteins": 150, "fats": 70},
                },
                "graphs_and_charts": {
                    "trends": {
                        "calories": [2000, 2200, 2100],
                        "macronutrients": [
                            {
                                "day": "2024-12-01",
                                "carbs": 250,
                                "proteins": 150,
                                "fats": 70,
                            },
                            {
                                "day": "2024-12-02",
                                "carbs": 230,
                                "proteins": 140,
                                "fats": 60,
                            },
                        ],
                    }
                },
                "weekly_summaries": {
                    "total_calories": 14000,
                    "average_daily_calories": 2000,
                    "habit_analysis": "Consistent protein intake",
                },
                "diet_comparison": {
                    "recommended_calories": 2000,
                    "current_average": 2100,
                },
                "multi_language_support": ["English", "Spanish", "French"],
                "offline_mode": True,
            },
        }
    return {"result": "success", "food_name_list_response": food_name_list_response}
