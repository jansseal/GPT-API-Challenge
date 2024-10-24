# Unittests to ensure database meets requirements as per db schema.

from backend.models import User, Recipe, RecipeIngredient, Ingredient
import pytest

def test_create_user(init_db):
    # Tests if a user can be created and if attributes are correctly assigned as per model restrictions.
    user = User(user_name='BruceWayne', user_email='bruce@osu.edu', user_password='redacted')

    init_db.session.add(user)
    init_db.session.commit()

    assert user.user_id is not None 
    assert user.user_name == 'BruceWayne'
    assert user.user_email == 'bruce@osu.edu'

def test_unique(init_db):
    # Ensures only users with unique email addresses are created
    user_one = User(user_name='LebronJames', user_email='lbj@nba.com', user_password='funpassword1')
    user_two = User(user_name='BillGates', user_email='lbj@msft.com', user_password='funpassword2')

    init_db.session.add(user_one)
    init_db.session.commit()

    with pytest.raises(Exception):
        # IntegrityError - violates unique constraint
        init_db.session.add(user_two)
        init_db.session.commit()

def test_add_ingredient(init_db):
    # Tests ingredient can be added and is linked to correct user
    user = User(user_name='ChefCurry', user_email='steph@nba.com', user_password='cookingenthusiast')
    ingredient = Ingredient(ingredient_name = 'Turmeric', user=user)

    init_db.session.add(user)
    init_db.session.add(ingredient)
    init_db.session.commit()

    assert ingredient.ingredient_id is not None
    assert ingredient.ingredient_name == 'Turmeric'
    assert ingredient.user_id == user.user_id

def test_create_recipe(init_db):
    # Tests recipe is created with correct atrributes and is linked to correct user.
    user = User(user_name='osuBeaver', user_email='beav@osu.com', user_password='woodChuck!')
    recipe = Recipe(recipe_name = 'Chocolate Chip Cookies', recipe_cooktime=15, 
                    recipe_instructions= 'Mix chocolate chips with batter, cut into small pieces, then bake for suggested time.', user=user)
    
    init_db.session.add(user)
    init_db.session.add(recipe)
    init_db.session.commit()

    assert recipe.recipe_id is not None
    assert recipe.recipe_name == 'Chocolate Chip Cookies'
    assert recipe.recipe_cooktime == 15
    assert recipe.user_id == user.user_id

def test_create_ingredient_recipe(init_db):
    # Tests many-to-many relationships between Recipe and Ingredient.
    user = User(user_name='BobRoss', user_email='ross@bob.ca', user_password='bobrosssss')
    ingredient = Ingredient(ingredient_name = 'Eggs', user=user)
    recipe = Recipe(recipe_name = 'Hard Boiled Eggs', recipe_cooktime=10, 
                    recipe_instructions= 'Fill small pot with water, let water boil, add eggs and let it boil for suggested time.', user=user)
    recipe_ingredient = RecipeIngredient(quantity='2', recipe=recipe, ingredient=ingredient)

    init_db.session.add(user)
    init_db.session.add(ingredient)
    init_db.session.add(recipe)
    init_db.session.add(recipe_ingredient)
    init_db.session.commit()

    assert recipe_ingredient.recipe_ingredient_id is not None
    assert recipe_ingredient.quantity == '2'
    assert recipe_ingredient.recipe_id == recipe.recipe_id
    assert recipe_ingredient.ingredient_id == ingredient.ingredient_id
