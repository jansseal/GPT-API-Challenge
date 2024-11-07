from backend import db
import re
from sqlalchemy.ext.declarative import validates
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
    def validate_user_name(self, user_name):
        if len(user_name) < 3:
            raise ValueError("User name must be at least 3 characters long")
        if any(char.isdigit() for char in user_name):
            raise ValueError("User name cannot contain numbers")
        return user_name

    @validates('user_email')
    def validate_user_email(self, user_email):
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, user_email):
            raise ValueError("Invalid email format")
        return user_email

    @validates('user_password')
    def validate_user_password(self, user_password):
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
    def validate_ingredient_name(self, ingredient_name):
        if len(ingredient_name) < 2:
            raise ValueError("Ingredient name must be at least 2 "
                             "characters long")
        if any(char.isdigit() for char in ingredient_name):
            raise ValueError("Ingredient name cannot contain numbers")
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
    def validate_recipe_name(self, recipe_name):
        if len(recipe_name) < 3:
            raise ValueError("Recipe name must be at least 3 characters long")
        if any(char.isdigit() for char in recipe_name):
            raise ValueError("Recipe name cannot contain numbers")
        return recipe_name

    @validates('recipe_instructions')
    def validate_recipe_instructions(self, recipe_instructions):
        if len(recipe_instructions.strip()) < 10:
            raise ValueError("Recipe instructions must be at least 10 "
                             "characters long")
        return recipe_instructions
