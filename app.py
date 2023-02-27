import os

from flask import Flask, render_template, jsonify, request, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Potion, Spell, UserPotion, UserSpell
from quiz import sorting_hat_quiz, determine_house, find_wizard_name
from forms import LoginForm, NewUserForm, EditUserForm, WizardNameForm
import requests
import random
from psycopg2.errors import UniqueViolation
from werkzeug.exceptions import BadRequest


app = Flask(__name__)
app.app_context().push()

uri = os.environ.get('DATABASE_URL', 'postgresql:///harry_potter')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecretkey13')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

RESPONSES_KEY = 'responses'
CURR_USER_KEY = 'curr_user'
HOUSE_KEY = 'house'
WIZARD_KEY = 'wiz_name'


#################################################################
# User signup / login / logout routes


@ app.route('/signup', methods=["GET", "POST"])
def signup():
    """handle user signup"""
    if HOUSE_KEY not in session:
        return redirect('/')

    form = NewUserForm()
    house = session[HOUSE_KEY]

    if form.validate_on_submit():
    
        user = User.signup(first_name=form.first_name.data, last_name=form.last_name.data,
                           username=form.username.data, password=form.password.data, image_url=form.image_url.data, house=house)

        try:
            db.session.commit()
            session[CURR_USER_KEY] = user.id
            session.pop(HOUSE_KEY)
            session.pop(RESPONSES_KEY)

        except IntegrityError:
            flash("This username is already take", 'danger')
            db.session.rollback()
         
            return redirect('/signup')

        return redirect(f'/user/{user.id}')

   
    else:
        return render_template('signup.html', form=form)


@ app.route('/login', methods=["GET", "POST"])
def login():
    """Renders login form and handles user"""
    form = LoginForm()
   
    """check for valid login credentials"""
    if form.validate_on_submit():
        user = User.auth(form.username.data, form.password.data)

        if user:
            session[CURR_USER_KEY] = user.id
           
            return redirect(f'/user/{user.id}')

        else:
            flash("Incorrect username/password", 'danger')

    return render_template('/login.html', form=form)


@ app.route('/logout')
def logout():
    """handle user logout"""
    if CURR_USER_KEY in session:
        session.pop(CURR_USER_KEY)
    if WIZARD_KEY in session:
        session.pop(WIZARD_KEY)
    if HOUSE_KEY in session:
        session.pop(HOUSE_KEY)
    if RESPONSES_KEY in session:
        session.pop(RESPONSES_KEY)    

    
    return redirect('/')


#####################################################
# survey routes


@ app.route('/')
def homepage():
    """Show homepage"""
    
    return render_template('index.html')


@ app.route('/start', methods=["POST"])
def start_quiz():
    """clear session of previous responses"""
    session[HOUSE_KEY] = []
    session[RESPONSES_KEY] = []

    return redirect("/ques/0")


@ app.route('/ques/<int:quesid>')
def show_ques(quesid):
    """"Show current question"""

    responses = session.get(RESPONSES_KEY)

    if responses is None:
        return redirect('/')

    if len(responses) == len(sorting_hat_quiz.questions):
        return redirect('/result')

    if len(responses) != quesid:
        flash(f'Invalid question {quesid}')
        return redirect(f'/ques/{len(responses)}')

    question = sorting_hat_quiz.questions[quesid]

    return render_template('ques.html', question=question)


@ app.route('/response', methods=["POST"])
def handle_response():
    """handles the users quiz answers"""
    responses = session[RESPONSES_KEY]

    try:
        response = request.form['answer']
        responses.append(response)
        session[RESPONSES_KEY] = responses

    except BadRequest:
        db.session.rollback()
        return redirect(f'/ques/{len(responses)}')

    if (len(responses) == len(sorting_hat_quiz.questions)):
        """All the questions have been answered. Redirect to see the results"""
        return redirect('/result')

    else:
        return redirect(f'/ques/{len(responses)}')


@ app.route('/result')
def quiz_result():
    """Shows the Harry Potter House the user belongs to based on quiz results"""

    if HOUSE_KEY not in session:
        return redirect('/')

    responses = session[RESPONSES_KEY]
    results = determine_house(responses)
    session[HOUSE_KEY] = results

    """if user is already logged in then update their house based on latest quiz"""
    if CURR_USER_KEY in session:
        user = User.query.get_or_404(session[CURR_USER_KEY])
        house = session[HOUSE_KEY]

        user.house = house
        db.session.commit()

        session.pop(HOUSE_KEY)
        session.pop(RESPONSES_KEY)

        return redirect(f'/user/{user.id}')

    return render_template('results.html', results=results)


########################################################
# user routes
@ app.route('/users')
def show_users():
    """Show all users """
    users = User.query.all()

    return render_template('/wizards.html', users=users)


@ app.route('/home')
def show_user_homepage():
    user_id = session[CURR_USER_KEY]

    return redirect(f'/user/{user_id}')


