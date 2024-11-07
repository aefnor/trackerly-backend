import hashlib
from pydantic import validator
from sqlalchemy import Column, Date, Float, String, Integer, Text
from sqlalchemy.orm import declarative_base, relationship

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

# Acquisition Samples model
class AcquisitionSamples(Base):
    __tablename__ = "acquisition_samples"

    fdc_id_of_sample_food = Column(Integer, primary_key=True)
    fdc_id_of_acquisition_food = Column(Integer)

    # Relation to Branded Foods model
    branded_foods = relationship('BrandedFoods', foreign_keys='BrandedFoods.fdc_id')
    # Relation to Foods model
    foods = relationship('Foods', foreign_keys='Foods.fdc_id')
    # Relation to Agricultural Samples model
    agricultural_samples = relationship('AgriculturalSamples', foreign_keys='AgriculturalSamples.fdc_id')
    # Relation to Food Attribute model
    food_attribute = relationship('FoodAttribute', foreign_keys='FoodAttribute.fdc_id')
    # Relation to Food Attribute Type model
    food_attribute_type = relationship('FoodAttributeType', foreign_keys='FoodAttributeType.id')
    # Relation to Food Calorie Conversion Factor model
    food_calorie_conversion_factor = relationship('FoodCalorieConversionFactor', foreign_keys='FoodCalorieConversionFactor.food_nutrient_conversion_factor_id')
    # Relation to Food Category model
    food_category = relationship('FoodCategory', foreign_keys='FoodCategory.id')
    # Relation to Food Component model
    food_component = relationship('FoodComponent', foreign_keys='FoodComponent.fdc_id')
    # Relation to Food Nutrient model
    food_nutrient = relationship('FoodNutrient', foreign_keys='FoodNutrient.fdc_id')
    # Relation to Food Nutrient Conversion Factor model
    food_nutrient_conversion_factor = relationship('FoodNutrientConversionFactor', foreign_keys='FoodNutrientConversionFactor.id')
    # Relation to Lab Method model
    lab_method = relationship('LabMethod', foreign_keys='LabMethod.id')
    # Relation to Lab Method Code model
    lab_method_code = relationship('LabMethodCode', foreign_keys='LabMethodCode.lab_method_id')
    # Relation to Lab Method Nutrient model
    lab_method_nutrient = relationship('LabMethodNutrient', foreign_keys='LabMethodNutrient.lab_method_id')

# Agricultural Samples Model
class AgriculturalSamples(Base):
    __tablename__ = "agricultural_samples"

    fdc_id = Column(Integer, primary_key=True)
    acquisition_date = Column(Date)
    market_class = Column(String)
    treatment = Column(String)
    state = Column(String)

    # Relation to Foods model
    foods = relationship('Foods', foreign_keys='Foods.fdc_id')
    # Relation to Acquisition Samples model
    acquisition_samples = relationship('AcquisitionSamples', foreign_keys='AcquisitionSamples.fdc_id_of_sample_food')
    # Relation to Agricultural Samples model
    agricultural_samples = relationship('AgriculturalSamples', foreign_keys='AgriculturalSamples.fdc_id')
    # Relation to Market Acquisition model
    market_acquisition = relationship('MarketAcquisition', foreign_keys='MarketAcquisition.fdc_id')
    # Relation to Sample Food model
    sample_food = relationship('SampleFood', foreign_keys='SampleFood.fdc_id')
    # Relation to SRLegacy Food model
    sr_legacy_food = relationship('SRLegacyFood', foreign_keys='SRLegacyFood.fdc_id')
    # Relation to Sub-Sample Food model
    sub_sample_food = relationship('SubSampleFood', foreign_keys='SubSampleFood.fdc_id')
    # Relation to Survey Fndds Food model
    survey_fndds_food = relationship('SurveyFnddsFood', foreign_keys='SurveyFnddsFood.fdc_id')
    # Relation to WWEIA Food Category model
    wweia_food_category = relationship('WWEIAFoodCategory', foreign_keys='WWEIAFoodCategory.wweia_food_category')

