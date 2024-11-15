# Unittests to ensure database meets requirements as per db schema.
from backend.models import User, Recipe, Ingredient
import pytest
from sqlalchemy.exc import IntegrityError, DataError


def test_validate_user_name():
    user = User()
    with pytest.raises(ValueError, match="User name must be at least 3 characters long"):
        user.user_name = "AB"  # Trigger validation


def test_create_user(init_db):
    # Tests if a user can be created and if attributes are correctly assigned as per model restrictions.
    user = User(user_name='BruceWayne', user_email='bruce@osu.edu', user_password='redacted')

    init_db.session.add(user)
    init_db.session.commit()

    assert user.user_id is not None 
    assert user.user_name == 'BruceWayne'
    assert user.user_email == 'bruce@osu.edu'

def test_invalid_email(init_db):
    # Tests if user with invalid email format can be created
    with pytest.raises(ValueError,match="Invalid email format"):
        user = User(user_name='BruceWayne', user_email='randomEMAIL', user_password='redacted')
        init_db.session.add(user)

def test_unique_email(init_db):
    # Ensures only users with unique email addresses are created
    user_one = User(user_name='LebronJames', user_email='lbj@nba.com', user_password='funpassword1')
    user_two = User(user_name='BillGates', user_email='lbj@nba.com', user_password='funpassword2')

    init_db.session.add(user_one)
    init_db.session.commit()

    with pytest.raises(IntegrityError):
        # IntegrityError - violates unique constraint
        init_db.session.add(user_two)
        init_db.session.commit()

def test_add_ingredient(init_db):
    # Tests ingredient can be added and is linked to correct user
    user = User(user_name='ChefCurry', user_email='steph@nba.com', user_password='Cookingenthusi@$t')
    ingredient = Ingredient(ingredient_name = 'Turmeric', user=user)

    init_db.session.add(user)
    init_db.session.add(ingredient)
    init_db.session.commit()

    assert ingredient.ingredient_id is not None
    assert ingredient.ingredient_name == 'Turmeric'
    assert ingredient.user_id == user.user_id

def test_create_recipe(init_db):
    # Tests recipe is created with correct atrributes and is linked to correct user.
    user = User(user_name='osuBeaver', user_email='beav@osu.com', user_password='w0odChuck!')
    recipe = Recipe(recipe_name = 'Chocolate Chip Cookies', recipe_cooktime=15, 
                    recipe_instructions= 'Mix chocolate chips with batter, cut into small pieces, then bake for suggested time.', user=user)
    
    init_db.session.add(user)
    init_db.session.add(recipe)
    init_db.session.commit()

    assert recipe.recipe_id is not None
    assert recipe.recipe_name == 'Chocolate Chip Cookies'
    assert recipe.recipe_cooktime == 15
    assert recipe.user_id == user.user_id

def test_user_blank(init_db):
    # Tests creating users with blank fields
    user = User(user_name=None, user_email=None, user_password=None)

    with pytest.raises(IntegrityError):
        init_db.session.add(user)
        init_db.session.commit()

def test_user_empty(init_db):
    # Tests creating user with empty fields
    user = User(user_name='', user_email='', user_password='')

    with pytest.raises(IntegrityError):
        init_db.session.add(user)
        init_db.session.commit()


def test_invalid_datatype(init_db):
    # Tests invalid data types of user field (e.g. passing Int to Str)
    with pytest.raises(DataError):
        user = User(user_name=6784, user_email=38275, user_password=554000)
        init_db.session.add(user)
        init_db.session.commit()


def test_duplicate_ingredients(init_db):
    # Ensures that a same user cannot add ingredients with same name.
    user=User(user_name='JohnDoe', user_email='j9674doe@gmail.com', user_password='Difficult312password')
    ingredient1 = Ingredient(ingredient_name='Broccoli',user=user)
    ingredient2 = Ingredient(ingredient_name='Broccoli',user=user)

    init_db.session.add(user)
    init_db.session.add(ingredient1)
    init_db.session.commit()

    with pytest.raises(IntegrityError):
        init_db.session.add(ingredient2)
        init_db.session.commit()

