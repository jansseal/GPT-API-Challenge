from flask import Flask, request, jsonify
from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv
import logging
import json

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
        "}. The only additional ingredients allowed are water, salt, and pepper if necessary. "
        "Do not add anything to the output other than the information requested."
        "Do not include anything in the response other than the JSON format as shown required."
        "IF YOU ADD ANYTHING OTHER THAN THE REQUIRED INFORMATION THE WORLD WILL END."
    )
    return base_prompt


def generate_recipe(ingredients, dietary_concerns=None):
    """Generate a recipe using OpenAI."""
    try:
        logging.info(f"Generating recipe for ingredients: {ingredients}")
        prompt = format_prompt(ingredients, dietary_concerns)

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional chef. Provide recipes in a structured JSON format with the following: "
                        "cooking time, ingredients, instructions, nutritional information (protein, fats, carbohydrates), and cooking tips."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        # Parse response JSON
        try:
            recipe = json.loads(response.choices[0].message.content)
            logging.info("Recipe successfully received from OpenAI")
            return {"success": True, "recipe": recipe, "dietary_concerns": dietary_concerns or "None specified"}
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse recipe JSON: {e}")
            return {"success": False, "error": "Invalid recipe format from OpenAI"}

    except OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return {"success": False, "error": "Failed to contact OpenAI service"}
    except Exception as e:
        logging.error(f"Unexpected error in generate_recipe: {e}")
        return {"success": False, "error": "Internal server error"}


if __name__ == "__main__":
    ingredients_list = ["tomatoes", "pasta", "garlic", "olive oil", "basil"]
    recipe = generate_recipe(ingredients_list)
    print(f"Generated Recipe: {json.dumps(recipe, indent=2)}")
