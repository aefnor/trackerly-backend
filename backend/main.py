import hashlib
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from backend import schema
from fastapi import FastAPI, HTTPException, Depends, Query
import jwt
from sqlalchemy.ext.asyncio.session import (
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import select
from backend.models import Base, FoodEntry, User
import datetime
from backend.food import analyze_food_sentence_locally
from typing import AsyncGenerator
from fastapi.middleware.cors import CORSMiddleware


# Use the DATABASE_URL from the environment (injected via Docker Compose)
import os

HAS_CONFIGURED_DATABASE = bool(os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL"))


def _get_database_config() -> tuple[str, dict[str, bool]]:
    database_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
    if not database_url:
        return (
            "postgresql+asyncpg://fooduser:foodpass@localhost:5432/foodtracker",
            {},
        )

    connect_args = {}

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    parts = urlsplit(database_url)
    if parts.query:
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query.pop("channel_binding", None)
        sslmode = query.pop("sslmode", None)
        if sslmode and sslmode != "disable":
            connect_args["ssl"] = True
        database_url = urlunsplit(
            (parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment)
        )

    return database_url, connect_args


DATABASE_URL, DB_CONNECT_ARGS = _get_database_config()
JWT_SECRET = os.getenv("JWT_SECRET", "secret")

# SQLAlchemy Setup
engine = create_async_engine(
    DATABASE_URL,
    connect_args=DB_CONNECT_ARGS,
    echo=os.getenv("SQLALCHEMY_ECHO") == "true",
)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# FastAPI App
app = FastAPI()

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    if os.getenv("VERCEL") and not HAS_CONFIGURED_DATABASE:
        print("Skipping database startup: DATABASE_URL/POSTGRES_URL is not configured")
        return

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health():
    return {"status": "ok"}


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if os.getenv("VERCEL") and not HAS_CONFIGURED_DATABASE:
        raise HTTPException(
            status_code=503,
            detail="Database is not configured for this deployment.",
        )

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
        JWT_SECRET,
        algorithm="HS256",
    )

    return {"token": token}


@app.post("/signup/", response_model=schema.UserRead)
async def signup(user: schema.User, db: AsyncSession = Depends(get_db)):
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
        JWT_SECRET,
        algorithm="HS256",
    )
    return {"token": token}