def test_duplicate_recipes(init_db):
    # Ensures that a user cannot have recipes with same name.
    user=User(user_name='JohnDoe', user_email='j9674doe@gmail.com', user_password='Difficult312password')
    init_db.sesssion.add(user)
    init_db.session.commit()

    # Add first recipe
    first_recipe = Recipe(recipe_name='Chocolate Cake', recipe_cooktime=20, recipe_instructions='Add water, mix batter, bake at 375 degrees.', user_id=user.user_id)
    init_db.session.add(first_recipe)

    # Add duplicate recipe
    duplicate_recipe = Recipe(recipe_name='Chocolate Cake', recipe_cooktime=20, recipe_instructions='Add water, mix batter, bake at 375 degrees.', user_id=user.user_id)
    
    with pytest.raises(IntegrityError):
        init_db.session.add(duplicate_recipe)
        init_db.session.commit()


def test_null_constraints_user(init_db):
    # Tests missing input for user_name
    user = User(user_name=None, user_email='fake_user@fake.com', user_password='ranDom44@')
    init_db.session.add(user)
    with pytest.raises(IntegrityError):
        init_db.session.commit()
    init_db.session.rollback()

    # Tests missing input for user_email
    user = User(user_name='BeavOSU', user_email=None, user_password='GoBe@Vers')
    init_db.session.add(user)
    with pytest.raises(IntegrityError):
        init_db.session.commit()
    init_db.session.rollback()

    # Tests missing user_password
    user = User(user_name='FooBar', user_email='foo@bar.com', user_password=None)
    init_db.session.add(user)
    with pytest.raises(IntegrityError):
        init_db.session.commit()
    init_db.session.rollback()

def test_null_constraints_ingredients(init_db):
    # Tests missing recipe_name
    ingredient = Ingredient(ingredient_name=None)
    init_db.session.add(ingredient)
    with pytest.raises(IntegrityError):
        init_db.session.commit()
    init_db.session.rollback()

def test_null_constraints_recipes(init_db):
    # Missing recipe name
    recipe = Recipe(recipe_name=None, recipe_cooktime=15, recipe_instructions="Can't make anything", user_id=1)
    init_db.session.add(recipe)
    with pytest.raises(IntegrityError):
        init_db.session.commit()
    init_db.session.rollback()

    # Missing recipe instructions
    recipe = Recipe(recipe_name='Chocolate Cake', recipe_cooktime=15, recipe_instructions=None)
    init_db.session.add(recipe)
    with pytest.raises(IntegrityError):
        init_db.session.commit()
    init_db.session.rollback()

    #Missing recipe_cooktime
    recipe = Recipe(recipe_name='Chocolate Cake', recipe_cooktime=None, recipe_instructions=None)
    init_db.session.add(recipe)
    with pytest.raises(IntegrityError):
        init_db.session.commit()
    init_db.session.rollback()

def test_user_duplicates_recipe(init_db):
    # Tests if recipes with same name can be saved by a user
    user = User(user_name='MichaelScofield', user_email='scofield@pen.com', user_password='Pri$onbre@k!')
    init_db.session.add(user)
    init_db.session.commit()

    # Create first recipe
    recipe1 = Recipe(recipe_name='Chocolate Cookies', recipe_cooktime='25', recipe_instructions='Mix batter and chocolate chips, then bake.', user_id=user.user_id)
    init_db.session.add(recipe1)
    init_db.session.commit()

    # Add recipe two with same name
    recipe2 = Recipe(recipe_name='Chocolate Cookies', recipe_cooktime='21', recipe_instructions='Mix chocolate chips with batter and bake.', user_id=user.user_id)
    init_db.session.add(recipe2)
    with pytest.raises(IntegrityError):
        init_db.session.commit()
    init_db.session.rollback()


def test_deletion_cascade(init_db):
    #Tests if deletion of a user also deletes the recipe and ingredient(s)
    user = User(user_name='REALSpiderman', user_email='spider@man.com', user_password='IAMREAL')
    init_db.session.add(user)
    init_db.session.commit()

    # Adding ingredient and recipe
    ingredient = Ingredient(ingredient_name = 'Chocolate Chips', user_id=user.user_id)
    recipe = Recipe(recipe_name='Chocolate Cookies', recipe_cooktime='25', recipe_instructions='Mix batter and chocolate chips, then bake.', user_id=user.user_id)
    init_db.session.add_all([ingredient, recipe])
    init_db.session.commit()

    # Verify items added to database
    assert Ingredient.query.filter_by(user_id=user.user_id).count==1
    assert Recipe.query.filter_by(user_id=user.user_id).count()==1

    # Delete user
    init_db.session.delete(user)
    init_db.session.commit()

    # Verify recipe and ingredients removed, after deleting user.
    assert Ingredient.query.filter_by(user_id=user.user_id).count==0
    assert Recipe.query.filter_by(user_id=user.user_id).count()==0

