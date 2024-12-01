from backend.models import User, Recipe, Ingredient
from backend.chatgptAPI import generate_recipe
from unittest.mock import patch, Mock
from flask import session
import pytest

def test_generate_recipe_valid(test_client, init_db):
    # Set up user
    user = User(user_name="realMadrid", user_email="madridchefs@gmail.com", user_password="Secur3Enuff1@")
    init_db.session.add(user)
    init_db.session.commit()

    # Simulate a session with the user's ID
    with test_client.session_transaction() as session:
        session['user_id'] = user.user_id

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


def test_fail_to_connect(test_client, init_db):
    # Set up user
    user = User(user_name="rattatouille", user_email="radzz@yahoo.com", user_password="RaShi0NaLitY!!!")
    init_db.session.add(user)
    init_db.session.commit()

    # Simulate a session with the user's ID
    with test_client.session_transaction() as session:
        session['user_id'] = user.user_id

    # Simulate failure
    with patch('backend.chatgptAPI.client.chat.completions.create', side_effect=Exception("OpenAI API failure")):
        response = test_client.post('/api/generate-recipe', json={
            "ingredients": "brown rice, chicken",
            "dietary_concerns": "gluten-free"
        })

        assert response.status_code == 500
        data = response.get_json()
        assert data['error'] == "Internal server error"


def test_gen_recipe_fridge_valid(test_client, init_db):
    # Set up user
    user = User(user_name="JamesHarden", user_email="harden@nba.com", user_password="Clipper5B@Ll")
    init_db.session.add(user)
    init_db.session.commit()

    # Simulate a session with the user's ID
    with test_client.session_transaction() as session:
        session['user_id'] = user.user_id

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


def test_gen_recipe_parsing_error(test_client, init_db):
    # Set up user
    user = User(user_name="RayMondsss", user_email="raymondz@shop.ca", user_password="RandoMizeQU311!!")
    init_db.session.add(user)
    init_db.session.commit()

    # Simulate a session with the user's ID
    with test_client.session_transaction() as session:
        session['user_id'] = user.user_id

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