import hashlib
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, validator
from datetime import datetime


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


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    created_by: Optional[str] = None
    created_time: Optional[datetime] = None
    updated_by: Optional[str] = None
    updated_time: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class FoodEntryBase(BaseModel):
    food_name: str
    category: Optional[str] = None
    date: Optional[datetime] = None
    portion_size: Optional[Dict[str, Any]] = None
    calories: Optional[float] = None
    macronutrients: Optional[Dict[str, Any]] = None
    micronutrients: Optional[Dict[str, Any]] = None

    # Core nutrition tracking
    fiber_content: Optional[str] = None
    sugar: Optional[Dict[str, Any]] = None
    cholesterol: Optional[str] = None
    sodium: Optional[str] = None
    fats: Optional[Dict[str, Any]] = None

    # Additional features
    common_allergens: Optional[List[str]] = None
    dietary_tags: Optional[List[str]] = None
    custom_recipes: Optional[Dict[str, Any]] = None
    user_notes: Optional[str] = None

    # App features
    barcode_scanner: Optional[str] = None
    photo_upload: Optional[str] = None
    offline_mode: Optional[bool] = None

    class Config:
        orm_mode = True


class FoodEntryCreate(FoodEntryBase):
    pass


class FoodEntryRead(FoodEntryBase):
    id: int
    created_time: Optional[datetime] = None
    updated_time: Optional[datetime] = None


class TextRequest(BaseModel):
    sentence: str


class UserForgotPassword(BaseModel):
    email: str


# ---- Leaf / nested helpers ----


class ImageSizes(BaseModel):
    model_config = ConfigDict(extra="allow")
    # Common resolutions appear repeatedly; keep flexible for others
    size_100: Optional[Dict[str, int]] = Field(default=None, alias="100")
    size_200: Optional[Dict[str, int]] = Field(default=None, alias="200")
    size_400: Optional[Dict[str, int]] = Field(default=None, alias="400")
    full: Optional[Dict[str, int]] = None


class ImageEntry(BaseModel):
    model_config = ConfigDict(extra="allow")
    sizes: Optional[ImageSizes] = None
    uploaded_t: Optional[int] = None
    uploader: Optional[str] = None
    rev: Optional[str] = None
    imgid: Optional[str] = None
    coordinates_image_size: Optional[str] = None
    x1: Optional[int] = None
    x2: Optional[int] = None
    y1: Optional[int] = None
    y2: Optional[int] = None


class SelectedImageVariant(BaseModel):
    en: Optional[str] = None


class SelectedImageGroup(BaseModel):
    display: Optional[SelectedImageVariant] = None
    small: Optional[SelectedImageVariant] = None
    thumb: Optional[SelectedImageVariant] = None


class SelectedImages(BaseModel):
    front: Optional[SelectedImageGroup] = None
    ingredients: Optional[SelectedImageGroup] = None
    nutrition: Optional[SelectedImageGroup] = None


class Ingredient(BaseModel):
    id: Optional[str] = None
    text: Optional[str] = None
    rank: Optional[int] = None
    percent_estimate: Optional[float] = None
    percent_min: Optional[float | str] = None
    percent_max: Optional[float | str] = None
    processing: Optional[str] = None
    vegan: Optional[str] = None
    vegetarian: Optional[str] = None
    ciqual_food_code: Optional[str] = None
    ciqual_proxy_food_code: Optional[str] = None
    ecobalyse_code: Optional[str] = None
    from_palm_oil: Optional[str] = None
    is_in_taxonomy: Optional[int] = None


class Nutriments(BaseModel):
    model_config = ConfigDict(extra="allow")
    # Strongly type the common ones; leave the rest flexible via extra="allow"
    energy_kcal_100g: Optional[float] = Field(None, alias="energy-kcal_100g")
    energy_kcal_serving: Optional[float] = Field(None, alias="energy-kcal_serving")
    energy_kcal: Optional[float] = Field(None, alias="energy-kcal")
    energy_100g: Optional[float] = Field(None, alias="energy_100g")
    energy_serving: Optional[float] = Field(None, alias="energy_serving")
    fat_100g: Optional[float] = Field(None, alias="fat_100g")
    saturated_fat_100g: Optional[float] = Field(None, alias="saturated-fat_100g")
    carbohydrates_100g: Optional[float] = Field(None, alias="carbohydrates_100g")
    sugars_100g: Optional[float] = Field(None, alias="sugars_100g")
    fiber_100g: Optional[float] = Field(None, alias="fiber_100g")
    proteins_100g: Optional[float] = Field(None, alias="proteins_100g")
    salt_100g: Optional[float] = Field(None, alias="salt_100g")
    sodium_100g: Optional[float] = Field(None, alias="sodium_100g")
    # Serving fields
    fat_serving: Optional[float] = Field(None, alias="fat_serving")
    saturated_fat_serving: Optional[float] = Field(None, alias="saturated-fat_serving")
    carbohydrates_serving: Optional[float] = Field(None, alias="carbohydrates_serving")
    sugars_serving: Optional[float] = Field(None, alias="sugars_serving")
    fiber_serving: Optional[float] = Field(None, alias="fiber_serving")
    proteins_serving: Optional[float] = Field(None, alias="proteins_serving")
    salt_serving: Optional[float] = Field(None, alias="salt_serving")
    sodium_serving: Optional[float] = Field(None, alias="sodium_serving")


