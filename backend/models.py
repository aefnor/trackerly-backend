import hashlib
from pydantic import validator
from sqlalchemy import Column, Date, Float, String, Integer, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import ForeignKey

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


# # Food Model
# class Food(Base):
#     __tablename__ = "food"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     fdc_id = Column(Integer)
#     data_type = Column(String)
#     description = Column(String)
#     food_category_id = Column(String)
#     publication_date = Column(Date)

#     # Relationships
#     # acquisition_samples_as_sample = relationship('AcquisitionSamples', foreign_keys='AcquisitionSamples.fdc_id_of_sample_food', back_populates='sample_food')
#     # acquisition_samples_as_acquisition = relationship('AcquisitionSamples', foreign_keys='AcquisitionSamples.fdc_id_of_acquisition_food', back_populates='acquisition_food')
#     # agricultural_samples = relationship('AgriculturalSamples', back_populates='food')
#     # branded_food = relationship('BrandedFoods', uselist=False, back_populates='food')
#     # food_attributes = relationship('FoodAttribute', back_populates='food')
#     # food_components = relationship('FoodComponent', back_populates='food')
#     # food_nutrients = relationship('FoodNutrient', back_populates='food')
#     # food_calorie_conversion_factors = relationship('FoodCalorieConversionFactor', back_populates='food')
#     # Add other relationships as necessary

# # Food Category Model
# class FoodCategory(Base):
#     __tablename__ = "food_category"

#     id = Column(Integer, primary_key=True)
#     code = Column(String)
#     description = Column(String)

# # Acquisition Samples Model
# class AcquisitionSamples(Base):
#     __tablename__ = "acquisition_samples"

#     fdc_id_of_sample_food = Column(Integer, primary_key=True)
#     fdc_id_of_acquisition_food = Column(Integer)

#     # Relationships
#     # sample_food = relationship('Food', foreign_keys=[fdc_id_of_sample_food], back_populates='acquisition_samples_as_sample')
#     # acquisition_food = relationship('Food', foreign_keys=[fdc_id_of_acquisition_food], back_populates='acquisition_samples_as_acquisition')

# # Agricultural Samples Model
# class AgriculturalSamples(Base):
#     __tablename__ = "agricultural_samples"

#     fdc_id = Column(Integer, primary_key=True)
#     acquisition_date = Column(Date)
#     market_class = Column(String)
#     treatment = Column(String)
#     state = Column(String)

#     # Relationships
#     food = relationship('Food', back_populates='agricultural_samples')

# # Branded Food Model
# class BrandedFoods(Base):
#     __tablename__ = "branded_foods"

#     fdc_id = Column(Integer, primary_key=True)
#     brand_owner = Column(String)
#     brand_name = Column(String)
#     subbrand_name = Column(String)
#     gtin_upc = Column(String)
#     ingredients = Column(String)
#     serving_size = Column(Float)
#     serving_size_unit = Column(String)
#     household_serving_fulltext = Column(String)
#     branded_food_category = Column(String)
#     data_source = Column(String)
#     package_weight = Column(Float)
#     modified_date = Column(Date)
#     available_date = Column(Date)
#     market_country = Column(String)
#     discontinued_date = Column(Date)
#     preparation_state_code = Column(String)
#     trade_channel = Column(String)
#     short_description = Column(String)

#     # Relationships
#     # food = relationship('Food', back_populates='branded_food')

# # Food Attribute Model
# class FoodAttribute(Base):
#     __tablename__ = "food_attribute"

#     id = Column(Integer, primary_key=True)
#     fdc_id = Column(Integer)
#     seq_num = Column(Float)
#     food_attribute_type_id = Column(Integer, ForeignKey('food_attribute_type.id'))
#     name = Column(String)
#     value = Column(String)

#     # Relationships
#     # food = relationship('Food', back_populates='food_attributes')
#     # food_attribute_type = relationship('FoodAttributeType', back_populates='food_attributes')

# class InputFood(Base):
#     __tablename__ = "input_food"

#     id = Column(Integer, primary_key=True)
#     fdc_id = Column(Integer)
#     fdc_id_of_input_food = Column(Integer)
#     seq_num = Column(Integer)
#     amount = Column(Float)
#     sr_code = Column(Integer, ForeignKey('sr_legacy_food.NDB_number'), nullable=True)
#     sr_description = Column(String)
#     unit = Column(String)
#     portion_code = Column(Integer)
#     portion_description = Column(String)
#     gram_weight = Column(Float)
#     retention_code = Column(Integer, ForeignKey('retention_factor.code'), nullable=True)

#     # Relationships
#     # parent_food = relationship('Food', foreign_keys=[fdc_id], back_populates='input_foods')
#     # component_food = relationship('Food', foreign_keys=[fdc_id_of_input_food], back_populates='input_food_components')
#     # sr_legacy_food = relationship('SRLegacyFood', foreign_keys=[sr_code], back_populates='input_foods')
#     # retention_factor = relationship('RetentionFactor', foreign_keys=[retention_code], back_populates='input_foods')


