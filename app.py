import requests

from flask import Flask, render_template, request, redirect, session, g, flash
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm, SearchDrinkForm, SearchLiquorForm
from models import db, connect_db, User, FavoriteCocktail

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cocktail'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretCode'

CURR_USER_KEY = "curr_user"

connect_db(app)
with app.app_context():
    db.create_all()

# ------------------------------------------------------------------------------
# User Signup/Login/Logout/View Profile Routes
@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session: 
        g.user = User.query.get(session[CURR_USER_KEY])
    else: 
        g.user = None
def do_login(user):
    session[CURR_USER_KEY] = user.id
def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/register.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user: 
            do_login(user)
            flash(f'Logged In {user.username}!')
            return redirect(f'/user/{user.id}')
        flash('Bad Username or Password, try again')
    
    return render_template('users/login.html', form=form)

@app.route('/user/<int:user_id>')
def user_page(user_id):
    if not g.user:
        flash("access unauothrized, danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    drinks = FavoriteCocktail.query.filter(FavoriteCocktail.user_id == user_id).all()

    return render_template('users/userInfo.html', user=user, drinks=drinks)

@app.route('/logout')
def logout():
    session.pop(CURR_USER_KEY)
    flash('Youre logged out now')
    return redirect('/register')

# ------------------------------------------------------------------------------------------
# GENERAL VIEW ROUTES
@app.route('/')
def home_page():
    url = "https://the-cocktail-db.p.rapidapi.com/popular.php"
    headers = {
        "X-RapidAPI-Key": "1f4b3e251bmshb1df2538c036ddfp1c6675jsn19129a6f9614",
        "X-RapidAPI-Host": "the-cocktail-db.p.rapidapi.com"
        }
    response = requests.get(url, headers=headers)
    data = response.json()
    returnDrink = data['drinks']

    url2 = "https://the-cocktail-db.p.rapidapi.com/random.php"
    headers2 = {
        "X-RapidAPI-Key": "1f4b3e251bmshb1df2538c036ddfp1c6675jsn19129a6f9614",
        "X-RapidAPI-Host": "the-cocktail-db.p.rapidapi.com"
        }
    response2 = requests.get(url2, headers=headers2)
    data2 = response2.json()
    dataDrink = data2['drinks']

    return render_template('index.html', returnDrink=returnDrink, dataDrink=dataDrink)

@app.route('/search', methods=['GET', 'POST'])
def search_drink():
    form = SearchDrinkForm()

    if form.validate_on_submit():
        drinkname = form.drinkname.data

        return redirect(f"/{drinkname}")

    else:
        return render_template('search.html', form=form)
    
@app.route('/searchbyliquor', methods=['GET', 'POST'])
def search_by_liquor():
    form = SearchLiquorForm()

    if form.validate_on_submit():
        liquor = form.drinkname.data

        return redirect(f'/search/{liquor}')
    else: 
        return render_template('liquorsearch.html', form=form)


@app.route('/<drinkname>')
def popular_drink(drinkname):
    url = "https://the-cocktail-db.p.rapidapi.com/search.php"
    querystring = {"s":drinkname}
    headers = {
        "X-RapidAPI-Key": "1f4b3e251bmshb1df2538c036ddfp1c6675jsn19129a6f9614",
        "X-RapidAPI-Host": "the-cocktail-db.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    dataDrink = [data['drinks'][0]]

    returnDrink={}
    for drink in dataDrink:
        for k in drink:
            if drink[k] != None:
                returnDrink[k] = drink[k]
    ingredient = []
    for k in returnDrink:
        if 'strIngredient' in k:
            ingredient.append(returnDrink[k])
    measure = []
    for k in returnDrink:
        if 'strMeasure' in k:
            measure.append(returnDrink[k])
    result = zip(ingredient, measure)
    result_list = list(result)
    
    
    return render_template('popularDrink.html', returnDrink=[returnDrink], result_list=result_list)

@app.route('/search/<liquor>')
def liquor_search(liquor):
    url = "https://the-cocktail-db.p.rapidapi.com/filter.php"

    querystring = {"i":liquor}

    headers = {
        "X-RapidAPI-Key": "1f4b3e251bmshb1df2538c036ddfp1c6675jsn19129a6f9614",
        "X-RapidAPI-Host": "the-cocktail-db.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    returnDrink = data['drinks']

    return render_template('liquor.html', returnDrink=returnDrink)

@app.route('/<drinkname>/add', methods=['POST'])
def set_favorite(drinkname):
    if not g.user:
        flash("access unauothrized, danger")
        return redirect("/")

    favCocktail = FavoriteCocktail(
        name = drinkname,
        user_id = g.user.id
    )
    db.session.add(favCocktail)
    db.session.commit()

    return redirect(f'/user/{g.user.id}')

@app.route('/generate-random')
def genRandom():
    url = "https://the-cocktail-db.p.rapidapi.com/random.php"
    headers = {
        "X-RapidAPI-Key": "1f4b3e251bmshb1df2538c036ddfp1c6675jsn19129a6f9614",
        "X-RapidAPI-Host": "the-cocktail-db.p.rapidapi.com"
        }
    response = requests.get(url, headers=headers)
    data = response.json()
    dataDrink = data['drinks']
    returnDrink={}
    for drink in dataDrink:
        for k in drink:
            if drink[k] != None:
                returnDrink[k] = drink[k]
    
    ingredient = []
    for k in returnDrink:
        if 'strIngredient' in k:
            ingredient.append(returnDrink[k])
    measure = []
    for k in returnDrink:
        if 'strMeasure' in k:
            measure.append(returnDrink[k])
    result = zip(ingredient, measure)
    result_list = list(result)
    
    return render_template('randomCocktail.html', returnDrink=[returnDrink], result_list=result_list)