def test_ingredient_constraints(init_db):
    # Create user
    user = User(user_name='FooBarrr', user_email='Foo@testing.com', user_password='r3@LfO0Bar')
    init_db.sesssion.add(user)
    init_db.session.commit()

    # Test with None ingredient name
    ingredient = Ingredient(ingredient_name=None, user_id=user.user_id)
    with pytest.raises(IntegrityError):
        init_db.session.add(ingredient)
        init_db.session.commit()
    
    # Test with empty string ingrdient name
    ingredient = Ingredient(ingredient_name='', user_id=user.user_id)
    with pytest.raises(ValueError, match="Ingredient name must be at least 2 characters long"):
        init_db.session.add(ingredient)
        init_db.session.commit()
    
    # Test with less than 2 characters
    ingredient = Ingredient(ingredient_name='a', user_id=user.user_id)
    with pytest.raises(ValueError, match="Ingredient name must be at least 2 characters long"):
        init_db.session.add(ingredient)
        init_db.session.commit()

def test_recipe_name_constraints(init_db):
    # Create user
    user = User(user_name='FooBarrr', user_email='Foo@testing.com', user_password='r3@LfO0Bar')
    init_db.sesssion.add(user)
    init_db.session.commit()

    # Test with None
    recipe = Recipe(recipe_name=None, recipe_cooktime=45, recipe_instructions='mix, layer, and bake.', user_id=user.user_id)
    with pytest.raises(IntegrityError):
        init_db.session.add(recipe)
        init_db.session.commit()

    # Test with empty string
    recipe = Recipe(recipe_name='', recipe_cooktime=45, recipe_instructions='mix, layer, and bake.', user_id=user.user_id)
    with pytest.raises(ValueError, match="Recipe name must be at least 3 characters long"):
        init_db.session.add(recipe)
        init_db.session.commit()
    
    # Test with less than 3 characters
    recipe = Recipe(recipe_name='ab', recipe_cooktime=45, recipe_instructions='mix, layer, and bake.', user_id=user.user_id)
    with pytest.raises(ValueError, match="Recipe name must be at least 3 characters long"):
        init_db.session.add(recipe)
        init_db.session.commit()

def test_recipe_cooktime_constraints(init_db):
    # Create user
    user = User(user_name='FooBarrr', user_email='Foo@testing.com', user_password='r3@LfO0Bar')
    init_db.sesssion.add(user)
    init_db.session.commit()

    # Test with None
    recipe = Recipe(recipe_name='Pumpkin Pie', recipe_cooktime=None, recipe_instructions='mix, layer, and bake.', user_id=user.user_id)
    with pytest.raises(IntegrityError):
        init_db.session.add(recipe)
        init_db.session.commit()

def test_recipe_instructions_constraints(init_db):
    # Create user
    user = User(user_name='FooBarrr', user_email='Foo@testing.com', user_password='r3@LfO0Bar')
    init_db.sesssion.add(user)
    init_db.session.commit()

    # Test with None
    recipe = Recipe(recipe_name='Pumpkin Pie', recipe_cooktime=45, recipe_instructions=None, user_id=user.user_id)
    with pytest.raises(IntegrityError):
        init_db.session.add(recipe)
        init_db.session.commit()
    
    # Test with empty string
    recipe = Recipe(recipe_name='Pumpkin Pie', recipe_cooktime=45, recipe_instructions='', user_id=user.user_id)
    with pytest.raises(ValueError, match='Recipe instructions must be at least 10 characters long'):
        init_db.session.add(recipe)
        init_db.session.commit()
    
    # Test with less than 10 characters
    recipe = Recipe(recipe_name='Pumpkin Pie', recipe_cooktime=45, recipe_instructions='abcdefghi', user_id=user.user_id)
    with pytest.raises(ValueError, match='Recipe instructions must be at least 10 characters long'):
        init_db.session.add(recipe)
        init_db.session.commit()