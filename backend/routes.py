from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from backend import db
from .models import User, Ingredient, Recipe

main = Blueprint('main', __name__)


# Existing user login (with password verification)
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        user = User.query.filter_by(user_email=data['user_email']).first()
        if user and check_password_hash(
            user.user_password,
            data['user_password']
        ):
            return jsonify({
                'id': user.user_id,
                'user_name': user.user_name}), 200
        return jsonify({'message': 'Invalid email or password'}), 401
    except Exception as e:
        print(f'Error on login route: {str(e)}')
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        db.session.close()


# Add a new user (with password hashing)
@main.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    try:
        new_user = User(
            user_name=data['user_name'],
            user_email=data['user_email'],
            user_password=['user_password']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'id': new_user.user_id,
            'user_name': new_user.user_name}), 201
    except Exception as e:
        print(f'Error on add_user route: {str(e)}')
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        db.session.close()


# Fetch user account information by ID
@main.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'user_name': user.user_name,
                'user_email': user.user_email}), 200
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        print(f'Error on get_user route: {str(e)}')
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        db.session.close()


# Update a user by ID (with password verification and/or hashing)
@main.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            data = request.get_json()

            # Verify the existing password for security before allowing updates
            if 'current_user_password' not in data or not check_password_hash(
                user.user_password,
                data['current_user_password']
            ):
                return jsonify({
                    'message': 'Current password is incorrect'}), 403

            # Update user_name if provided
            user.user_name = data.get('user_name', user.user_name)

            # Update password if provided
            if 'new_user_password' in data:
                user.user_password = generate_password_hash(
                    data['new_user_password']
                )

            db.session.commit()
            return jsonify({
                'id': user.user_id, 'user_name': user.user_name}), 200
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        print(f'Error on update_user route: {str(e)}')
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        db.session.close()


# Delete a user by ID
@main.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        print(f'Error on delete_user route: {str(e)}')
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        db.session.close()


# Add a new ingredient
@main.route('/ingredients', methods=['POST'])
def add_ingredient():
    data = request.get_json()
    try:
        new_ingredient = Ingredient(
            ingredient_name=data['ingredient_name'],
            user_id=data['user_id']
        )
        db.session.add(new_ingredient)
        db.session.commit()
        return jsonify({
            'id': new_ingredient.ingredient_id,
            'name': new_ingredient.ingredient_name}), 201
    except Exception as e:
        print(f'Error on add_ingredient route: {str(e)}')
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        db.session.close()


# Fetch all ingredients tied to a user's account
@main.route('/ingredients/<int:user_id>', methods=['GET'])
def get_ingredients(user_id):
    try:
        ingredients = Ingredient.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': ing.ingredient_id,
            'name': ing.ingredient_name}
            for ing in ingredients]), 200
    except Exception as e:
        print(f'Error on get_ingredients route: {str(e)}')
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        db.session.close()


# Delete an ingredient by ID
@main.route('/ingredients/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        if ingredient:
            db.session.delete(ingredient)
            db.session.commit()
            return jsonify({'message': 'Ingredient deleted successfully'}), 200
        return jsonify({'message': 'Ingredient not found'}), 404
    except Exception as e:
        print(f'Error on delete_ingredients route: {str(e)}')
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        db.session.close()    


# Add a new recipe
@main.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    try:
        new_recipe = Recipe(
            recipe_name=data['recipe_name'],
            recipe_cooktime=data['recipe_cooktime'],
            recipe_instructions=data['recipe_instructions'],
            user_id=data['user_id']
        )
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify({
            'id': new_recipe.recipe_id,
            'name': new_recipe.recipe_name}), 201
    except Exception as e:
        print(f'Error on add_recipe route: {str(e)}')
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        db.session.close()


# Fetch all recipes favorited by a user
@main.route('/recipes/<int:user_id>', methods=['GET'])
def get_recipes(user_id):
    try:
        recipes = Recipe.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': recipe.recipe_id,
            'name': recipe.recipe_name,
            'cooktime': recipe.recipe_cooktime,
            'instructions': recipe.recipe_instructions}
            for recipe in recipes]), 200
    except Exception as e:
        print(f'Error on get_recipes route: {str(e)}')
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        db.session.close()


# Fetch a favorite recipe by ID
@main.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    try:
        recipe = Recipe.query.get(recipe_id)
        if recipe:
            return jsonify({
                'id': recipe.recipe_id,
                'name': recipe.recipe_name,
                'cooktime': recipe.recipe_cooktime,
                'instructions': recipe.recipe_instructions}), 200
        return jsonify({'message': 'Recipe not found'}), 404
    except Exception as e:
        print(f'Error on get_recipe route: {str(e)}')
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        db.session.close()


# Delete a favorite recipe by ID
@main.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    try:
        recipe = Recipe.query.get(recipe_id)
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return jsonify({'message': 'Recipe deleted successfully'}), 200
        return jsonify({'message': 'Recipe not found'}), 404
    except Exception as e:
        print(f'Error on delete_recipe route: {str(e)}')
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        db.session.close()
