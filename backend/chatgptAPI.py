from flask import Flask, request, jsonify
from openai import OpenAI

client = OpenAI(api_key="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")



def generate_recipe(prompt):
    # generate a new key later and store as env variable on personal machine
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a 1950's Italian Mobster who likes to speak in metaphors."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7)

    recipe = response.choices[0].message.content  
    return recipe

if __name__ == "__main__":
    prompt = "Generate a recipe for pasta with tomato sauce."
    recipe = generate_recipe(prompt)
    print(f"Generated Recipe: {recipe}")

