from backend.models import User, Recipe, Ingredient
from backend.chatgptAPI import generate_recipe
from unittest.mock import patch, Mock
from flask import session
import pytest
import json
import os
import logging

def test_generate_recipe_valid(test_client):
    # Mock API response
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content="""
        {
            \"recipe_name\": \"Pasta Primavera\",
            \"cooking_time\": \"30 minutes\",
            \"ingredients\": [
                {\"ingredient\": \"Pasta\", \"quantity\": \"200\", \"unit\": \"grams\"},
                {\"ingredient\": \"Tomatoes\", \"quantity\": \"2\", \"unit\": \"pieces\"}
            ],
            \"instructions\": [\"Boil pasta\", \"Cook tomatoes\"],
            \"nutritional_info\": {\"calories\": \"400\", \"protein\": \"15g\", \"fat\": \"10g\", \"carbohydrates\": \"60g\"},
            \"cooking_tips\": \"Use fresh basil for better flavor.\"
        }
        """))
    ]
    mock_response.usage = Mock(prompt_tokens=20, completion_tokens=30, total_tokens=50)

    with patch('backend.chatgptAPI.client.chat.completions.create', return_value=mock_response):
        response = test_client.post('/api/generate-recipe', json={
            "ingredients": "pasta, tomatoes",
            "dietary_concerns": "vegetarian"
        })

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['recipe']['recipe_name'] == 'Pasta Primavera'


def test_fail_to_connect(test_client):
    # Simulate failure
    with patch('backend.chatgptAPI.client.chat.completions.create', side_effect=Exception("OpenAI API failure")):
        response = test_client.post('/api/generate-recipe', json={
            "ingredients": "brown rice, chicken",
            "dietary_concerns": "gluten-free"
        })

        assert response.status_code == 500
        data = response.get_json()
        assert data['error'] == "Internal server error"


def test_gen_recipe_fridge_valid(test_client):
    # Mock API response
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content="""
        {
            \"recipe_name\": \"Tomato Soup\",
            \"cooking_time\": \"20 minutes\",
            \"ingredients\": [
                {\"ingredient\": \"Tomatoes\", \"quantity\": \"3\", \"unit\": \"pieces\"},
                {\"ingredient\": \"Onions\", \"quantity\": \"1\", \"unit\": \"piece\"}
            ],
            \"instructions\": [\"Chop tomatoes\", \"Boil them\"],
            \"nutritional_info\": {\"calories\": \"150\", \"protein\": \"3g\", \"fat\": \"5g\", \"carbohydrates\": \"20g\"},
            \"cooking_tips\": \"Add a pinch of sugar for taste.\"
        }
        """))
    ]
    mock_response.usage = Mock(prompt_tokens=25, completion_tokens=35, total_tokens=60)

    with patch('backend.chatgptAPI.client.chat.completions.create', return_value=mock_response):
        response = test_client.post('/api/generate-recipe-from-fridge', json={
            "fridge_ingredients": ["tomatoes", "onions"],
            "dietary_concerns": "vegan"
        })

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['recipe']['recipe_name'] == 'Tomato Soup'


def test_gen_recipe_parsing_error(test_client):
    # Mock invalid API response
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content="weatherforecast jack"))
    ]
    mock_response.usage = Mock(prompt_tokens=15, completion_tokens=10, total_tokens=25)

    with patch('backend.chatgptAPI.client.chat.completions.create', return_value=mock_response):
        response = test_client.post('/api/generate-recipe', json={
            "ingredients": "whole grain bread, cheese, jalapenos",
            "dietary_concerns": "none"
        })

        assert response.status_code == 500
        data = response.get_json()
        assert data['success'] is False
        assert data['error'] == "Invalid recipe format from OpenAI"


