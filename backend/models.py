from backend import db
import re
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column(db.String(255), nullable=False)

    # Relationships with Ingredient and Recipe
    ingredients = db.relationship('Ingredient', backref='user', lazy=True)
    recipes = db.relationship('Recipe', backref='user', lazy=True)

    @validates('user_name')
    def validate_user_name(self, key, user_name):
        if user_name is None:
            raise ValueError("User name cannot be null")
        if not isinstance(user_name, str):
            raise TypeError("User name must be a string")
        if any(char.isdigit() for char in user_name):
            raise ValueError("User name cannot contain numbers")
        if len(user_name) < 3:
            raise ValueError("User name must be at least 3 characters long")
        return user_name

    @validates('user_email')
    def validate_user_email(self, key, user_email):
        if user_email is None:
            raise ValueError("User email cannot be null")
        if not isinstance(user_email, str):
            raise TypeError("User email must be a string")
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, user_email):
            raise ValueError("Invalid email format")
        return user_email

    @validates('user_password')
    def validate_user_password(self, key, user_password):
        if user_password is None:
            raise ValueError("User password cannot be null")
        if not isinstance(user_password, str):
            raise TypeError("User name must be a string")
        password_pattern = (
            r'^(?=.*[A-Z])(?=.*\d)'
            r'(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        )
        if not re.match(password_pattern, user_password):
            raise ValueError("Password must be at least 8 characters long, "
                             "contain one uppercase letter, one number, and "
                             "one special character")
        return generate_password_hash(user_password, method='pbkdf2:sha256')


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredient_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id'),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            'user_id',
            'ingredient_name',
            name='user_ingredient_unique'
        ),)

    @validates('ingredient_name')
    def validate_ingredient_name(self, key, ingredient_name):
        if ingredient_name is None:
            raise ValueError("Ingredient name cannot be null")
        if not isinstance(ingredient_name, str):
            raise TypeError("Ingredient name must be a string")
        if any(char.isdigit() for char in ingredient_name):
            raise ValueError("Ingredient name cannot contain numbers")
        if len(ingredient_name) < 2:
            raise ValueError("Ingredient name must be at least 2 "
                             "characters long")
        return ingredient_name


class Recipe(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_name = db.Column(db.String(100), nullable=False)
    recipe_cooktime = db.Column(db.Integer, nullable=False)
    recipe_instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id'),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            'user_id',
            'recipe_name',
            name='user_recipe_unique'
        ),)

    @validates('recipe_name')
    def validate_recipe_name(self, key, recipe_name):
        if recipe_name is None:
            raise ValueError("Recipe name cannot be null")
        if not isinstance(recipe_name, str):
            raise TypeError("Recipe name must be a string")
        if any(char.isdigit() for char in recipe_name):
            raise ValueError("Recipe name cannot contain numbers")
        if len(recipe_name) < 3:
            raise ValueError("Recipe name must be at least 3 characters long")
        return recipe_name

    @validates('recipe_cooktime')
    def validate_recipe_cooktime(self, key, recipe_cooktime):
        if recipe_cooktime is None:
            raise ValueError("Recipe name cannot be null")
        if not isinstance(recipe_cooktime, int):
            raise TypeError("Recipe name must be an integer")
        return recipe_cooktime

    @validates('recipe_instructions')
    def validate_recipe_instructions(self, key, recipe_instructions):
        if recipe_instructions is None:
            raise ValueError("Recipe instructions cannot be null")
        if not isinstance(recipe_instructions, str):
            raise TypeError("Recipe instructions must be a string")
        if len(recipe_instructions.strip()) < 10:
            raise ValueError("Recipe instructions must be at least 10 "
                             "characters long")
        return recipe_instructions
