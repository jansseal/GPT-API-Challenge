from flask import Blueprint, request, jsonify
from .chatgptAPI import generate_recipe
import logging

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return "GPT API Challenge"

@main.route('/api/generate-recipe', methods=['POST'])
def create_recipe():
    try:
        data = request.get_json()
        ingredients_string = data.get('ingredients', '') # I'm imagining this is a list of ingredients
        ingredient_list = [ing.strip() for ing in ingredients_string.split(',') if ing.strip()] # input sanitization
        
        if not ingredient_list:
            logging.warning("No ingredients provided in request")
            return jsonify({"error": "No ingredients provided"}), 400
            
        recipe = generate_recipe(ingredient_list)
        
        if not recipe.get('success'):
            logging.error(f"Failed to generate recipe: {recipe.get('error')}")
            return jsonify(recipe), 500
            
        logging.info("Successfully processed recipe request")
        
        return jsonify(recipe)
    
    except Exception as e:
        logging.error(f"Error in create_recipe: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@main.route('/api/generate-recipe-from-fridge', methods=['POST']) 
def generate_recipe_from_fridge():
    data = request.get_json()
    ingredients = data.get('fridge_ingredients', []) # I'm imagining this is a list of ingredients

    if not ingredients:
        return jsonify({"error": "No ingredients provided from fridge"}), 400

    recipe = generate_recipe(ingredients)
    return jsonify(recipe)