# Branded Foods model
class BrandedFoods(Base):
    __tablename__ = "branded_foods"

    fdc_id = Column(Integer, primary_key=True)
    brand_owner = Column(String)
    brand_name = Column(String)
    subbrand_name = Column(String)
    gtin_upc = Column(Integer)
    ingredients = Column(String)
    serving_size = Column(Float)
    serving_size_unit = Column(String)
    household_serving_fulltext = Column(String)
    branded_food_category = Column(String)
    data_source = Column(String)
    package_weight = Column(Float)
    modified_date = Column(Date)
    available_date = Column(Date)
    market_country = Column(String)
    discontinued_date = Column(Date)
    preparation_state_code = Column(String)
    trade_channel = Column(String)
    short_description = Column(String)

    # Relation to Acquisition Samples model
    acquisition_samples = relationship('AcquisitionSamples', foreign_keys='AcquisitionSamples.fdc_id_of_acquisition_food')
    # Relation to Foods model
    foods = relationship('Foods', foreign_keys='Foods.fdc_id')
    # Relation to Food Attribute model
    food_attribute = relationship('FoodAttribute', foreign_keys='FoodAttribute.fdc_id')
    # Relation to Food Attribute Type model
    food_attribute_type = relationship('FoodAttributeType', foreign_keys='FoodAttributeType.id')
    # Relation to Food Calorie Conversion Factor model
    food_calorie_conversion_factor = relationship('FoodCalorieConversionFactor', foreign_keys='FoodCalorieConversionFactor.food_nutrient_conversion_factor_id')
    # Relation to Food Category model
    food_category = relationship('FoodCategory', foreign_keys='FoodCategory.id')
    # Relation to Food Component model
    food_component = relationship('FoodComponent', foreign_keys='FoodComponent.fdc_id')
    # Relation to Food Nutrient model
    food_nutrient = relationship('FoodNutrient', foreign_keys='FoodNutrient.fdc_id')
    # Relation to Food Nutrient Conversion Factor model
    food_nutrient_conversion_factor = relationship('FoodNutrientConversionFactor', foreign_keys='FoodNutrientConversionFactor.id')
    # Relation to Lab Method model
    lab_method = relationship('LabMethod', foreign_keys='LabMethod.id')
    # Relation to Lab Method Code model
    lab_method_code = relationship('LabMethodCode', foreign_keys='LabMethodCode.lab_method_id')
    # Relation to Lab Method Nutrient model
    lab_method_nutrient = relationship('LabMethodNutrient', foreign_keys='LabMethodNutrient.lab_method_id')

# Fndds Derivation model
class FnddsDerivation(Base):
    __tablename__ = "fndds_derivation"

    derivation_code = Column(String, primary_key=True)
    derivation_description = Column(String)

    # Relation to Food Nutrient model
    food_nutrient = relationship('FoodNutrient', foreign_keys='FoodNutrient.derivation_id')
    # Relation to Food Nutrient Conversion Factor model
    food_nutrient_conversion_factor = relationship('FoodNutrientConversionFactor', foreign_keys='FoodNutrientConversionFactor.derivation_id')
    # Relation to Lab Method Nutrient model
    lab_method_nutrient = relationship('LabMethodNutrient', foreign_keys='LabMethodNutrient.derivation_id')
    # Relation to Food Category model
    food_category = relationship('FoodCategory', foreign_keys='FoodCategory.derivation_id')
    # Relation to Food Component model
    food_component = relationship('FoodComponent', foreign_keys='FoodComponent.derivation_id')
    # Relation to Food Nutrient model
    food_nutrient = relationship('FoodNutrient', foreign_keys='FoodNutrient.derivation_id')
    # Relation to Food Nutrient Conversion Factor model
    food_nutrient_conversion_factor = relationship('FoodNutrientConversionFactor', foreign_keys='FoodNutrientConversionFactor.derivation_id')
    # Relation to Lab Method model
    lab_method = relationship('LabMethod', foreign_keys='LabMethod.derivation_id')
    # Relation to Lab Method Code model
    lab_method_code = relationship('LabMethodCode', foreign_keys='LabMethodCode.derivation_id')
    # Relation to Lab Method Nutrient model
    lab_method_nutrient = relationship('LabMethodNutrient', foreign_keys='LabMethodNutrient.derivation_id')

