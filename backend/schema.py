import hashlib
from typing import List
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, Dict, Any


class UserSignIn(BaseModel):
    email: str
    password: str


class User(BaseModel):
    username: str
    password: str
    password_hash: Optional[str] = None
    email: str
    first_name: str
    last_name: str

    # @validator("username")
    # def username_must_contain_underscore(cls, v):
    #     if "_" not in v:
    #         raise ValueError("must contain an underscore")
    #     return v

    # hash the password
    # @validator("password")
    # def hash_password(cls, v):
    #     return hashlib.sha256(v.encode()).hexdigest()

    class Config:
        orm_mode = True


class FoodEntryBase(BaseModel):
    food_name: str
    category: Optional[str]
    date: datetime
    portion_size: Optional[Dict[str, Any]]
    calories: Optional[float]
    macronutrients: Optional[Dict[str, Any]]
    micronutrients: Optional[Dict[str, Any]]

    # Core nutrition tracking
    fiber_content: Optional[str]
    sugar: Optional[Dict[str, Any]]
    cholesterol: Optional[str]
    sodium: Optional[str]
    fats: Optional[Dict[str, Any]]

    # Additional features
    common_allergens: Optional[List[str]]
    dietary_tags: Optional[List[str]]
    custom_recipes: Optional[Dict[str, Any]]
    user_notes: Optional[str]

    # App features
    barcode_scanner: Optional[str]
    photo_upload: Optional[str]
    offline_mode: Optional[bool]

    class Config:
        orm_mode = True


class TextRequest(BaseModel):
    sentence: str


class UserForgotPassword(BaseModel):
    email: str
