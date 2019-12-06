from flask import Flask, request, session, g, url_for, \
    render_template, flash, redirect

from basic_auth_edited import BasicAuth
from database import Database

# import numpy as np
# from helpers import fade_colors

app = Flask(__name__)

app.config.from_envvar('LIGHT_CONTROLS_SETTINGS', silent=True)

db = Database()
# password protected info for lights_control
## TODO: salt and hash password/username

# pi1 = pigpio.pi()

with open('lights_login.csv', 'r') as pass_file:
    login_info = pass_file.read()
    login_info = login_info.split(',')
    username = login_info[0]
    password = login_info[1]
app.config['BASIC_AUTH_USERNAME'] = username
app.config['BASIC_AUTH_PASSWORD'] = password
basic_auth = BasicAuth(app, failed_login='failed_login.html')


# don't cache css
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/climbing')
def climbing():
    return render_template('climbing.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/wildlife')
def wildlife():
    return render_template('wildlife.html')


@app.route('/handler')
def handler():
    return render_template('handler.html')


@app.route('/table')
def table():
    return render_template('table.html')


@app.route('/website')
def website():
    return render_template('website.html')


@app.route('/auto_app')
def auto_app():
    return render_template('auto_app.html')


# a page with a description etc.
@app.route('/compare_grades')
def compare_grades():
    return render_template('compare_grades.html')


# the full html page.
@app.route('/compare_grades_full')
def compare_grades_full():
    return render_template('compare_grades_full.html')


@app.route('/baking', methods=['GET', 'POST'])
def baking():
    food_dict = db.query_foods()

    if request.method == 'POST':
        if 'Add a Food' == request.form['baking_button']:
            return redirect(url_for('add_food'))
        else:
            food_id = request.form['baking_button']
            return redirect(url_for('view_food',
                                    food_id=food_id))

    return render_template('baking.html', foods=food_dict)


@app.route('/view_food', methods=['GET', 'POST'])
def view_food():
    if request.method == 'POST':

        selection = list(request.form.items())[0]

        if selection[0] == 'add_recipe':
            return redirect(url_for('add_recipe', food_id=request.form.get('food_id')))

        return redirect(url_for('view_recipe',
                                recipe_id=request.form['recipe_selector']))

    food_id = request.args.get('food_id')
    recipes = db.query_recipes(food_id)
    food = db.food_name_from_id(food_id)

    return render_template('view_food.html', food=food, recipes=recipes, food_id=food_id)


@app.route('/view_recipe', methods=['GET', 'POST'])
def view_recipe():
    if request.method == 'POST':
        return redirect(url_for('add_review', recipe_id=request.form.get('recipe_id')))

    recipe_id = request.args.get('recipe_id')
    recipe, reviews = db.query_reviews(recipe_id)
    recipe = [str(line) for line in recipe[0][2:]]
    reviews = [" | ".join([str(info1) for info1 in info]) for info in [review[2:] for review in reviews]]

    return render_template('view_ratings.html', recipe=recipe, reviews=reviews, recipe_id=recipe_id)


@app.route('/add_food', methods=['GET', 'POST'])
def add_food():
    if request.method == 'POST':
        food_id = db.add_food(name=request.form['food_name'])
        return redirect(url_for('view_food', food_id=food_id))
    return render_template('add_food.html')


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == "POST":
        recipe = request.form['recipe_name']
        recipe_id = db.add_recipe(food_id=request.args.get('food_id'),
                                  recipe_name=recipe,
                                  directions=request.form['directions'],
                                  change=request.form['recipe_change'],
                                  notes=request.form['notes'],
                                  ingredients=request.form['ingredients'])
        return redirect(url_for('view_recipe', recipe_id=recipe_id, food=request.args.get('food')))
    return render_template('add_recipe.html')


@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        form = request.form
        db.add_review(recipe_id=request.args.get('recipe_id'),
                      reviewer_name=form['reviewer_name'],
                      taste=form['taste'],
                      texture=form['texture'],
                      appearance=form['appearance'],
                      overall=form['overall'],
                      comments=form['comments'])
        return redirect(url_for('view_recipe', recipe_id=request.args.get('recipe_id')))

    return render_template('add_review.html', recipe_id=request.args.get('recipe_id'))

# this will never be used. I Could just redirect all traffic to the example page, but want to keep it as it's
# an ok example of authentication
@app.route('/controls', methods=['GET', 'POST'])
@basic_auth.required
def light_controls():
    # safely try to get the current values of the GPIO Pins. If multiple people
    # are controlling the table, it pulls the current value every time they
    # load it. I could move this into the html so people get live updates
    ## TODO: move into html for live update.
    r = 0
    g = 0
    b = 0
    # try:
    #     r = pi1.get_PWM_dutycycle(17)
    #     g = pi1.get_PWM_dutycycle(27)
    #     b = pi1.get_PWM_dutycycle(22)
    # except AttributeError:
    #     r = 0
    #     g = 0
    #     b = 0
    # except:
    #     print(Exception)
    #
    # if request.method == 'POST':
    #     try:
    #         new_colors = np.array([request.form['red'], request.form['green'],
    #                               request.form['blue']])
    #         new_colors = new_colors.astype('int')
    #         assert (np.all(new_colors < 256) and np.all(new_colors >= 0))
    #         fade_colors(pi1, np.array([r, g, b]), new_colors, [17, 27, 22])
    #         r = pi1.get_PWM_dutycycle(17)
    #         g = pi1.get_PWM_dutycycle(27)
    #         b = pi1.get_PWM_dutycycle(22)
    #     except (ValueError, AssertionError):
    #         flash('You need to type a value between 0 and 255 for all boxes')
    return render_template('light_controls.html', r_value=r, g_value=g,
                            b_value=b)


if __name__ == '__main__':
    
    app.run(threaded=True, port=80, host='0.0.0.0')