# Foods Model
class Foods(Base):
    __tablename__ = "foods"

    fdc_id = Column(Integer, primary_key=True)
    data_type = Column(String)
    description = Column(String)
    food_category_id = Column(String)
    publication_date = Column(Date)

    # Relation to Acquisition Samples model
    acquisition_samples = relationship('AcquisitionSamples', foreign_keys='AcquisitionSamples.fdc_id_of_sample_food')
    # Relation to Agricultural Samples model
    agricultural_samples = relationship('AgriculturalSamples', foreign_keys='AgriculturalSamples.fdc_id')
    # Relation to Branded Foods model
    branded_foods = relationship('BrandedFoods', foreign_keys='BrandedFoods.fdc_id')
    # Relation to Food Attribute model
    food_attribute = relationship('FoodAttribute', foreign_keys='FoodAttribute.fdc_id')
    # Relation to Food Attribute Type model
    food_attribute_type = relationship('FoodAttributeType', foreign_keys='FoodAttributeType.id')
    # Relation to Food Calorie Conversion Factor model
    food_calorie_conversion_factor = relationship('FoodCalorieConversionFactor', foreign_keys='FoodCalorieConversionFactor.food_nutrient_conversion_factor_id')
    # Relation to Food Category model
    food_category = relationship('FoodCategory', foreign_keys='FoodCategory.id')
    # Relation to Food Component model
    food_component = relationship('FoodComponent', foreign_keys='FoodComponent.fdc_id')
    # Relation to Food Nutrient model
    food_nutrient = relationship('FoodNutrient', foreign_keys='FoodNutrient.fdc_id')
    # Relation to Food Nutrient Conversion Factor model
    food_nutrient_conversion_factor = relationship('FoodNutrientConversionFactor', foreign_keys='FoodNutrientConversionFactor.id')
    # Relation to Lab Method model
    lab_method = relationship('LabMethod', foreign_keys='LabMethod.id')
    # Relation to Lab Method Code model
    lab_method_code = relationship('LabMethodCode', foreign_keys='LabMethodCode.lab_method_id')
    # Relation to Lab Method Nutrient model
    lab_method_nutrient = relationship('LabMethodNutrient', foreign_keys='LabMethodNutrient.lab_method_id')

