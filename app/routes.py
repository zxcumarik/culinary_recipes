from flask import render_template, redirect, url_for, flash, request
import sqlalchemy as sa
from flask_login import logout_user, current_user, login_required, login_user
from . import app, db
from .models import Recipes, User
from .forms import RecipesForm, SignForm, LoginForm


@app.route('/')
def home():
    recipes = db.session.scalars(sa.select(Recipes)).all()
    return render_template('home.html', recipes=recipes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data) or not user.is_active:
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('sign.html', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    form = SignForm()
    return render_template('sign.html', form=form)


@login_required
@app.route('/new/recipes', methods=['POST', 'GET'])
def new_recipes():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RecipesForm()
    if form.validate_on_submit():
        recipe = Recipes(title=form.title.data, description=form.description.data)
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_recipes.html', form=form)


@app.route('/edit/<int:recipe_id>', methods=['POST', 'GET'])
def edit_recipe(recipe_id):
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    recipe = db.session.scalar(sa.select(Recipes).where(Recipes.id == recipe_id))
    form = RecipesForm
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_recipes.html', form=form)