def test_malformed_fridge_ingredient(test_client):
    # Test responses when missing fridge_ingredient field
    with patch('backend.chatgptAPI.generate_recipe', return_value=None) as mock_generate_recipe:
        response = test_client.post('/api/generate-recipe-from-fridge', json={
            # Missing field: fridge_ingredient
            "dietary_concerns": None
        })
        
        mock_generate_recipe.assert_not_called()
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == "Please provide ingredients as a list"


def test_fridge_ingredient_number(test_client):
    # Test response when fridge_ingredient data type is int
    with patch('backend.chatgptAPI.generate_recipe', return_value=None) as mock_generate_recipe:
        response = test_client.post('/api/generate-recipe-from-fridge', json={
            "fridge_ingredients": 2415,
            "dietary_concerns": None
        })

        mock_generate_recipe.assert_not_called()
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == "Please provide ingredients as a list"


def test_fridge_ingredient_string(test_client):
    # Test response when fridge_ingredient data type is string
    with patch('backend.chatgptAPI.generate_recipe', return_value=None) as mock_generate_recipe:
        response = test_client.post('/api/generate-recipe-from-fridge', json={
            "fridge_ingredients": "celery, garlic",
            "dietary_concerns": "vegan",
        })

        mock_generate_recipe.assert_not_called()
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == "Please provide ingredients as a list"


def test_fridge_ingredients_empty(test_client):
    # Test response when fridge_ingredients is an empty list []
    with patch('backend.chatgptAPI.generate_recipe', return_value=None) as mock_generate_recipe:
        response = test_client.post('/api/generate-recipe-from-fridge', json={
            "fridge_ingredients": [],
            "dietary_concerns": "vegan",
        })

        mock_generate_recipe.assert_not_called()
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == "Please provide ingredients as a list"


def test_user_flow(test_client, init_db):
    # Tests users flow from account creation to recipe generation. Ensures all aspects are working

    # Add user
    user_data = {"user_name":"OSUBEAVERRRRR",
                 "user_email": "testbeav@beav.com",
                 "user_password": "Te3thy12@Tee"}
    
    user_response = test_client.post('/users', json=user_data)
    assert user_response.status_code == 201

    user = user_response.get_json()
    user_id = user['id']
    assert user['user_name'] == user_data["user_name"]
    assert user['user_email'] == user_data["user_email"]

    # Simulate session
    with test_client.session_transaction() as session:
        session['user_id'] = user_id

    # Add ingredient
    ingredient_data = {
        "ingredient_name": "Broccoli"
    }

    ingredient_response = test_client.post('/ingredients', json=ingredient_data)
    assert ingredient_response.status_code == 201

    ingredient = ingredient_response.get_json()
    assert ingredient['name'] == ingredient_data["ingredient_name"]

    # Generate recipe using added ingredient
    recipe_response = Mock()
    recipe_response.choices = [
        Mock(message=Mock(content=json.dumps({
            "recipe_name": "Broccoli Soup",
            "cooking_time": "20 minutes",
            "ingredients": [
                {"ingredient": "Broccoli", "quantity": "3", "unit": "pieces"}
            ],
            "instructions": ["Chop broccoli", "Boil them"],
            "nutritional_info": {"calories": "160", "protein": "5g", "fat": "1g", "carbohydrates": "17g"},
            "cooking_tips": "Add a pinch of sugar, salt, and pepper for taste."
        })))
    ]
    recipe_response.usage = Mock(prompt_tokens=25, completion_tokens=35, total_tokens=60)

    with patch('backend.chatgptAPI.client.chat.completions.create', return_value=recipe_response):
        generate_recipe_response = test_client.post('/api/generate-recipe-from-fridge', json={
            "fridge_ingredients": [ingredient_data['ingredient_name']],
            "dietary_concerns": "vegan"
        })

    assert generate_recipe_response.status_code == 200
    recipe = generate_recipe_response.get_json()
    assert recipe['success'] is True
    assert recipe['recipe']['recipe_name'] == 'Broccoli Soup'
    assert recipe['recipe']['ingredients'][0]['ingredient'] == "Broccoli"