# Food Attribute Model
class FoodAttribute(Base):
    __tablename__ = "food_attribute"

    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer)
    seq_num = Column(Float)
    food_attribute_type_id = Column(Float)
    name = Column(String)
    value = Column(String)

    # Relation to Foods model
    foods = relationship('Foods', foreign_keys='Foods.fdc_id')
    # Relation to Food Attribute Type model
    food_attribute_type = relationship('FoodAttributeType', foreign_keys='FoodAttributeType.id')
    # Relation to Food Calorie Conversion Factor model
    food_calorie_conversion_factor = relationship('FoodCalorieConversionFactor', foreign_keys='FoodCalorieConversionFactor.food_nutrient_conversion_factor_id')
    # Relation to Food Nutrient model 
    food_nutrient = relationship('FoodNutrient', foreign_keys='FoodNutrient.food_attribute_id')
    # Relation to Food Nutrient Conversion Factor model
    food_nutrient_conversion_factor = relationship('FoodNutrientConversionFactor', foreign_keys='FoodNutrientConversionFactor.id')
    # Relation to Lab Method Nutrient model
    lab_method_nutrient = relationship('LabMethodNutrient', foreign_keys='LabMethodNutrient.food_attribute_id')
    # Relation to Branded Foods model
    branded_foods = relationship('BrandedFoods', foreign_keys='BrandedFoods.fdc_id')
    # Relation to Foods model
    foods = relationship('Foods', foreign_keys='Foods.fdc_id')
    # Relation to Food Component model
    food_component = relationship('FoodComponent', foreign_keys='FoodComponent.fdc_id')
    # Relation to Food Nutrient model
    food_nutrient = relationship('FoodNutrient', foreign_keys='FoodNutrient.food_attribute_id')
    # Relation to Lab Method model
    lab_method = relationship('LabMethod', foreign_keys='LabMethod.id')
    # Relation to Lab Method Code model
    lab_method_code = relationship('LabMethodCode', foreign_keys='LabMethodCode.lab_method_id')
    # Relation to Lab Method Nutrient model
    lab_method_nutrient = relationship('LabMethodNutrient', foreign_keys='LabMethodNutrient.food_attribute_id')

# Food Attribute Type Model
class FoodAttributeType(Base):
    __tablename__ = "food_attribute_type"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    # Relation to Food Attribute model
    food_attribute = relationship('FoodAttribute', foreign_keys='FoodAttribute.food_attribute_type_id')
    # Relation to Food Calorie Conversion Factor model
    food_calorie_conversion_factor = relationship('FoodCalorieConversionFactor', foreign_keys='FoodCalorieConversionFactor.food_nutrient_conversion_factor_id')
    # Relation to Food Nutrient model
    food_nutrient = relationship('FoodNutrient', foreign_keys='FoodNutrient.food_attribute_type_id')
    # Relation to Food Nutrient Conversion Factor model
    food_nutrient_conversion_factor = relationship('FoodNutrientConversionFactor', foreign_keys='FoodNutrientConversionFactor.id')
    # Relation to Lab Method Nutrient model
    lab_method_nutrient = relationship('LabMethodNutrient', foreign_keys='LabMethodNutrient.food_attribute_type_id')
    # Relation to Food Attribute model
    food_attribute = relationship('FoodAttribute', foreign_keys='FoodAttribute.food_attribute_type_id')
    # Relation to Food Component model
    food_component = relationship('FoodComponent', foreign_keys='FoodComponent.food_attribute_type_id')
    # Relation to Food Nutrient model
    food_nutrient = relationship('FoodNutrient', foreign_keys='FoodNutrient.food_attribute_type_id')
    # Relation to Lab Method model
    lab_method = relationship('LabMethod', foreign_keys='LabMethod.id')
    # Relation to Lab Method Code model
    lab_method_code = relationship('LabMethodCode', foreign_keys='LabMethodCode.lab_method_id')
    # Relation to Lab Method Nutrient model
    lab_method_nutrient = relationship('LabMethodNutrient', foreign_keys='LabMethodNutrient.food_attribute_type_id')

# Food Calorie Conversion Factor model
class FoodCalorieConversionFactor(Base):
    __tablename__ = "food_calorie_conversion_factor"

    food_nutrient_conversion_factor_id = Column(Float, primary_key=True)
    protein_value = Column(Float)
    fat_value = Column(Float)
    carbohydrate_value = Column(Float)

# Food Category Model
class FoodCategory(Base):
    __tablename__ = "food_category"

    id = Column(Integer, primary_key=True)
    code = Column(String)
    description = Column(String)

# Food Component Model
class FoodComponent(Base):
    __tablename__ = "food_component"

    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer)
    name = Column(String)
    pct_weight = Column(Float)
    is_refuse = Column(String)
    gram_weight = Column(Float)
    data_points = Column(Integer)
    min_year_acquired = Column(Float)

