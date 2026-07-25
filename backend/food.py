import re
import os

# Global variables
model_name = "Qwen/Qwen2.5-3B-Instruct"
pipeline = None
prompt_node = None


def initialize_pipeline():
    """
    Initialize the Haystack pipeline with the Qwen model.
    This function sets up the model, tokenizer, and pipeline.
    """
    global pipeline, prompt_node

    import torch
    from haystack import Pipeline
    from haystack.nodes import PromptNode

    print("Cuda available: ", torch.cuda.is_available())  # Should print: True
    print(f"Loading the {model_name} model and tokenizer")

    # Step 1: Setup the PromptNode using the Qwen model
    prompt_node = PromptNode(
        model_name_or_path=model_name,
        default_prompt_template="question-answering",
        # devices=["cuda:0"],
        devices=["cpu"],

    )
    print(f"Setup the PromptNode using the {model_name}")

    # Step 2: Create a Haystack pipeline and add the prompt node
    pipeline = Pipeline()
    pipeline.add_node(component=prompt_node, name="QwenPromptNode", inputs=["Query"])
    print("Created a Haystack pipeline and added the prompt node")

    return pipeline


def toggle_pipeline():
    """
    Toggle the pipeline initialization based on environment variable.
    Returns the pipeline instance if enabled, None otherwise.
    """
    global pipeline

    # Check if the pipeline should be enabled (default to True if not specified)
    pipeline_enabled = (
        os.environ.get("ENABLE_FOOD_MODEL_DEPLOYMENT", "true").lower() == "true"
    )

    if pipeline_enabled and pipeline is None:
        # Initialize the pipeline if it's enabled and not already initialized
        pipeline = initialize_pipeline()
    elif not pipeline_enabled:
        # If pipeline is disabled, set it to None
        pipeline = None
        print("Food analysis pipeline is disabled via environment variable")

    return pipeline


def analyze_food_query(sentence: str) -> str:
    """
    Analyze a food query and extract food items from it.

    Args:
        sentence: The input sentence to analyze

    Returns:
        A JSON string containing the extracted food items
    """
    # Ensure pipeline is initialized if enabled
    current_pipeline = toggle_pipeline()

    # If pipeline is disabled, return empty response
    if current_pipeline is None:
        print(
            "Food analysis pipeline is disabled. Enable it by setting ENABLE_FOOD_PIPELINE=true"
        )
        return ""

    # Example query
    # system_prompt = "Extract the food items from the sentence and return only a valid JSON array. Do not include any explanations, confirmations, or additional text. Only output JSON, like this: ['item1', 'item2']. Any other output format is invalid."
    system_prompt = """
    Extract the food items from the sentence and return a valid JSON array. 
    If a food item has ingredients or components (like a sandwich), represent it as a dictionary with keys for 'name' and 'ingredients'. 

    Example:
    Input: "I had a turkey sandwich with lettuce, tomato, and mustard. I also ate Lay's potato chips."
    Output: [
        {"name": "turkey sandwich", "ingredients": ["lettuce", "tomato", "mustard"]},
        "Lay's potato chips"
    ]
    """

    user_prompt = sentence
    final_prompt = f"System: {system_prompt}\nUser: {user_prompt}"
    print(f"Final prompt: {final_prompt}")
    # add system prompt

    # Get answers
    # result = pipeline.run(query=final_prompt, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}})
    result = current_pipeline.run(query=final_prompt)

    model_response = ""
    if not result or not result["answers"]:
        print("No answer found")
        return model_response
    # Display results
    for answer in result["answers"]:
        print(f"Answer: {answer.answer}, Score: {answer.score}")
        model_response = model_response + answer.answer

    return model_response


