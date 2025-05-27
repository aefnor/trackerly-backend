from haystack.nodes import PromptNode
from haystack import Pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
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

    print("Cuda available: ", torch.cuda.is_available())  # Should print: True
    print(f"Loading the {model_name} model and tokenizer")

    # Step 1: Setup the PromptNode using the Qwen model
    prompt_node = PromptNode(
        model_name_or_path=model_name,
        default_prompt_template="question-answering",
        devices=["cuda:0"],
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
