from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String

tables = [
    {"name": "Food",
     "columns": ["id serial PRIMARY KEY",
                 "name TEXT"]
     },

    {"name": "Recipe",
     "columns": ["recipe_id serial PRIMARY KEY",
                 "food_id Integer",
                 "recipe_name TEXT",
                 "change TEXT",
                 "directions TEXT",
                 "notes TEXT",
                 "ingredients TEXT"]
     },

    {"name": "Reviews",
     "columns": ["review_id serial",
                 "recipe_id INTEGER",
                 "reviewer_name TEXT",
                 "taste INTEGER",
                 "texture INTEGER",
                 "appearance INTEGER",
                 "overall INTEGER",
                 "comments TEXT"]}
]


class Food(declarative_base()):
    """ A class so we can add food items to the database."""
    __tablename__ = 'food'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"Food Item(id={self.id}, name={self.name}"

    def __str__(self):
        return f"Food Item(id={self.id}, name={self.name}"


class Recipe(declarative_base()):
    """ A class so we can add email recipients to the database."""
    __tablename__ = 'recipe'
    recipe_id = Column(Integer, primary_key=True)
    food_id = Column(Integer)
    recipe_name = Column(String)
    change=Column(String)
    directions = Column(String)
    notes = Column(String)
    ingredients = Column(String)

    def __repr__(self):
        return f"Recipe (recipe_id={self.recipe_id}, food_id={self.food_id}, recipe_name={self.recipe_name}, " \
               f"directions={self.directions}, notes={self.notes}, " \
               f"ingredients={self.ingredients}"

    def __str__(self):
        return str(self.recipe_id)


class Review(declarative_base()):
    __tablename__ = 'reviews'
    review_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer)
    reviewer_name = Column(String)
    taste = Column(Integer)
    texture = Column(Integer)
    appearance = Column(Integer)
    overall = Column(Integer)
    comments = Column(String)

    def __repr__(self):
        return f"Review (id={self.recipe_id}, reviewer_name={self.reviewer_name}, taste={self.taste}, " +\
               f"texture={self.texture}, appearance={self.appearance}, overall={self.overall}, comments={self.comments}"

    def __str__(self):
        return f"Review (id={self.recipe_id}, reviewer_name={self.reviewer_name}, taste={self.taste}, " +\
               f"texture={self.texture}, appearance={self.appearance}, overall={self.overall}, comments={self.comments}"