def analyze_food_sentence_locally(sentence: str) -> dict:
    """
    Lightweight natural-language food parser for local development.
    It intentionally returns estimates rather than pretending to know exact
    restaurant nutrition.
    """
    normalized = " ".join(sentence.lower().strip().split())
    cleaned = re.sub(r"^(i|we)\s+(had|ate|drank|got|ordered)\s+", "", normalized)

    portion = "1"
    for size in ["extra large", "small", "medium", "large", "venti", "grande", "tall"]:
        if re.search(rf"\b{re.escape(size)}\b", cleaned):
            portion = size
            break

    venue = None
    venue_match = re.search(r"\b(?:from|at)\s+(.+?)(?:\s+with\s+|$)", cleaned)
    if venue_match:
        venue = venue_match.group(1).strip()

    milk = None
    milk_match = re.search(
        r"\bwith\s+((?:whole|oat|almond|soy|skim|nonfat|2%|two percent)\s+milk)\b",
        cleaned,
    )
    if milk_match:
        milk = milk_match.group(1).replace("two percent", "2%")

    food_phrase = cleaned
    if venue:
        food_phrase = re.sub(rf"\b(?:from|at)\s+{re.escape(venue)}", "", food_phrase)
    if milk:
        food_phrase = re.sub(rf"\bwith\s+{re.escape(milk)}", "", food_phrase)
    food_phrase = re.sub(r"\b(a|an|the)\b", "", food_phrase).strip()
    food_phrase = re.sub(r"\s+", " ", food_phrase)

    category = "Food"
    calories = 350.0
    carbs = 35.0
    protein = 12.0
    fat = 12.0
    sugar = 12.0
    sodium = "250 mg"
    notes = []

    if "dirty chai" in food_phrase:
        category = "Drink"
        food_name = "iced dirty chai" if "iced" in food_phrase else "dirty chai"
        calories = 320.0
        carbs = 48.0
        protein = 10.0
        fat = 10.0
        sugar = 42.0
        sodium = "160 mg"
    elif "chai" in food_phrase:
        category = "Drink"
        food_name = "iced chai" if "iced" in food_phrase else "chai"
        calories = 260.0
        carbs = 44.0
        protein = 8.0
        fat = 7.0
        sugar = 38.0
        sodium = "140 mg"
    elif "latte" in food_phrase:
        category = "Drink"
        food_name = "iced latte" if "iced" in food_phrase else "latte"
        calories = 190.0
        carbs = 18.0
        protein = 10.0
        fat = 8.0
        sugar = 17.0
        sodium = "125 mg"
    elif "coffee" in food_phrase:
        category = "Drink"
        food_name = "iced coffee" if "iced" in food_phrase else "coffee"
        calories = 20.0
        carbs = 3.0
        protein = 1.0
        fat = 0.0
        sugar = 0.0
        sodium = "10 mg"
    elif "salad" in food_phrase:
        food_name = food_phrase
        calories = 420.0
        carbs = 24.0
        protein = 24.0
        fat = 24.0
        sugar = 8.0
        sodium = "620 mg"
    elif "sandwich" in food_phrase:
        food_name = food_phrase
        calories = 520.0
        carbs = 52.0
        protein = 28.0
        fat = 22.0
        sugar = 7.0
        sodium = "980 mg"
    else:
        food_name = food_phrase or sentence.strip()
        notes.append("Nutrition is a broad estimate from the sentence.")

    if portion in ["large", "extra large", "venti"]:
        calories *= 1.2
        carbs *= 1.2
        protein *= 1.15
        fat *= 1.15
        sugar *= 1.2
    elif portion in ["small", "tall"]:
        calories *= 0.75
        carbs *= 0.75
        protein *= 0.8
        fat *= 0.8
        sugar *= 0.75

    if milk == "whole milk":
        notes.append("Includes whole milk estimate.")
    elif milk in [
        "oat milk",
        "soy milk",
        "almond milk",
        "skim milk",
        "nonfat milk",
        "2% milk",
    ]:
        notes.append(f"Includes {milk} estimate.")

    if venue:
        notes.append(f"Venue: {venue.title()}.")

    if portion not in ["1", "medium"]:
        food_name = f"{portion} {food_name}"

    return {
        "food_name": food_name,
        "category": category,
        "portion_size": {
            "amount": portion,
            "unit": "serving" if category == "Food" else "drink",
        },
        "calories_per_portion": round(calories),
        "macronutrients": {
            "carbohydrates": round(carbs, 1),
            "proteins": round(protein, 1),
            "fats": round(fat, 1),
        },
        "micronutrients": {},
        "fiber_content": "",
        "sugar": {"added": f"{round(sugar, 1)} g", "natural": ""},
        "cholesterol": "",
        "sodium": sodium,
        "fats": {
            "saturated_fats": f"{round(fat * 0.55, 1)} g",
            "trans_fats": "0 g",
        },
        "common_allergens": ["milk"] if milk else [],
        "dietary_tags": [],
        "custom_recipes": [],
        "favorite_foods": [],
        "user_notes": " ".join(notes) or "Estimated from natural-language entry.",
        "time_and_date": None,
        "estimated": True,
        "source_sentence": sentence,
    }
