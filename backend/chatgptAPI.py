from flask import Flask, request, jsonify
from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv
import logging

# logger config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('recipe_api.log'),
        logging.StreamHandler()  
    ]
)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    logging.error("OpenAI API key not found in environment variables")
    raise ValueError("OpenAI API key not configured")

client = OpenAI(api_key=api_key)

def generate_recipe(ingredients, dietary_concerns=None):
    try:
        logging.info(f"Generating recipe for: {ingredients}")
        
        # Convert ingredients to string regardless of input type
        if isinstance(ingredients, list):
            ingredient_string = ', '.join(ingredients)
        else:
            ingredient_string = ingredients
            
        # Build prompt with dietary concerns if provided
        base_prompt = f"Create a recipe using some or all of these ingredients: {ingredient_string}."
        if dietary_concerns:
            base_prompt += f" The recipe must be suitable for {dietary_concerns} diet."
        
        prompt = base_prompt + " Include cooking time, ingredients with quantities, and step-by-step instructions."
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional chef. Provide recipes in a structured format with cooking time, ingredients list, and clear instructions. Including cooking tips and nutritional information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        recipe = response.choices[0].message.content
        logging.info("Successfully received recipe from OpenAI")
        return {
            "success": True,
            "recipe": recipe,
            "dietary_concerns": dietary_concerns if dietary_concerns else "None specified"
        }

    except OpenAIError as e:
        logging.error(f"OpenAI API error: {str(e)}")
        return {"success": False, "error": "Failed to contact OpenAI service"}
    except Exception as e:
        logging.error(f"Unexpected error in generate_recipe: {str(e)}")
        return {"success": False, "error": "Internal server error"}

if __name__ == "__main__":
    ingredients_list = ["tomatoes", "pasta", "garlic", "olive oil", "basil"]
    recipe = generate_recipe(ingredients_list, dietary_concerns=None)
    print(f"Generated Recipe: {recipe}")