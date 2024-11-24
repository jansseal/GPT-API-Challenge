# Comprehensive package of tests for the API routes

import pytest
from backend.models import User, Ingredient, Recipe
from sqlalchemy.exc import IntegrityError

def test_home_route(test_client):
    # Basic test to ensure home route is working
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == "GPT API Challenge"

def test_add_user_success(test_client, init_db):
    #Tests if user sent from API can be added to DB
    response = test_client.post('/users', json={
        'user_name': 'ElizMonroe',
        'user_email': 'mmonroe@osu.com',
        'user_password': 'P@ssValiD1'
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['user_name'] == 'ElizMonroe'
    assert data['id'] is not None

def test_add_duplicate_email(test_client, init_db):
    # Tests if user with pre-existing email address can be added
    # Not passing.
    user = User(user_name='ElizMonroe', user_email='mmonroe@osu.com', user_password='P@ssValiD1')
    init_db.session.add(user)
    init_db.session.commit()

    response_one = test_client.post('/users', json={
        'user_name': 'RileyMonroe',
        'user_email': 'mmonroe@osu.com',
        'user_password': 'P@ssValiD1'
    })

    assert response_one.status_code == 400  # Failure
    assert response_one.get_json()['message'] == 'User email must be unique'


def test_add_user_invalid_data(test_client):
    # Tests if user with invalid data fields can be added
    response = test_client.post('/users', json={
        'user_name': '',
        'user_email': 'ReALeMail',
        'user_password': 'FD@'
    })

    assert response.status_code == 500

def test_get_valid_user(test_client, init_db):
    # Retrieves valid user
    user = User(user_name='FooBar', user_email='FooBar@oregonstate.edu', user_password='LegITpW123@!')
    init_db.session.add(user)
    init_db.session.commit()

    response = test_client.get(f'/users/{user.user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['user_name'] == user.user_name
    assert data['user_email'] == user.user_email

def test_user_not_found(test_client, init_db):
    # Checks for user that is not in database.
    user = User(user_name='FooBar', user_email='FooBar@oregonstate.edu', user_password='LegITpW123@!')
    init_db.session.add(user)
    init_db.session.commit()

    # Delete user
    response_one = test_client.delete(f'/users/{user.user_id}')
    assert response_one.status_code == 200
    assert response_one.get_json()['message'] == 'User deleted successfully'

    # Attempt to delete user again
    response_two = test_client.delete(f'/users/{user.user_id}')
    assert response_two.status_code == 404
    assert response_two.get_json()['message'] == 'User not found'

    # Attempt to retriever non-existent user
    response_three = test_client.get(f'/users/{user.user_id}')
    assert response_three.status_code == 404
    assert response_three.get_json()['message'] == 'User not found'

def test_delete_user(test_client, init_db):
    # Tests if existing user is deleted
    user = User(user_name='RemoveMe', user_email='removers@validdb.com', user_password='RoMe@Italy!1')
    init_db.session.add(user)
    init_db.session.commit()

    response = test_client.delete(f'/users/{user.user_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == "User deleted successfully"

def test_delete_invalid_user(test_client, init_db):
    # Attempts to delete user that is not in database. 
    user = User(user_name='JohnDoe', user_email='johndoe@randomize.org', user_password='Crazy1$$lolzaaaaa')
    init_db.session.add(user)
    init_db.session.commit()
    
    # Delete user
    response_one = test_client.delete(f'/users/{user.user_id}')
    assert response_one.status_code == 200
    assert response_one.get_json()['message'] == 'User deleted successfully'

    # Attempt to remove user again
    response_two = test_client.delete(f'/users/{user.user_id}')
    assert response_two.status_code == 404
    assert response_two.get_json()['message'] == 'User not found'

def test_add_ingredient(test_client, init_db):
    # Tests if a valid ingredient can be added
    user = User(user_name='FooBar', user_email='realFoo@bar.com', user_password='Re@L1ty$TriKez')
    init_db.session.add(user)
    init_db.session.commit()

    response = test_client.post('/ingredients', json={
        'ingredient_name': 'Spinach',
        'user_id': user.user_id
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Spinach'


def test_add_duplicate_ingredient(test_client, init_db):
    # Tests if duplicate ingredients can be associated to a user
    response_one = test_client.post('/users', json={
        'user_name': 'FooBar',
        'user_email': 'realFoo@Bar.com',
        'user_password': 'Re@L1ty$TriKez'
    })

    assert response_one.status_code == 201
    user_id = response_one.get_json()['id'] # retrieve ID to associated ingredient to user

    # Add ingredient
    response_two = test_client.post('/ingredients', json={
        'ingredient_name':'Olives',
        'user_id':user_id
    })
    assert response_two.status_code == 201

    # Attempt to add same ingredient again
    response_three = test_client.post('/ingredients', json={
        'ingredient_name':'Olives',
        'user_id':user_id
    })
    assert response_three.status_code == 400
    assert response_three.get_json()['error'] == 'This ingredient already exists for the user.'


def test_retrieve_ingredient(test_client, init_db):
    # Tests if valid ingredient can be retrieved
    user = User(user_name='FooBar', user_email='realFoo@bar.com', user_password='Re@L1ty$TriKez')
    init_db.session.add(user)
    init_db.session.commit()

    ingredient = Ingredient(ingredient_name='Turkey', user=user)
    init_db.session.add(ingredient)
    init_db.session.commit()

    response = test_client.get(f'/ingredients/{user.user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['name'] == 'Turkey'

def test_remove_ingredient(test_client, init_db):
    # Tests if removal of ingredient is success
    user = User(user_name='LBJames', user_email='lbj@nba.com', user_password='W!nL0$e3514sss')
    init_db.session.add(user)
    init_db.session.commit()

    ingredient = Ingredient(ingredient_name='Greek Yogurt', user=user)
    init_db.session.add(ingredient)
    init_db.session.commit()

    response = test_client.delete(f'/ingredients/{ingredient.ingredient_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Ingredient deleted successfully'

def test_remove_invalid_ingredient(test_client, init_db):
    # Tests if non-existent ingredient can be removed
    user = User(user_name='MichaelScott', user_email='realscott@yahoo.com', user_password='W!nXYZzz3514sss')
    init_db.session.add(user)
    init_db.session.commit()

    ingredient = Ingredient(ingredient_name='Baking Powder', user=user)
    init_db.session.add(ingredient)
    init_db.session.commit()

    # Remove ingredient
    response_one = test_client.delete(f'/ingredients/{ingredient.ingredient_id}')
    assert response_one.status_code == 200
    assert response_one.get_json()['message'] == 'Ingredient deleted successfully'

    # Attempt to remove ingredient again.
    response_two = test_client.delete(f'/ingredients/{ingredient.ingredient_id}')
    assert response_two.status_code == 404
    assert response_two.get_json()['message'] == 'Ingredient not found'

def test_add_recipe(test_client, init_db):
    # Tests if a recipe can be created for a valid user
    user = User(user_name='BatManReal', user_email='justkidding@gmail.com', user_password='MarvelV$DC321')
    init_db.session.add(user)
    init_db.session.commit()

    response = test_client.post('/recipes', json={
        'recipe_name': 'Pasta',
        'recipe_cooktime': 20,
        'recipe_instructions': 'Boil past in hot water, add rose sauce, serve.',
        'user_id': user.user_id,
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Pasta'

def test_add_duplicate_recipe(test_client, init_db):
    # Tests if an existing recipe can be added again for a user
    response_one = test_client.post('/users', json={
        'user_name': 'JaneDoe',
        'user_email': 'doe@jane.ca',
        'user_password': 'DifficultP@$$W0rd1!'
    })

    assert response_one.status_code == 201
    user_id = response_one.get_json()['id'] # Retrieve user ID

    # Add first recipe
    response_two = test_client.post('/recipes', json={
        'recipe_name': 'Rose Pasta',
        'recipe_cooktime': 15,
        'recipe_instructions': 'Boil past in hot water, add rose sauce, serve.',
        'user_id': user_id
    })
    assert response_two.status_code == 201

    # Try to add same recipe again
    response_three = test_client.post('/recipes', json={
        'recipe_name': 'Rose Pasta',
        'recipe_cooktime': 15,
        'recipe_instructions': 'Boil past in hot water, add rose sauce, serve.',
        'user_id': user_id
    })

    assert response_three.status_code == 400
    assert response_three.get_json()['error'] == 'This recipe already exists for the user.'


def test_get_recipe(test_client, init_db):
    # Test if existing recipe is retrieved
    user = User(user_name='JohnDoe', user_email='johndoe@yahoo.com', user_password='D0e@1973Jane1!')
    init_db.session.add(user)
    init_db.session.commit()

    recipe = Recipe(
        recipe_name = 'Chocolate Chip Cookies',
        recipe_cooktime=35,
        recipe_instructions = 'Add water, stir mixture, make small balls and bake at 375.',
        user = user
    )

    init_db.session.add(recipe)
    init_db.session.commit()

    response = test_client.get(f'/recipes/{user.user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['name'] == 'Chocolate Chip Cookies'

def test_delete_recipe(test_client, init_db):
    # Tests if exist recipe from database is removed
    user = User(user_name='JohnDoe', user_email='johndoe@yahoo.com', user_password='D0e@1973Jane1!')
    init_db.session.add(user)
    init_db.session.commit()

    recipe = Recipe(
        recipe_name = 'Muffins',
        recipe_cooktime=35,
        recipe_instructions = 'Add water, add chocolate chips, stir mixture and place in muffin tray. Let it bake at 375.',
        user = user
    )
    init_db.session.add(recipe)
    init_db.session.commit()

    response = test_client.delete(f'/recipes/{recipe.recipe_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Recipe deleted successfully'


def test_delete_invalid_recipe(test_client, init_db):
    # Tests if non-existing recipe can be deleted.
    user = User(user_name='MaryJane', user_email='jacob22@gmail.com', user_password='Pa@sZwOrd1ZZzz!')
    init_db.session.add(user)
    init_db.session.commit()

    # Add recipe
    recipe = Recipe(
        recipe_name = 'Chocolate Cake',
        recipe_cooktime = 45,
        recipe_instructions='Mix ingredients, add melted chocolate, and bake at 375.',
        user=user
    )
    init_db.session.add(recipe)
    init_db.session.commit()

    # Delete recipe
    response_one = test_client.delete(f'/recipes/{recipe.recipe_id}')
    assert response_one.status_code == 200
    assert response_one.get_json()['message'] == 'Recipe deleted successfully'

    # Attempt to delete again]
    response_two = test_client.delete(f'/recipes/{recipe.recipe_id}')
    assert response_two.status_code == 404
    assert response_two.get_json()['message'] == 'Recipe not found'


def test_update_user_success(test_client, init_db):
    # Update user name and password with correct current password
    user = User(user_name="TimothyEl", user_email="timoth@school.com", user_password="Gl@diat0r12!!")
    init_db.session.add(user)
    init_db.session.commit()

    response = test_client.put(f'/users/{user.user_id}', json={
        "current_user_password": "Gl@diat0r12!!",
        "user_name": "TimothyElNew",
        "new_user_password": "NEWGl@diat0r12!!"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == user.user_id
    assert data["user_name"] == "TimothyElNew"


def test_update_user_invalid_password(test_client, init_db):
    # Test updating a user with an incorrect password
    user = User(user_name="BobCouzy", user_email="couzybob@bob.com", user_password="COuZyy123!@Couzy")
    init_db.session.add(user)
    init_db.session.commit()

    response = test_client.put(f'/users/{user.user_id}', json={
        "current_user_password": "COuZyy123!@",
        "user_name": "CouzyBobEdit",
        "new_user_password": "IwantNewP@SSw0Rd12!"
    })

    assert response.status_code == 403
    assert response.get_json()["message"] == "Current password is incorrect"

def test_update_user_not_found(test_client, init_db):
    # Tests if a user not in database can be updated
    user = User(user_name="TimothyEl", user_email="timoth@school.com", user_password="Gl@diat0r12!!")
    init_db.session.add(user)
    init_db.session.commit()

    # Remove user
    init_db.session.delete(user)
    init_db.session.commit()

    # Attempt to update user
    response = test_client.put(f'/users/{user.user_id}', json={
        "current_user_password": "Gl@diat0r12!!",
        "user_name": "TimothElNew",
        "new_user_password": "NEWGl@diat0r12!!"
    })

    assert response.status_code == 404
    assert response.get_json()["message"] == "User not found"


def test_get_ingredients_success(test_client,init_db):
    # Retrieve ingredients for a valid user
    user = User(user_name="ChefScooby", user_email="scooby@scoobysnacks.com", user_password="WhereRu321@")
    init_db.session.add(user)
    init_db.session.commit()

    ingredient = Ingredient(ingredient_name="Rice grains", user=user)
    init_db.session.add(ingredient)
    init_db.session.commit()

    response = test_client.get(f"/ingredients/{user.user_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1 # User only has one ingredient
    assert data[0]["name"] == 'Rice grains' # Verify it is the ingredient added

def test_get_empty_ingredients(test_client,init_db):
    # Retrieve ingredients user with no ingredients
    user = User(user_name="ChefScooby", user_email="scooby@scoobysnacks.com", user_password="WhereRu321@")
    init_db.session.add(user)
    init_db.session.commit()

    response = test_client.get(f"/ingredients/{user.user_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0 # User has 0 ingredients


def test_get_ingredients_user_dne(test_client,init_db):
    # Test checks output for retrieving ingredient if user dne
    user = User(user_name="SantaClause", user_email="gifts@christmasllc.com", user_password="Rudolph@541Deer")
    init_db.session.add(user)
    init_db.session.commit()

    # Add ingredient associated to user
    ingredient = Ingredient(ingredient_name="Beef Patty", user=user)
    init_db.session.add(ingredient)
    init_db.session.commit()

    # Delete user
    response_one = test_client.delete(f"/users/{user.user_id}")
    assert response_one.status_code == 200
    assert response_one.get_json()["message"] == "User deleted successfully"

    # Attempt to retrieve users ingredient
    response_two = test_client.get(f"/ingredients/{user.user_id}")
    assert response_two.status_code == 404
    assert response_two.get_json()["message"] == "Ingredient not found"


def test_get_empty_recipes(test_client, init_db):
    # Test retrieving recipes for user with no recipes
    user = User(user_name="ChefShaggy", user_email="shaggy@scoobyempire.com", user_password="ShaggyScooby12$@")
    init_db.session.add(user)
    init_db.session.commit()

    response = test_client.get(f"/recipes/{user.user_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0 # User has 0 recipes


def test_get_recipes_user_dne(test_client,init_db):
    # Test checks output for retrieving recipe if user does not exist
    user = User(user_name="ChefShaggy", user_email="shaggy@scoobyempire.com", user_password="ShaggyScooby12$@")
    init_db.session.add(user)
    init_db.session.commit()

    # Add ingredient associated to user
    ingredient = Ingredient(ingredient_name="Potato", user=user)
    init_db.session.add(ingredient)
    init_db.session.commit()

    # Add recipe associated to user using ingredient
    recipe = Recipe(
        recipe_name = "Potato Wedges",
        recipe_cooktime=30,
        recipe_instructions = "Soak potatose in hot water for 15 min, slice them up, apply oil, and air fry at 375",
        user=user
    )

    init_db.session.add(recipe)
    init_db.session.commit()

    # Delete user
    response_one = test_client.delete(f"/users/{user.user_id}")
    assert response_one.status_code == 200
    assert response_one.get_json()["message"] == "User deleted successfully"

    # Attempt to retrieve users ingredient
    response_two = test_client.get(f"/ingredients/{user.user_id}")
    assert response_two.status_code == 404
    assert response_two.get_json()["message"] == "Ingredient not found"

    # Attempt to retreive users recipe
    response_three = test_client.get(f"/recipes/{user.user_id}")
    assert response_three.status_code == 404
    assert response_three.get_json(["message"]) == "Recipe not found"