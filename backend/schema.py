from typing import List
from pydantic import BaseModel, validator
import pandas as pd

# Acquisition Samples model
class AcquisitionSamples(BaseModel):
    fdc_id_of_sample_food: int
    fdc_id_of_acquisition_food: int

# Agricultural Samples Model
class AgriculturalSamples(BaseModel):
    fdc_id: int
    acquisition_date: str
    market_class: str
    treatment: str
    state: str

# Branded Foods model
class BrandedFoods(BaseModel):
    fdc_id: int
    brand_owner: str
    brand_name: str
    subbrand_name: str
    gtin_upc: int
    ingredients: str
    serving_size: float
    serving_size_unit: str
    household_serving_fulltext: str
    branded_food_category: str
    data_source: str
    package_weight: float
    modified_date: str
    available_date: str
    market_country: str
    discontinued_date: str
    preparation_state_code: str
    trade_channel: str
    short_description: str

# Fndds Derivation model
class FnddsDerivation(BaseModel):
    derivation_code: str
    derivation_description: str

# Foods Model
class Foods(BaseModel):
    fdc_id: int
    data_type: str
    description: str
    food_category_id: str
    publication_date: str

# Food Attribute Model
class FoodAttribute(BaseModel):
    id: int
    fdc_id: int
    seq_num: float
    food_attribute_type_id: float
    name: str
    value: str

# Food Attribute Type Model
class FoodAttributeType(BaseModel):
    id: int
    name: str
    description: str

# Food Calorie Conversion Factor model
class FoodCalorieConversionFactor(BaseModel):
    food_nutrient_conversion_factor_id: float
    protein_value: float
    fat_value: float
    carbohydrate_value: float

# Food Category Model
class FoodCategory(BaseModel):
    id: int
    code: str
    description: str

# Food Component Model
class FoodComponent(BaseModel):
    id: int
    fdc_id: int
    name: str
    pct_weight: float
    is_refuse: str
    gram_weight: float
    data_points: int
    min_year_acquired: float

# Food Nutrient Model
class FoodNutrient(BaseModel):
    id: int
    fdc_id: int
    nutrient_id: int
    amount: float
    data_points: float
    derivation_id: float
    min: float
    max: float
    median: float
    loq: float
    footnote: str
    min_year_acquired: float
    percent_daily_value: float

# Food Nutrient Conversion Factor Model 
class FoodNutrientConversionFactor(BaseModel):
    id: int
    fdc_id: int

# Lab Method Model
class LabMethod(BaseModel):
    id: int
    description: str
    technique: str

# Lab Method Code Model
class LabMethodCode(BaseModel):
    lab_method_id: int
    code: str

# Lab Method Nutrient Model
class LabMethodNutrient(BaseModel):
    lab_method_id: int
    nutrient_id: int

# Market Acquisition Model
class MarketAcquisition(BaseModel):
    fdc_id: int
    brand_description: str
    expiration_date: str
    label_weight: float
    location: str
    acquisition_date: str
    sales_type: str
    sample_lot_nbr: str
    sell_by_date: str
    store_city: str
    store_name: str
    store_state: str
    upc_code: str

# Measure Unit Model
class MeasureUnit(BaseModel):
    id: int
    name: str

# Microbe Model
class Microbe(BaseModel):
    id: int
    foodId: int
    method: str
    microbe_code: str
    min_value: int
    max_value: float
    uom: str

# Nutrient Model
class Nutrient(BaseModel):
    id: int
    name: str
    unit_name: str
    nutrient_nbr: float
    rank: float

# Retention Factor model
class RetentionFactor(BaseModel):
    n.gid: int
    n.code: int
    n.foodGroupId: int
    n.description: str

# Sample Food Model
class SampleFood(BaseModel):
    fdc_id: int

# SR Legacy Food Model
class SRLegacyFood(BaseModel):
    fdc_id: int
    NDB_number: int

# Sub-Sample Food Model
class SubSampleFood(BaseModel):
    fdc_id: int
    fdc_id_of_sample_food: int

# Sub Sample Result model
class SubSampleResult(BaseModel):
    food_nutrient_id: int
    adjusted_amount: float
    lab_method_id: int
    nutrient_name: str

# Survey Fndds Food Model
class SurveyFnddsFood(BaseModel):
    fdc_id: int
    food_code: int
    wweia_category_code: int
    start_date: str
    end_date: str

# WWEIA Food Category model
class WWEIAFoodCategory(BaseModel):
    wweia_food_category: int
    wweia_food_category_description: str
