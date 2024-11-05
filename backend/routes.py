from flask import Blueprint, request, jsonify
from .chatgptAPI import generate_recipe

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return "GPT API Challenge"

@main.route('/api/generate-recipe', methods=['POST'])
def create_recipe():
    data = request.get_json()
    
    ingredients_string = data.get('ingredients', '') # I'm imagining this is a comma separated string of ingredients

    ingredient_list = [ing.strip() for ing in ingredients_string.split(',') if ing.strip()]
    
    if not ingredient_list:
        return jsonify({"error": "No ingredients provided"}), 400
        
    recipe = generate_recipe(ingredient_list)
    return jsonify(recipe)


@main.route('/api/generate-recipe-from-fridge', methods=['POST']) 
def generate_recipe_from_fridge():
    data = request.get_json()
    ingredients = data.get('fridge_ingredients', []) # I'm imagining this is a list of ingredients

    if not ingredients:
        return jsonify({"error": "No ingredients provided from fridge"}), 400

    recipe = generate_recipe(ingredients)
    return jsonify(recipe)
