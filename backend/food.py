from haystack.nodes import PromptNode
from haystack import Pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

print("Cuda available: ", torch.cuda.is_available())  # Should print: True
# Step 1: Load the Qwen-2.5 (32B version) model and tokenizer
model_name = "Qwen/Qwen2.5-3B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)
print("Loaded the Qwen-2.5 (3B version) model and tokenizer")

# Step 2: Setup the PromptNode using the Qwen-2.5 model
prompt_node = PromptNode(model_name_or_path=model_name, default_prompt_template="question-answering", devices=["cuda:0"])
print("Setup the PromptNode using the Qwen-2.5 model")
# Step 3: Create a Haystack pipeline and add the prompt node
pipeline = Pipeline()
pipeline.add_node(component=prompt_node, name="QwenPromptNode", inputs=["Query"])
print("Created a Haystack pipeline and added the prompt node")

def analyze_food_query(sentence: str) -> str:
    # Example query
    system_prompt = "Extract the food items from the sentence and return only a valid JSON array. Do not include any explanations, confirmations, or additional text. Only output JSON, like this: ['item1', 'item2']. Any other output format is invalid."

    user_prompt = sentence
    final_prompt = f"System: {system_prompt}\nUser: {user_prompt}"
    # add system prompt

    # Get answers
    # result = pipeline.run(query=final_prompt, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}})
    result = pipeline.run(query=final_prompt)


    # Display results
    for answer in result['answers']:
        print(f"Answer: {answer.answer}, Score: {answer.score}")
