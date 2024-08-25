from flask import render_template, redirect, url_for, flash
import sqlalchemy as sa
from flask_login import logout_user, current_user, login_required, login_user

from app import app, db
from app.models import Recipes, User
from app.forms import RecipesForm, SignForm, LoginForm


@login_required
@app.route('/')
def home():
    recipes = db.session.scalars(sa.select(Recipes)).all()
    return render_template('home.html', recipes=recipes)


@app.route('/login', methods=['POST', 'GET'])
def login_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login_up'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('home.html', form=form)


@app.route('/sign', methods=['POST', 'GET'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_up'))
    return render_template('home.html', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return render_template('sign.html')