# # Food Attribute Type Model
# class FoodAttributeType(Base):
#     __tablename__ = "food_attribute_type"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     description = Column(String)

#     # Relationships
#     food_attributes = relationship('FoodAttribute', back_populates='food_attribute_type')

# # Food Calorie Conversion Factor Model
# class FoodCalorieConversionFactor(Base):
#     __tablename__ = "food_calorie_conversion_factor"

#     id = Column(Integer, primary_key=True)
#     fdc_id = Column(Integer)
#     protein_value = Column(Float)
#     fat_value = Column(Float)
#     carbohydrate_value = Column(Float)

#     # Relationships
#     food = relationship('Food', back_populates='food_calorie_conversion_factors')

# # Food Component Model
# class FoodComponent(Base):
#     __tablename__ = "food_component"

#     id = Column(Integer, primary_key=True)
#     fdc_id = Column(Integer)
#     name = Column(String)
#     pct_weight = Column(Float)
#     is_refuse = Column(String)
#     gram_weight = Column(Float)
#     data_points = Column(Integer)
#     min_year_acquired = Column(Float)

#     # Relationships
#     food = relationship('Food', back_populates='food_components')

# # Food Nutrient Model
# class FoodNutrient(Base):
#     __tablename__ = "food_nutrient"

#     id = Column(Integer, primary_key=True)
#     fdc_id = Column(Integer)
#     nutrient_id = Column(Integer, ForeignKey('nutrient.id'))
#     amount = Column(Float)
#     data_points = Column(Float)
#     derivation_id = Column(String, ForeignKey('fndds_derivation.derivation_code'))
#     min = Column(Float)
#     max = Column(Float)
#     median = Column(Float)
#     loq = Column(Float)
#     footnote = Column(String)
#     min_year_acquired = Column(Float)
#     percent_daily_value = Column(Float)

#     # Relationships
#     food = relationship('Food', back_populates='food_nutrients')
#     nutrient = relationship('Nutrient', back_populates='food_nutrients')
#     derivation = relationship('FnddsDerivation', back_populates='food_nutrients')

# # Nutrient Model
# class Nutrient(Base):
#     __tablename__ = "nutrient"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     unit_name = Column(String)
#     nutrient_nbr = Column(Float)
#     rank = Column(Float)

#     # Relationships
#     food_nutrients = relationship('FoodNutrient', back_populates='nutrient')
#     lab_method_nutrients = relationship('LabMethodNutrient', back_populates='nutrient')

# # Fndds Derivation Model
# class FnddsDerivation(Base):
#     __tablename__ = "fndds_derivation"

#     derivation_code = Column(String, primary_key=True)
#     derivation_description = Column(String)

#     # Relationships
#     food_nutrients = relationship('FoodNutrient', back_populates='derivation')
#     lab_method_nutrients = relationship('LabMethodNutrient', back_populates='derivation')

# # Lab Method Model
# class LabMethod(Base):
#     __tablename__ = "lab_method"

#     id = Column(Integer, primary_key=True)
#     description = Column(String)
#     technique = Column(String)

#     # Relationships
#     lab_method_nutrients = relationship('LabMethodNutrient', back_populates='lab_method')
#     lab_method_codes = relationship('LabMethodCode', back_populates='lab_method')

# # Lab Method Code Model
# class LabMethodCode(Base):
#     __tablename__ = "lab_method_code"

#     id = Column(Integer, primary_key=True)
#     lab_method_id = Column(Integer, ForeignKey('lab_method.id'))
#     code = Column(String)

#     # Relationships
#     lab_method = relationship('LabMethod', back_populates='lab_method_codes')

# # Lab Method Nutrient Model
# class LabMethodNutrient(Base):
#     __tablename__ = "lab_method_nutrient"

#     id = Column(Integer, primary_key=True)
#     lab_method_id = Column(Integer, ForeignKey('lab_method.id'))
#     nutrient_id = Column(Integer, ForeignKey('nutrient.id'))
#     derivation_id = Column(String, ForeignKey('fndds_derivation.derivation_code'))

#     # Relationships
#     lab_method = relationship('LabMethod', back_populates='lab_method_nutrients')
#     nutrient = relationship('Nutrient', back_populates='lab_method_nutrients')
#     derivation = relationship('FnddsDerivation', back_populates='lab_method_nutrients')

# # Market Acquisition Model
# class MarketAcquisition(Base):
#     __tablename__ = "market_acquisition"

#     fdc_id = Column(Integer, primary_key=True)
#     brand_description = Column(String)
#     expiration_date = Column(Date)
#     label_weight = Column(Float)
#     location = Column(String)
#     acquisition_date = Column(Date)
#     sales_type = Column(String)
#     sample_lot_nbr = Column(String)
#     sell_by_date = Column(Date)
#     store_city = Column(String)
#     store_name = Column(String)
#     store_state = Column(String)
#     upc_code = Column(String)

#     # Relationships
#     food = relationship('Food', back_populates='market_acquisition')

