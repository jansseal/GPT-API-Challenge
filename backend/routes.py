from flask import Blueprint, request, jsonify
from .chatgptAPI import generate_recipe

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return "GPT API Challenge"

@main.route('/api/generate-recipe', methods=['POST'])
def create_recipe():
    data = request.get_json()
    
    # Get the comma-separated string and parse it
    ingredients_string = data.get('ingredients', '')
    # Split by comma and strip whitespace from each ingredient
    ingredient_list = [ing.strip() for ing in ingredients_string.split(',') if ing.strip()]
    
    if not ingredient_list:
        return jsonify({"error": "No ingredients provided"}), 400
        
    recipe = generate_recipe(ingredient_list)
    return jsonify(recipe)

