from flask import Blueprint, request, jsonify, session, send_from_directory
from .chatgptAPI import generate_recipe
import logging
from werkzeug.security import check_password_hash
from backend import db
from .models import User, Ingredient, Recipe
from sqlalchemy.exc import IntegrityError

main = Blueprint('main', __name__)


@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def catch_all(path):
    return send_from_directory('static', 'index.html')


@main.route('/api/generate-recipe', methods=['POST'])
def create_recipe():
    try:
        data = request.get_json()

        ingredients_string = data.get('ingredients', '')  # Expecting a string
        dietary_concerns = data.get('dietary_concerns')

        if not ingredients_string or not isinstance(ingredients_string, str):
            logging.warning("No ingredients string provided in request")
            return jsonify({"error": "Please provide ingredients as a "
                            "comma-separated string"}), 400

        recipe = generate_recipe(
            ingredients=ingredients_string,
            dietary_concerns=dietary_concerns
        )

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
    try:
        data = request.get_json()
        ingredients_list = data.get(
            'fridge_ingredients', [])  # Expecting a list
        dietary_concerns = data.get('dietary_concerns')

        if not ingredients_list or not isinstance(ingredients_list, list):
            logging.warning("No ingredients list provided in request")
            return jsonify(
                {"error": "Please provide ingredients as a list"}), 400

        recipe = generate_recipe(
            ingredients=ingredients_list,
            dietary_concerns=dietary_concerns
        )

        if not recipe.get('success'):
            logging.error(f"Failed to generate recipe: {recipe.get('error')}")
            return jsonify(recipe), 500

        logging.info("Successfully processed recipe from fridge request")
        return jsonify(recipe)

    except Exception as e:
        logging.error(f"Error in generate_recipe_from_fridge: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


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
            session['user_id'] = user.user_id
            logging.info(f'User "{user.user_email}" logged in successfully.')
            return jsonify({
                'id': user.user_id,
                'user_name': user.user_name}), 200

        logging.warning(
            f'Invalid login attempt for email: "{data["user_email"]}".'
        )
        return jsonify({'message': 'Invalid email or password'}), 401

    except Exception as e:
        db.session.rollback()
        logging.error(f'Error on login route: {str(e)}.')
        return jsonify({'message': 'Internal server error'}), 500

    finally:
        db.session.close()


# User logout
@main.route('/logout', methods=['POST'])
def logout():
    try:
        if 'user_id' in session:
            # Remove user_id from and clear the entire session
            user_id = session.pop('user_id', None)
            session.clear()
            logging.info(f'User with ID {user_id} logged out successfully.')
            return jsonify({'message': 'Logout successful'}), 200
        else:
            logging.warning('Logout attempt without an active session.')
            return jsonify({'message': 'No active session found'}), 400

    except Exception as e:
        logging.error(f'Error on logout route: {str(e)}.')
        return jsonify({'message': 'Internal server error'}), 500


# Add a new user
@main.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    try:
        new_user = User(
            user_name=data['user_name'],
            user_email=data['user_email'],
            user_password=data['user_password']
        )
        db.session.add(new_user)
        db.session.commit()
        logging.info(f'User "{new_user.user_email}" created successfully.')
        return jsonify({
            'id': new_user.user_id,
            'user_name': new_user.user_name,
            'user_email': new_user.user_email}), 201

    except IntegrityError:
        db.session.rollback()
        logging.warning(f'Duplicate email attempted: {data["user_email"]}')
        return jsonify({'message': 'User email must be unique'}), 400

    except Exception as e:
        db.session.rollback()
        logging.error(f'Error on add_user route: {str(e)}.')
        return jsonify({'message': 'Internal server error'}), 500

    finally:
        db.session.close()


# Fetch user account information by ID
@main.route('/users', methods=['GET'])
def get_user():
    try:
        # Get user_id from session
        user_id = session.get('user_id')
        if not user_id:
            logging.warning(
                'Attempt to access user info without an active session.'
            )
            return jsonify({'message': 'Unauthorized. Please log in.'}), 401

        user = User.query.get(user_id)
        if user:
            logging.info(
                f'User "{user.user_email}" account information loaded'
                f' successfully.'
            )
            return jsonify({
                'user_name': user.user_name,
                'user_email': user.user_email}), 200

        logging.warning(f'User with ID #{user_id} not found.')
        return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        logging.error(f'Error on get_user route: {str(e)}.')
        return jsonify({'message': 'Internal server error'}), 500

    finally:
        db.session.close()


# Update a user by ID (with password verification)
@main.route('/users', methods=['PUT'])
def update_user():
    try:
        # Get user_id from session
        user_id = session.get('user_id')
        if not user_id:
            logging.warning(
                'Attempt to update user info without an active session.'
            )
            return jsonify({'message': 'Unauthorized. Please log in.'}), 401

        user = User.query.get(user_id)
        if user:
            data = request.get_json()

            # Verify the existing password for security before allowing updates
            if 'current_user_password' not in data or not check_password_hash(
                user.user_password,
                data['current_user_password']
            ):
                logging.warning(
                    f'User "{user.user_email}" entered an incorrect current '
                    f'password.'
                )
                return jsonify({
                    'message': 'Current password is incorrect'}), 403

            # Update user_name if provided
            user.user_name = data.get('user_name', user.user_name)

            # Update password if provided
            if 'new_user_password' in data:
                user.user_password = data['new_user_password']

            db.session.commit()
            logging.info(
                f'User "{user.user_email}" updated account name and/or '
                f'password successfully.'
            )
            return jsonify({
                'id': user.user_id, 'user_name': user.user_name}), 200

        db.session.rollback()
        logging.warning(f'User with ID #{user_id} not found.')
        return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        db.session.rollback()
        logging.error(f'Error on update_user route: {str(e)}.')
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        db.session.close()


# Delete a user by ID
@main.route('/users', methods=['DELETE'])
def delete_user():
    try:
        # Get user_id from session
        user_id = session.get('user_id')
        if not user_id:
            logging.warning(
                'Attempt to delete user without an active session.'
            )
            return jsonify({'message': 'Unauthorized. Please log in.'}), 401

        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            logging.info(f'User "{user.user_email}" deleted successfully.')
            return jsonify({'message': 'User deleted successfully'}), 200

        db.session.rollback()
        logging.warning(f'User with ID #{user_id} not found.')
        return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        db.session.rollback()
        logging.error(f'Error on delete_user route: {str(e)}.')
        return jsonify({'message': 'Internal server error'}), 500

    finally:
        db.session.close()


# Add a new ingredient
@main.route('/ingredients', methods=['POST'])
def add_ingredient():
    data = request.get_json()
    try:
        # Get user_id from session
        user_id = session.get('user_id')
        if not user_id:
            logging.warning(
                'Attempt to save ingredient without an active session.'
            )
            return jsonify({'message': 'Unauthorized. Please log in.'}), 401

        new_ingredient = Ingredient(
            ingredient_name=data['ingredient_name'],
            user_id=user_id
        )
        db.session.add(new_ingredient)
        db.session.commit()
        logging.info(
            f'User ID #{new_ingredient.user_id} added ingredient '
            f'"{new_ingredient.ingredient_name}" successfully.'
        )
        return jsonify({
            'id': new_ingredient.ingredient_id,
            'name': new_ingredient.ingredient_name}), 201

    except IntegrityError:
        db.session.rollback()
        logging.error(
            f'User ID # {new_ingredient.user_id} tried to add duplicate '
            f'ingredient "{new_ingredient.ingredient_name}".'
        )
        return jsonify({
            'error': 'This ingredient already exists for the user.'
        }), 400

    except Exception as e:
        db.session.rollback()
        logging.error(f'Error on add_ingredient route: {str(e)}.')
        return jsonify({'message': 'Internal server error'}), 500

    finally:
        db.session.close()


# Fetch all ingredients tied to a user's account
@main.route('/ingredients', methods=['GET'])
def get_ingredients():
    try:
        # Get user_id from session
        user_id = session.get('user_id')
        if not user_id:
            logging.warning(
                'Attempt to get available ingredients without an active session.'
            )
            return jsonify({'message': 'Unauthorized. Please log in.'}), 401

        ingredients = Ingredient.query.filter_by(user_id=user_id).all()
        logging.info(
            f'All ingredients tied to user ID #{user_id} loaded successfully.'
        )
        return jsonify([{
            'id': ing.ingredient_id,
            'name': ing.ingredient_name}
            for ing in ingredients]), 200

    except Exception as e:
        logging.error(f'Error on get_ingredients route: {str(e)}.')
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
            logging.info(
                f'User ID #{ingredient.user_id} deleted '
                f'"{ingredient.ingredient_name}" successfully.'
            )
            return jsonify({'message': 'Ingredient deleted successfully'}), 200

        db.session.rollback()
        logging.warning(f'Ingredient with ID #{ingredient_id} not found.')
        return jsonify({'message': 'Ingredient not found'}), 404

    except Exception as e:
        db.session.rollback()
        logging.error(f'Error on delete_ingredients route: {str(e)}.')
        return jsonify({'message': 'Internal server error'}), 500

    finally:
        db.session.close()


# Add a new recipe
@main.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    try:
        # Get user_id from session
        user_id = session.get('user_id')
        if not user_id:
            logging.warning(
                'Attempt to save recipe without an active session.'
            )
            return jsonify({'message': 'Unauthorized. Please log in.'}), 401

        new_recipe = Recipe(
            recipe_name=data['recipe_name'],
            recipe_cooktime=data['recipe_cooktime'],
            recipe_instructions=data['recipe_instructions'],
            user_id=user_id
        )
        db.session.add(new_recipe)
        db.session.commit()
        logging.info(
            f'User ID #{new_recipe.user_id} added recipe '
            f'"{new_recipe.recipe_name}" successfully.'
        )
        return jsonify({
            'id': new_recipe.recipe_id,
            'name': new_recipe.recipe_name}), 201

    except IntegrityError:
        db.session.rollback()
        logging.error(
            f'User ID #{new_recipe.user_id} tried to add duplicate recipe '
            f'"{new_recipe.recipe_name}".'
        )
        return jsonify({
            'error': 'This recipe already exists for the user.'
        }), 400

    except Exception as e:
        db.session.rollback()
        logging.error(f'Error on add_recipe route: {str(e)}.')
        return jsonify({'message': 'Internal server error'}), 500

    finally:
        db.session.close()


# Fetch all recipes favorited by a user
@main.route('/recipes/', methods=['GET'])
def get_recipes():
    try:
        # Get user_id from session
        user_id = session.get('user_id')
        if not user_id:
            logging.warning(
                'Attempt to get saved recipes without an active session.'
            )
            return jsonify({'message': 'Unauthorized. Please log in.'}), 401

        recipes = Recipe.query.filter_by(user_id=user_id).all()
        logging.info(
            f'All recipes tied to user ID #{user_id} have loaded successfully.'
        )
        return jsonify([{
            'id': recipe.recipe_id,
            'name': recipe.recipe_name,
            'cooktime': recipe.recipe_cooktime,
            'instructions': recipe.recipe_instructions}
            for recipe in recipes]), 200

    except Exception as e:
        logging.error(f'Error on get_recipes route: {str(e)}.')
        return jsonify({'message': 'Internal server error'}), 500

    finally:
        db.session.close()


# Fetch a favorite recipe by ID
@main.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    try:
        recipe = Recipe.query.get(recipe_id)
        if recipe:
            logging.info(
                f'User ID #{recipe.user_id} loaded recipe '
                f'"{recipe.recipe_name}" successfully.'
            )
            return jsonify({
                'id': recipe.recipe_id,
                'name': recipe.recipe_name,
                'cooktime': recipe.recipe_cooktime,
                'instructions': recipe.recipe_instructions}), 200

        logging.warning(f'Recipe with ID #{recipe_id} not found.')
        return jsonify({'message': 'Recipe not found'}), 404

    except Exception as e:
        logging.error(f'Error on get_recipe route: {str(e)}.')
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
            logging.info(
                f'User ID #{recipe.user_id} deleted recipe '
                f'"{recipe.recipe_name}" successfully.'
            )
            return jsonify({'message': 'Recipe deleted successfully'}), 200

        db.session.rollback()
        logging.warning(f'Recipe with ID #{recipe_id} not found.')
        return jsonify({'message': 'Recipe not found'}), 404

    except Exception as e:
        db.session.rollback()
        logging.error(f'Error on delete_recipe route: {str(e)}.')
        return jsonify({'message': 'Internal server error'}), 500

    finally:
        db.session.close()