@ app.route('/user/<int:user_id>')
def show_user_page(user_id):
    """Show user detail"""
    user = User.query.get_or_404(user_id)

    """make an API call to get characters in the user's house"""
    final_results = []
    for page in range(1, 4):
        response = requests.get(
            f'https://api.potterdb.com/v1/characters?filter[house_eq]={user.house}&page[number={page}]')
        data = response.json()
        final_results = final_results + data['data']

    """filter house characters to show those with images"""
    characters = []
    for repo in final_results:
        if repo['attributes']['image'] is not None:
            characters.append({'name': repo['attributes']['name'],
                               'image': repo['attributes']['image']})

    return render_template('main.html', user=user, characters=characters)


@ app.route('/user/<int:user_id>/potions')
def show_user_potions(user_id):
    """shows users potions and a search button to look for more to add"""

    user = User.query.get_or_404(user_id)

    return render_template('/my-potions.html', user=user)


@ app.route('/user/<int:user_id>/spells')
def show_user_spells(user_id):
    """shows users spells and a search button to add"""

    user = User.query.get_or_404(user_id)

    return render_template('/my-spells.html', user=user)


@ app.route('/user/<int:user_id>/wizardname', methods=["GET", "POST"])
def show_wizard_name_form(user_id):

    form = WizardNameForm()
    user = User.query.get_or_404(user_id)
    if WIZARD_KEY in session:
        session.pop(WIZARD_KEY)

    if form.validate_on_submit():
        name = request.form.get('first_name')
        month = request.form.get('birth_month')
        color = request.form.get('fav_color')

        wiz_name = find_wizard_name(
            {'name': name, 'month': month, 'color': color})

        session[WIZARD_KEY] = wiz_name
        return render_template('/name-results.html', user=user, wiz_name=wiz_name)

    return render_template('/name.html', form=form, user=user)


@ app.route('/user/<int:user_id>/add-wizardname', methods=["POST"])
def add_wizard_name_form(user_id):
    """Allows user to add wizard name to user profile"""

    if WIZARD_KEY not in session:
        return redirect('/home')

    wiz_name = session[WIZARD_KEY]

    if CURR_USER_KEY in session:
        user = User.query.get_or_404(session[CURR_USER_KEY])
        wiz_name = session[WIZARD_KEY]

        user.username = wiz_name
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("This username is already take", 'danger')
            x = str(random.randint(1, 5000))
            wiz_name = wiz_name + x
            session[WIZARD_KEY] = wiz_name
            return render_template('/name-results.html', user=user, wiz_name=wiz_name)

    return redirect('/home')


