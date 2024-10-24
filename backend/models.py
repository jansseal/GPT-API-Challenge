from backend import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column(db.String(255), nullable=False)

    # Relationships with Ingredient and Recipe
    ingredients = db.relationship('Ingredient', backref='user', lazy=True)
    recipes = db.relationship('Recipe', backref='user', lazy=True)


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredient_name = db.Column(db.String(100), nullable=False, unique=True)

    # Foreign key to User
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id'),
        nullable=False
    )

    # Relationship with RecipeIngredient (join table)
    recipe_ingredients = db.relationship(
        'RecipeIngredient',
        backref='ingredient',
        lazy=True
    )


class Recipe(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_name = db.Column(db.String(100), nullable=False, unique=True)
    recipe_cooktime = db.Column(db.Integer, nullable=False)
    recipe_instructions = db.Column(db.Text, nullable=False)

    # Foreign key to users
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id'),
        nullable=False
    )

    # Relationship with RecipeIngredient (join table)
    ingredients = db.relationship(
        'RecipeIngredient',
        backref='recipe',
        lazy=True
    )


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    recipe_ingredient_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    quantity = db.Column(db.String(50))

    # Foreign keys to Recipe and Ingredient
    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey('recipes.recipe_id'),
        nullable=False
    )
    ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey('ingredients.ingredient_id'),
        nullable=False
    )
