from flask import render_template, redirect, url_for
import sqlalchemy as sa
from flask_login import logout_user, current_user, login_required, login_user
from . import app, db
from .models import Recipes, User, Category
from .forms import RecipesForm, SignUpForm, LoginForm, CategoryForm


@app.route('/')
def home():
    recipes = db.session.scalars(sa.select(Recipes)).all()
    categories = db.session.scalars(sa.select(Category)).all()
    return render_template('home.html', recipes=recipes, categories=categories)


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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('sign.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/new/recipes', methods=['POST', 'GET'])
@login_required
def new_recipes():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RecipesForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        recipe = Recipes(title=form.title.data, description=form.description.data, author=current_user,
                         category_id=form.category.data)
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_recipes.html', form=form)


@app.route('/edit/<int:recipe_id>', methods=['POST', 'GET'])
def edit_recipe(recipe_id):
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    recipe = db.session.scalar(sa.select(Recipes).where(Recipes.id == recipe_id))
    form = RecipesForm(obj=recipe)
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_recipes.html', form=form)


@app.route('/profile')
def profile():
    recipes = db.session.scalars(current_user.recipes.select())
    return render_template('profile.html', recipes=recipes)


@app.route('/recipe/save/<int:recipe_id>')
def save_recipe(recipe_id):
    recipe = db.session.scalar(sa.select(Recipes).where(Recipes.id == recipe_id))
    recipes = db.session.scalars(current_user.recipes.select())
    if recipe in recipes:
        return redirect(url_for('already_saved'))
    current_user.recipes.add(recipe)
    db.session.commit()
    return render_template('recipe_saved.html')


@app.route('/recipe/already')
def already_saved():
    return render_template('already_saved.html')


@app.route('/category/new', methods=['POST', 'GET'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_category.html', form=form)


@app.route('/category/edit', methods=['POST', 'GET'])
def edit_category(category_id):
    category = db.session.scalars(sa.select(Category).where(Category.id == category_id))
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_category.html', form=form)