@ app.route('/user/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user_profile(user_id):
    "Update profile for current user"
    if session[CURR_USER_KEY] != user_id:
        flash("Unauthorized access", "danger")
        return redirect('/login')

    form = EditUserForm()

    user = User.query.get_or_404(user_id)

    if form.validate_on_submit():
        user = User.auth(user.username, form.password.data)
        if user:

            user.first_name = form.first_name.data,
            user.last_name = form.last_name.data,
            user.image_url = form.image_url.data or "/static/images/userimage.jpeg"
            user.username = form.username.data

            try:
                db.session.commit()

            except IntegrityError as e:
                db.session.rollback()
                if isinstance(e.orig, UniqueViolation):
                    flash("Username already taken", "danger")
                return redirect(f'/user/{user.id}/edit')

            return redirect(f'/user/{user.id}')

        flash("Invalid credentials", "danger")
        return redirect('/login')

    return render_template('/edit.html', form=form, user=user)


@ app.route('/user/<int:user_id>/delete')
def delete_user(user_id):
    """Delete user"""

    if session[CURR_USER_KEY] != user_id:
        flash("Unauthorized access", "danger")
        return redirect('/login')

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    
    if CURR_USER_KEY in session:
        session.pop(CURR_USER_KEY)
    if WIZARD_KEY in session:
        session.pop(WIZARD_KEY)
    if HOUSE_KEY in session:
        session.pop(HOUSE_KEY)
    if RESPONSES_KEY in session:
        session.pop(RESPONSES_KEY)    

    return redirect('/')


##########################################################################
# Potions routes


@ app.route('/potions/search')
def get_all_potions():
    final_results = []
    for page in range(1, 3):
        response = requests.get(
            f'https://api.potterdb.com/v1/potions?page[number={page}]')
        data = response.json()
        final_results = final_results + data['data']

    potions = []
    for repo in final_results:
        if repo['attributes']['image'] is not None:
            potions.append({'id': repo['id'], 'name': repo['attributes']['name'],
                           'image': repo['attributes']['image']})

    return potions


@ app.route('/potions')
def show_all_potions():
    """shows potion search"""

    return render_template('/potions.html')


@ app.route('/potions/<potion_id>')
def show_potion(potion_id):
    """shows potion details"""
    """make an API call to get potion detail"""
    response = requests.get(
        f'https://api.potterdb.com/v1/potions/{potion_id}')
    repo = response.json()['data']

    ingredients = repo['attributes']['ingredients']

    if ingredients is None:
        ingredients = ['None listed']
    elif ingredients == '':
        ingredients = ['None listed']
    else:
        ingredients = ingredients.split(', ')

    potion = {'id': repo['id'], 'name': repo['attributes']['name'], 'image': repo['attributes']['image'], 'effect': repo['attributes']
              ['effect'], 'difficulty': repo['attributes']['difficulty'], 'ingredients': ingredients, 'characteristics': repo['attributes']['characteristics']}

    id = repo['id']

    pot_id_list = []

    user = User.query.get_or_404(session[CURR_USER_KEY])
    if len(user.potions) > 0:
        for pot in user.potions:
            pot_id_list.append(pot.potion_id)

        if id in pot_id_list:
            icon = "fa-solid fa-heart"

        else:
            icon = "fa-regular fa-heart"

    else:
        icon = "fa-regular fa-heart"

    return render_template('/potion-detail.html', potion=potion, icon=icon)


@ app.route('/potions/<potion_id>/add_like', methods=["POST"])
def add_like_for_potion(potion_id):

    user_id = session[CURR_USER_KEY]

    """check if potion is already on the potion shelf. If it is remove from shelf"""
    user_potion = UserPotion.query.filter(
        UserPotion.user_id == user_id, UserPotion.potion_id == potion_id).first()

    if user_potion:
        db.session.delete(user_potion)
        db.session.commit()

        return redirect(f'/user/{user_id}/potions')

    """make an API call to get potion detail"""
    response = requests.get(
        f'https://api.potterdb.com/v1/potions/{potion_id}')
    repo = response.json()['data']

    name = repo['attributes']['name']
    img_url = repo['attributes']['image']

    """if another user has liked it so it's in the potion database move directly to adding it to user potion table"""
    if Potion.query.get(potion_id):

        user_potions = UserPotion(user_id=user_id, potion_id=potion_id)
        db.session.add(user_potions)
        db.session.commit()

    else:

        potion = Potion(id=potion_id, name=name, img_url=img_url)
        db.session.add(potion)
        db.session.commit()

        user_potions = UserPotion(user_id=user_id, potion_id=potion_id)
        db.session.add(user_potions)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if isinstance(e.orig, UniqueViolation):

                return redirect(f'/user/{user_id}/potions')

    return redirect(f'/user/{user_id}/potions')


##########################################################################
# Spell routes


@ app.route('/spells/search')
def get_all_spells():
    """make an API call to get all spells"""
    final_results = []
    for page in range(1, 5):
        response = requests.get(
            f'https://api.potterdb.com/v1/spells?page[number={page}]')
        data = response.json()
        final_results = final_results + data['data']

    spells = []
    for repo in final_results:
        if repo['attributes']['image'] is not None:
            spells.append({'id': repo['id'], 'name': repo['attributes']['name'],
                           'image': repo['attributes']['image']})

    return spells


@ app.route('/spells')
def show_all_spells():
    """shows spells search"""

    return render_template('/spells.html')


@ app.route('/spells/<spell_id>')
def show_spell(spell_id):
    """shows spell details"""
    """make an API call to get spell detail"""
    response = requests.get(
        f'https://api.potterdb.com/v1/spells/{spell_id}')
    repo = response.json()['data']

    spell = {'id': repo['id'], 'name': repo['attributes']['name'], 'image': repo['attributes']['image'], 'incantation': repo['attributes']
             ['incantation'], 'category': repo['attributes']['category'], 'effect': repo['attributes']['effect']}

    id = repo['id']

    spl_id_list = []
    user = User.query.get_or_404(session[CURR_USER_KEY])
    if len(user.spells) > 0:
        for spl in user.spells:
            spl_id_list.append(spl.spell_id)

        if id in spl_id_list:
            icon = "fa-solid fa-heart"

        else:
            icon = "fa-regular fa-heart"

    else:
        icon = "fa-regular fa-heart"

    return render_template('/spell-detail.html', spell=spell, icon=icon)


@ app.route('/spells/<spell_id>/add_like', methods=["POST"])
def add_like_for_spell(spell_id):

    user_id = session[CURR_USER_KEY]

    """check if spell is already in the spell book. If it is remove from book"""
    user_spell = UserSpell.query.filter(
        UserSpell.user_id == user_id, UserSpell.spell_id == spell_id).first()

    if user_spell:
        db.session.delete(user_spell)
        db.session.commit()

        return redirect(f'/user/{user_id}/spells')

    """make an API call to get spell detail"""
    response = requests.get(
        f'https://api.potterdb.com/v1/spells/{spell_id}')
    repo = response.json()['data']

    name = repo['attributes']['name']
    img_url = repo['attributes']['image']

    """if another user has liked it so it's in the spell database move directly to adding it to user spell table"""
    if Spell.query.get(spell_id):

        user_spells = UserSpell(user_id=user_id, spell_id=spell_id)
        db.session.add(user_spells)
        db.session.commit()

    else:
        """add spell to spell table and user_spell to user spells"""
        spell = Spell(id=spell_id, name=name, img_url=img_url)
        db.session.add(spell)
        db.session.commit()

        user_spells = UserSpell(user_id=user_id, spell_id=spell_id)
        db.session.add(user_spells)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if isinstance(e.orig, UniqueViolation):

                return redirect(f'/user/{user_id}/spells')

    return redirect(f'/user/{user_id}/spells')
