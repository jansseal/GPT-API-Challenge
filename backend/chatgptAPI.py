from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv
import logging
import json
import time

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("recipe_api.log"),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    logging.error("OpenAI API key not found in environment variables")
    raise ValueError("OpenAI API key not configured")

client = OpenAI(api_key=api_key)


def format_prompt(ingredients, dietary_concerns):
    """Format the OpenAI prompt for recipe generation."""
    ingredient_string = ', '.join(ingredients) if isinstance(ingredients, list) else ingredients
    base_prompt = f"Create a recipe using some or all of these ingredients: {ingredient_string}."

    if dietary_concerns:
        base_prompt += f" The recipe must be suitable for a {dietary_concerns} diet."

    base_prompt += (
        " Ensure that you respond only with the criteria in the following JSON format: {"
        '"recipe_name": "Recipe Name", '
        '"cooking_time": "Cooking time in minutes", '
        '"ingredients": [{"ingredient": "name", "quantity": "amount", "unit": "unit of measurement"}], '
        '"instructions": ["Step 1", "Step 2", "Step 3"], '
        '"nutritional_info": {"calories": "value", "protein": "value", "fat": "value", "carbohydrates": "value"}, '
        '"cooking_tips": "Additional tips"'
        "}. Only include the JSON object with no extra text. Adhere strictly to this format."
    )
    return base_prompt


def validate_json(response_content):
    """Validate if the response content is a properly formatted JSON."""
    try:
        parsed_json = json.loads(response_content)
        # Ensure the JSON includes all required fields
        required_fields = ["recipe_name", "cooking_time", "ingredients", "instructions", "nutritional_info",
                           "cooking_tips"]
        if all(field in parsed_json for field in required_fields):
            return parsed_json
        else:
            logging.warning("Response JSON missing required fields")
            return None
    except json.JSONDecodeError:
        logging.warning("Response is not a valid JSON")
        return None


def generate_recipe(ingredients, dietary_concerns=None, retries=3, delay=2):
    """Generate a recipe using OpenAI with validation and retry logic."""
    for attempt in range(retries):
        try:
            logging.info(f"Generating recipe for ingredients: {ingredients}, Attempt: {attempt + 1}")
            prompt = format_prompt(ingredients, dietary_concerns)

            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional chef. Provide recipes in a structured JSON format with the following: "
                            "recipe_name, cooking_time, ingredients, instructions, nutritional_info (calories, protein, fat, carbohydrates), and cooking_tips."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # Lower temperature for deterministic output
                top_p=0.9
            )

            # Log token usage
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens

            logging.info(
                f"Token usage - Prompt: {prompt_tokens}, Completion: {completion_tokens}, Total: {total_tokens}")

            # Validate JSON response
            response_content = response.choices[0].message.content.strip()
            recipe = validate_json(response_content)
            if recipe:
                logging.info("Recipe successfully validated and received from OpenAI")
                return {"success": True, "recipe": recipe, "dietary_concerns": dietary_concerns or "None specified"}
            else:
                logging.warning("Invalid recipe format received, retrying...")

        except OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error in generate_recipe: {e}")

        # Retry logic
        time.sleep(delay)

    return {"success": False, "error": "Failed to generate a valid recipe after retries"}


if __name__ == "__main__":
    ingredients_list = ["tomatoes", "pasta", "garlic", "olive oil", "basil"]
    recipe = generate_recipe(ingredients_list)
    print(f"Generated Recipe: {json.dumps(recipe, indent=2)}")