# check if user token is valid
@app.get("/check-user-token-valid/{token}")
async def check_user_token_valid(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        print(decoded_token)
        # check if token is expired
        if (
            datetime.datetime.utcfromtimestamp(decoded_token["exp"])
            < datetime.datetime.utcnow()
        ):
            raise HTTPException(status_code=401, detail="Token has expired")

        return {
            "valid": True,
            "email": jwt.decode(token, JWT_SECRET, algorithms=["HS256"])["email"],
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
    return {
        "result": "success",
        "food_name_list_response": analyze_food_sentence_locally(request.sentence),
    }


def _serialize_food_entry(entry: FoodEntry) -> dict:
    return {
        "id": entry.id,
        "food_name": entry.food_name,
        "category": entry.category,
        "date": entry.date,
        "portion_size": entry.portion_size,
        "calories": entry.calories,
        "macronutrients": entry.macronutrients,
        "micronutrients": entry.micronutrients,
        "fiber_content": entry.fiber_content,
        "sugar": entry.sugar,
        "cholesterol": entry.cholesterol,
        "sodium": entry.sodium,
        "fats": entry.fats,
        "common_allergens": entry.common_allergens,
        "dietary_tags": entry.dietary_tags,
        "custom_recipes": entry.custom_recipes,
        "user_notes": entry.user_notes,
        "barcode_scanner": entry.barcode_scanner,
        "photo_upload": entry.photo_upload,
        "offline_mode": entry.offline_mode,
        "created_time": entry.created_time,
        "updated_time": entry.updated_time,
    }


@app.post("/food-entry/", status_code=201, response_model=schema.FoodEntryRead)
async def create_food_entry(
    entry: schema.FoodEntryCreate, db: AsyncSession = Depends(get_db)
):
    payload = entry.model_dump(exclude_unset=True)
    if payload.get("date") is None:
        payload["date"] = datetime.datetime.utcnow()

    db_entry = FoodEntry(**payload)
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    return _serialize_food_entry(db_entry)


@app.get("/food-entries/", response_model=list[schema.FoodEntryRead])
async def list_food_entries(
    start_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    query = select(FoodEntry).order_by(FoodEntry.date.desc(), FoodEntry.id.desc())

    if start_date:
        try:
            start = datetime.datetime.fromisoformat(start_date)
        except ValueError:
            start = datetime.datetime.fromisoformat(f"{start_date}T00:00:00")
        query = query.where(FoodEntry.date >= start)

    if end_date:
        try:
            end = datetime.datetime.fromisoformat(end_date)
        except ValueError:
            end = datetime.datetime.fromisoformat(f"{end_date}T23:59:59.999999")
        if end.time() == datetime.time.min:
            end = end.replace(hour=23, minute=59, second=59, microsecond=999999)
        query = query.where(FoodEntry.date <= end)

    result = await db.execute(query)
    return [_serialize_food_entry(entry) for entry in result.scalars().all()]


# routes_openfood.py
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

# Models you already defined
from backend.models import (
    Product as SAProduct,
    ProductIngredient,
    ProductImage,
    ProductPackaging,
)
from backend.schema import ProductEnvelope

router = APIRouter(prefix="/api/openfood", tags=["openfoodfacts"])


def _upsert_openfood_product(
    db: Session, payload: Dict[str, Any]
) -> tuple[SAProduct, bool]:
    """
    Upsert a product from an OpenFoodFacts-like payload.
    Returns (row, created_bool).
    """
    try:
        env = ProductEnvelope.model_validate(payload)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid payload: {e}")

    p = env.product

    created = False
    row = db.get(SAProduct, p.code)
    if row is None:
        row = SAProduct(code=p.code)
        db.add(row)
        created = True

    # --- map scalar fields ---
    row.id = p.id
    row.product_name = p.product_name
    row.brands = p.brands
    row.quantity = p.quantity
    row.countries = p.countries
    row.lang = p.lang
    row.lc = p.lc
    row.created_t = p.created_t
    row.last_modified_t = p.last_modified_t
    row.last_updated_t = p.last_updated_t
    row.rev = p.rev
    row.complete = p.complete
    row.completeness = p.completeness

    # images (flat)
    row.image_url = p.image_url
    row.image_small_url = p.image_small_url
    row.image_thumb_url = p.image_thumb_url
    row.image_front_url = p.image_front_url
    row.image_ingredients_url = p.image_ingredients_url
    row.image_nutrition_url = p.image_nutrition_url

    # json blobs
    row.nutriments = p.nutriments.model_dump(by_alias=True) if p.nutriments else None
    row.nutrient_levels = p.nutrient_levels
    row.nutriscore = p.nutriscore.model_dump(by_alias=True) if p.nutriscore else None
    row.nutriscore_grade = p.nutriscore_grade
    row.nutriscore_score = p.nutriscore_score

    row.ecoscore_data = (
        p.ecoscore_data.model_dump(by_alias=True) if p.ecoscore_data else None
    )
    row.ecoscore_grade = p.ecoscore_grade
    row.ecoscore_score = p.ecoscore_score

    # tags
    row.categories_tags = p.categories_tags
    row.countries_tags = p.countries_tags
    row.brands_tags = p.brands_tags
    row.editors_tags = p.editors_tags
    row.data_sources_tags = p.data_sources_tags
    row.misc_tags = p.misc_tags
    row.popularity_tags = p.popularity_tags
    row.states_tags = p.states_tags
    row.packaging_tags = p.packaging_tags
    row.packaging_materials_tags = p.packaging_materials_tags
    row.packaging_shapes_tags = p.packaging_shapes_tags

    # allergens/traces
    row.allergens = p.allergens
    row.allergens_tags = p.allergens_tags
    row.traces = p.traces
    row.traces_tags = p.traces_tags

    # blobs
    row.selected_images = (
        p.selected_images.model_dump(by_alias=True) if p.selected_images else None
    )
    row.images_raw = {k: v.model_dump() for k, v in (p.images or {}).items()} or None
    # keep anything else for future-proofing
    row.extra_blob = p.extra_blob or {}

    # --- replace child collections ---
    row.ingredients.clear()
    if p.ingredients:
        for ing in p.ingredients:
            row.ingredients.append(
                ProductIngredient(
                    ingredient_id=ing.id,
                    text=ing.text,
                    rank=ing.rank,
                    percent_estimate=ing.percent_estimate,
                    percent_min=(
                        None if ing.percent_min is None else str(ing.percent_min)
                    ),
                    percent_max=(
                        None if ing.percent_max is None else str(ing.percent_max)
                    ),
                    processing=ing.processing,
                    vegan=ing.vegan,
                    vegetarian=ing.vegetarian,
                    ciqual_food_code=ing.ciqual_food_code,
                    ciqual_proxy_food_code=ing.ciqual_proxy_food_code,
                    ecobalyse_code=ing.ecobalyse_code,
                    from_palm_oil=ing.from_palm_oil,
                    is_in_taxonomy=ing.is_in_taxonomy,
                    extra_blob={},
                )
            )

    row.packagings.clear()
    if p.packagings:
        for pk in p.packagings:
            row.packagings.append(
                ProductPackaging(
                    material=pk.material,
                    shape=pk.shape,
                    food_contact=pk.food_contact,
                    environmental_score_material_score=pk.environmental_score_material_score,
                    environmental_score_shape_ratio=pk.environmental_score_shape_ratio,
                    non_recyclable_and_non_biodegradable=(
                        None
                        if pk.non_recyclable_and_non_biodegradable is None
                        else str(pk.non_recyclable_and_non_biodegradable)
                    ),
                    extra_blob={},
                )
            )

    row.image_entries.clear()
    if p.images:
        for key, img in p.images.items():
            row.image_entries.append(
                ProductImage(
                    key=key,
                    img_meta=img.model_dump(),
                    uploader=img.uploader,
                    uploaded_t=img.uploaded_t,
                )
            )

    db.flush()
    return row, created


@router.post("/food-entry/", status_code=status.HTTP_201_CREATED)
def ingest_openfood_product(
    payload: Dict[str, Any],
    response: Response,
    db: Session = Depends(get_db),
):
    """
    Ingest/Upsert a full OpenFoodFacts product JSON.
    - 201 Created on first insert
    - 200 OK on update
    """
    try:
        row, created = _upsert_openfood_product(db, payload)
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upsert product: {e}")

    if not created:
        response.status_code = status.HTTP_200_OK

    # Optional Location header
    response.headers["Location"] = f"/api/openfood/products/{row.code}"

    # Return a compact view; you can swap to a Pydantic response_model if you want
    return {
        "code": row.code,
        "product_name": row.product_name,
        "brands": row.brands,
        "nutriscore_grade": row.nutriscore_grade,
        "ecoscore_grade": row.ecoscore_grade,
        "created": created,
    }
