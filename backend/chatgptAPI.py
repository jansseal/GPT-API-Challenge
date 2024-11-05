from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_recipe(ingredients_list):
    # Construct prompt based on available ingredients
    prompt = f"Create a recipe using some or all of these ingredients: {', '.join(ingredients_list)}. Include cooking time, ingredients with quantities, and step-by-step instructions."
    
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a professional chef. Provide recipes in a structured format with cooking time, ingredients list, and clear instructions. Including cooking tips and nutritional information."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.5)

    recipe = response.choices[0].message.content  #chat completion object instance
    return {"success": True, "recipe": recipe}


if __name__ == "__main__":
    ingredients_list = ["tomatoes", "pasta", "garlic", "olive oil", "basil"]
    recipe = generate_recipe(ingredients_list)
    print(f"Generated Recipe: {recipe}")