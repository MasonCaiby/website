import os
import json
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from baking.tables import tables, Food, Recipe, Review


class Database:
    """ A class to handle all interactions with a Database. It takes an optional config_file location,
        in case you want to save your config elsewhere."""

    def __init__(self, config_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')):
        self.config_file = config_file

        self.grab_data()
        self.get_session()

        self.con = None

    def grab_data(self):
        """ Grabs the data from the config file and also makes a DATABSE_URI. I believe psycopg2 convention is
            to have that variable name in all caps."""
        with open(self.config_file, 'r') as infile:
            self.data = json.load(infile)

        # Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
        self.DATABASE_URI = f"postgres+psycopg2://postgres:{self.data['database_password']}" + \
                            f"@localhost:{self.data['port']}/{self.data['server_name']}"

    def get_session(self):
        """ This safely makes a sqlalchemy connection engine and a Session instance. The Session isn't fully formed,
            so we can keep making new ones off the same instance."""
        self.engine = create_engine(self.DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)

    def create_database(self, dbname):
        """ This will make a new database, to help with setup."""

        con = psycopg2.connect(user=self.data['database_user'],
                               host='',
                               password=self.data['database_password'])
        con.autocommit = True
        cur = con.cursor()

        try:
            cur.execute(f"""CREATE DATABASE {dbname}
                            WITH 
                            OWNER = {self.data['database_user']}
                            ENCODING = 'UTF8'
                            CONNECTION LIMIT = -1;"""
                        )
            print(f"Made {dbname} database")
        except psycopg2.errors.DuplicateDatabase:
            print('Duplicate Database, passing')

    def create_tables(self, dbname, tables):
        """ This safely makes the DB's only table, called weather_app. It takes an optional name parameter, in case we
            want to further customize the emails later."""

        con = psycopg2.connect(dbname=dbname,
                               user=self.data['database_user'],
                               host='',
                               password=self.data['database_password'])
        con.autocommit = True
        cur = con.cursor()

        for table in tables:
            try:
                create = f"CREATE TABLE {table['name']} (" +\
                         f"{', '.join(table['columns'])});"

                cur.execute(create)
                print(f"Made {table['name']} table")

            except psycopg2.errors.DuplicateTable:
                print('Duplicate Table, passing')

    def add_food(self, name):
        """ Adds an email to the data base."""

        session = self.Session()
        food = Food(name=name)

        session.add(food)
        session.commit()
        session.close()

    def delete_food(self, id):
        session = self.Session()
        query = session.query(Food).filter(Food.id == id)
        query.delete()
        session.commit()

    def add_recipe(self, food_id, recipe_name, directions, change, notes, ingredients):
        session = self.Session()
        recipe = Recipe(food_id=food_id,
                        recipe_name=recipe_name,
                        directions=directions,
                        change=change,
                        notes=notes,
                        ingredients=ingredients)
        session.add(recipe)
        session.commit()

        session.refresh(recipe)

        session.close()

        return int(recipe.recipe_id)

    def delete_recipe(self, recipe_id):
        session = self.Session()
        query = session.query(Recipe).filter(Recipe.recipe_id == recipe_id)
        query.delete()
        session.commit()

    def add_review(self, recipe_id, reviewer_name, taste, texture, appearance, overall, comments):
        session = self.Session()
        review = Review(recipe_id=recipe_id,
                        reviewer_name=reviewer_name,
                        taste=taste,
                        texture=texture,
                        appearance=appearance,
                        overall=overall,
                        comments=comments)

        session.add(review)
        session.commit()
        session.close()

    def delete_review(self, review_id):
        session = self.Session()
        query = session.query(Review).filter(Review.review_id == review_id)
        query.delete()
        session.commit()

    def query_foods(self):
        self.make_query_con()

        cur = self.con.cursor()
        cur.execute("""SELECT id, name FROM food;""")
        foods = {food[1]: food[0] for food in cur.fetchall()}

        return foods

    def query_recipes(self, food_id):
        self.make_query_con()

        cur = self.con.cursor()
        cur.execute(f"""SELECT recipe_name, change, recipe_id FROM recipe
                        WHERE food_id = {food_id}; """)

        recipes = cur.fetchall()
        recipes = {recipe[0]: (recipe[1], recipe[2]) for recipe in recipes}

        return recipes

    def query_reviews(self, recipe_id):
        self.make_query_con()
        cur = self.con.cursor()
        cur.execute(f"""SELECT * from recipe
                        WHERE recipe_name = '{recipe_id}'; """)

        recipe = cur.fetchall()
        

        cur.execute(f"""SELECT * from reviews
                                WHERE recipe_id = {recipe[0][0]}; """)

        reviews = cur.fetchall()
        return recipe, reviews

    def make_query_con(self):
        if not self.con:
            self.con = psycopg2.connect(dbname='baking',
                                        user=self.data['database_user'],
                                        host='',
                                        password=self.data['database_password'])




if __name__ == "__main__":
    database = Database()
    database.create_database(dbname='baking')

    database.create_tables(dbname='baking', tables=tables)