# Food Nutrient Model
class FoodNutrient(Base):
    __tablename__ = "food_nutrient"

    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer)
    nutrient_id = Column(Integer)
    amount = Column(Float)
    data_points = Column(Float)
    derivation_id = Column(Float)
    min = Column(Float)
    max = Column(Float)
    median = Column(Float)
    loq = Column(Float)
    footnote = Column(String)
    min_year_acquired = Column(Float)
    percent_daily_value = Column(Float)

# Food Nutrient Conversion Factor Model 
class FoodNutrientConversionFactor(Base):
    __tablename__ = "food_nutrient_conversion_factor"

    id = Column(Integer, primary_key=True)
    fdc_id = Column(Integer)

# Lab Method Model
class LabMethod(Base):
    __tablename__ = "lab_method"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    technique = Column(String)

# Lab Method Code Model
class LabMethodCode(Base):
    __tablename__ = "lab_method_code"

    lab_method_id = Column(Integer, primary_key=True)
    code = Column(String)

# Lab Method Nutrient Model
class LabMethodNutrient(Base):
    __tablename__ = "lab_method_nutrient"

    lab_method_id = Column(Integer, primary_key=True)
    nutrient_id = Column(Integer)

# Market Acquisition Model
class MarketAcquisition(Base):
    __tablename__ = "market_acquisition"

    fdc_id = Column(Integer, primary_key=True)
    brand_description = Column(String)
    expiration_date = Column(Date)
    label_weight = Column(Float)
    location = Column(String)
    acquisition_date = Column(Date)
    sales_type = Column(String)
    sample_lot_nbr = Column(String)
    sell_by_date = Column(Date)
    store_city = Column(String)
    store_name = Column(String)
    store_state = Column(String)
    upc_code = Column(String)

# Measure Unit Model
class MeasureUnit(Base):
    __tablename__ = "measure_unit"

    id = Column(Integer, primary_key=True)
    name = Column(String)

# Microbe Model
class Microbe(Base):
    __tablename__ = "microbe"

    id = Column(Integer, primary_key=True)
    foodId = Column(Integer)
    method = Column(String)
    microbe_code = Column(String)
    min_value = Column(Integer)
    max_value = Column(Float)
    uom = Column(String)

# Nutrient Model
class Nutrient(Base):
    __tablename__ = "nutrient"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit_name = Column(String)
    nutrient_nbr = Column(Float)
    rank = Column(Float)

# Retention Factor model
class RetentionFactor(Base):
    __tablename__ = "retention_factor"

    gid = Column(Integer, primary_key=True)
    code = Column(Integer)
    foodGroupId = Column(Integer)
    description = Column(String)

# Sample Food Model
class SampleFood(Base):
    __tablename__ = "sample_food"

    fdc_id = Column(Integer, primary_key=True)

# SR Legacy Food Model
class SRLegacyFood(Base):
    __tablename__ = "sr_legacy_food"

    fdc_id = Column(Integer, primary_key=True)
    NDB_number = Column(Integer)

# Sub-Sample Food Model
class SubSampleFood(Base):
    __tablename__ = "sub_sample_food"

    fdc_id = Column(Integer, primary_key=True)
    fdc_id_of_sample_food = Column(Integer)

# Sub Sample Result model
class SubSampleResult(Base):
    __tablename__ = "sub_sample_result"

    food_nutrient_id = Column(Integer, primary_key=True)
    adjusted_amount = Column(Float)
    lab_method_id = Column(Integer)
    nutrient_name = Column(String)

# Survey Fndds Food Model
class SurveyFnddsFood(Base):
    __tablename__ = "survey_fndds_food"

    fdc_id = Column(Integer, primary_key=True)
    food_code = Column(Integer)
    wweia_category_code = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)

# WWEIA Food Category model
class WWEIAFoodCategory(Base):
    __tablename__ = "wweia_food_category"

    wweia_food_category = Column(Integer, primary_key=True)
    wweia_food_category_description = Column(String)