# # Food Model (update to include market acquisition relationship)
# Food.market_acquisition = relationship('MarketAcquisition', uselist=False, back_populates='food')

# # Measure Unit Model
# class MeasureUnit(Base):
#     __tablename__ = "measure_unit"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)

#     # Relationships
#     # Define relationships if any (not specified in initial code)

# # Microbe Model
# class Microbe(Base):
#     __tablename__ = "microbe"

#     id = Column(Integer, primary_key=True)
#     food_id = Column(Integer)
#     method = Column(String)
#     microbe_code = Column(String)
#     min_value = Column(Integer)
#     max_value = Column(Float)
#     uom = Column(String)

#     # Relationships
#     food = relationship('Food', back_populates='microbes')

# # Food Model (update to include microbes relationship)
# Food.microbes = relationship('Microbe', back_populates='food')

# # Retention Factor Model
# class RetentionFactor(Base):
#     __tablename__ = "retention_factor"

#     code = Column(Integer, primary_key=True)  # Set as primary key
#     gid = Column(Integer)
#     food_group_id = Column(Integer)
#     description = Column(String)

#     # Relationships
#     input_foods = relationship('InputFood', back_populates='retention_factor')

# # Sample Food Model
# class SampleFood(Base):
#     __tablename__ = "sample_food"

#     fdc_id = Column(Integer, primary_key=True)

#     # Relationships
#     food = relationship('Food', back_populates='sample_food')

# # Food Model (update to include sample food relationship)
# Food.sample_food = relationship('SampleFood', uselist=False, back_populates='food')

# # SR Legacy Food Model
# class SRLegacyFood(Base):
#     __tablename__ = "sr_legacy_food"

#     fdc_id = Column(Integer, primary_key=True)
#     NDB_number = Column(Integer, unique=True)  # Add unique constraint

#     # Relationships
#     food = relationship('Food', back_populates='sr_legacy_food')
#     input_foods = relationship('InputFood', foreign_keys='InputFood.sr_code', back_populates='sr_legacy_food')


# # Food Model (update to include SR Legacy Food relationship)
# Food.sr_legacy_food = relationship('SRLegacyFood', uselist=False, back_populates='food')

# # Sub-Sample Food Model
# class SubSampleFood(Base):
#     __tablename__ = "sub_sample_food"

#     fdc_id = Column(Integer, primary_key=True)
#     fdc_id_of_sample_food = Column(Integer)

#     # Relationships
#     food = relationship('Food', foreign_keys=[fdc_id], back_populates='sub_sample_foods')
#     sample_food = relationship('Food', foreign_keys=[fdc_id_of_sample_food])

# # Food Model (update to include sub-sample food relationship)
# Food.sub_sample_foods = relationship('SubSampleFood', foreign_keys='SubSampleFood.fdc_id', back_populates='food')

# # Sub-Sample Result Model
# class SubSampleResult(Base):
#     __tablename__ = "sub_sample_result"

#     id = Column(Integer, primary_key=True)
#     food_nutrient_id = Column(Integer, ForeignKey('food_nutrient.id'))
#     adjusted_amount = Column(Float)
#     lab_method_id = Column(Integer, ForeignKey('lab_method.id'))
#     nutrient_name = Column(String)

#     # Relationships
#     food_nutrient = relationship('FoodNutrient', back_populates='sub_sample_results')
#     lab_method = relationship('LabMethod', back_populates='sub_sample_results')

# # Food Nutrient Model (update to include sub-sample results)
# FoodNutrient.sub_sample_results = relationship('SubSampleResult', back_populates='food_nutrient')

# # Lab Method Model (update to include sub-sample results)
# LabMethod.sub_sample_results = relationship('SubSampleResult', back_populates='lab_method')

# # Survey FNDDS Food Model
# class SurveyFnddsFood(Base):
#     __tablename__ = "survey_fndds_food"

#     fdc_id = Column(Integer, primary_key=True)
#     food_code = Column(Integer)
#     wweia_category_code = Column(Integer, ForeignKey('wweia_food_category.wweia_food_category'))
#     start_date = Column(Date)
#     end_date = Column(Date)

#     # Relationships
#     food = relationship('Food', back_populates='survey_fndds_food')
#     wweia_food_category = relationship('WWEIAFoodCategory', back_populates='survey_fndds_foods')

# # Food Model (update to include survey FNDDS food relationship)
# Food.survey_fndds_food = relationship('SurveyFnddsFood', uselist=False, back_populates='food')

# # WWEIA Food Category Model
# class WWEIAFoodCategory(Base):
#     __tablename__ = "wweia_food_category"

#     wweia_food_category = Column(Integer, primary_key=True)
#     wweia_food_category_description = Column(String)

#     # Relationships
#     survey_fndds_foods = relationship('SurveyFnddsFood', back_populates='wweia_food_category')

# # Complete any additional relationships as necessary for other models.

# # Note: For classes like MeasureUnit, RetentionFactor, and others where relationships were not specified, add relationships based on the actual database schema and requirements.