class NutriScore2021(BaseModel):
    model_config = ConfigDict(extra="allow")
    grade: Optional[str] = None
    score: Optional[int] = None
    data: Optional[Dict[str, Any]] = None


class NutriScore2023(BaseModel):
    model_config = ConfigDict(extra="allow")
    grade: Optional[str] = None
    score: Optional[int] = None
    data: Optional[Dict[str, Any]] = None


class NutriScore(BaseModel):
    model_config = ConfigDict(extra="allow")
    score_2021: Optional[NutriScore2021] = Field(None, alias="2021")
    score_2023: Optional[NutriScore2023] = Field(None, alias="2023")


class PackagingEntry(BaseModel):
    material: Optional[str] = None
    shape: Optional[str] = None
    food_contact: Optional[int] = None
    environmental_score_material_score: Optional[float] = None
    environmental_score_shape_ratio: Optional[float] = None
    non_recyclable_and_non_biodegradable: Optional[str | int] = None


class EcoScoreData(BaseModel):
    model_config = ConfigDict(extra="allow")
    grade: Optional[str] = None
    score: Optional[int] = None
    agribalyse: Optional[Dict[str, Any]] = None
    adjustments: Optional[Dict[str, Any]] = None
    previous_data: Optional[Dict[str, Any]] = None
    scores: Optional[Dict[str, int]] = None
    grades: Optional[Dict[str, str]] = None
    missing: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class Product(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    # Required identifiers
    id: Optional[str] = None
    code: str

    # Common scalar/meta
    product_name: Optional[str] = None
    brands: Optional[str] = None
    quantity: Optional[str] = None
    countries: Optional[str] = None
    lang: Optional[str] = None
    lc: Optional[str] = None
    created_t: Optional[int] = None
    last_modified_t: Optional[int] = None
    last_updated_t: Optional[int] = None
    rev: Optional[int] = None
    complete: Optional[int] = None
    completeness: Optional[float] = None

    # Nutrition / scoring
    nutriments: Optional[Nutriments] = None
    nutrient_levels: Optional[Dict[str, str]] = None
    nutriscore: Optional[NutriScore] = None
    nutriscore_grade: Optional[str] = None
    nutriscore_score: Optional[int] = None
    nutriments_raw: Optional[Dict[str, Any]] = Field(
        None, alias="nutriments"
    )  # full blob already covered

    ecoscore_data: Optional[EcoScoreData] = None
    ecoscore_grade: Optional[str] = None
    ecoscore_score: Optional[int] = None

    # Ingredients
    ingredients_text: Optional[str] = None
    ingredients_text_en: Optional[str] = None
    ingredients: Optional[List[Ingredient]] = None
    ingredients_n: Optional[int] = None
    ingredients_analysis: Optional[Dict[str, List[str]]] = None
    allergens: Optional[str] = None
    allergens_tags: Optional[List[str]] = None
    traces: Optional[str] = None
    traces_tags: Optional[List[str]] = None

    # Images
    image_url: Optional[str] = None
    image_small_url: Optional[str] = None
    image_thumb_url: Optional[str] = None
    selected_images: Optional[SelectedImages] = None
    images: Optional[Dict[str, ImageEntry]] = None
    image_front_url: Optional[str] = None
    image_ingredients_url: Optional[str] = None
    image_nutrition_url: Optional[str] = None

    # Tags/arrays (keep as lists)
    categories: Optional[str] = None
    categories_tags: Optional[List[str]] = None
    countries_tags: Optional[List[str]] = None
    brands_tags: Optional[List[str]] = None
    editors_tags: Optional[List[str]] = None
    data_sources_tags: Optional[List[str]] = None
    misc_tags: Optional[List[str]] = None
    popularity_tags: Optional[List[str]] = None
    states_tags: Optional[List[str]] = None
    pnns_groups_1: Optional[str] = None
    pnns_groups_2: Optional[str] = None

    # Packaging
    packaging: Optional[str] = None
    packagings: Optional[List[PackagingEntry]] = None
    packaging_tags: Optional[List[str]] = None
    packaging_materials_tags: Optional[List[str]] = None
    packaging_shapes_tags: Optional[List[str]] = None

    # Everything else (future-proof)
    extra_blob: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_openfoodfacts(cls, d: Dict[str, Any]) -> "Product":
        # Peel off known top-level product dict; keep the rest in extra_blob
        raw = dict(d)  # shallow copy
        # Known fields are those declared above; shove unknowns into extra_blob
        known = {k for k in cls.model_fields}
        extra = {k: v for k, v in raw.items() if k not in known}
        raw["extra_blob"] = extra
        return cls.model_validate(raw)


class ProductEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    code: str
    status: int
    status_verbose: Optional[str] = None
    product: Product
