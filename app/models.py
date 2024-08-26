from typing import Optional

from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login

user_recipes = sa.Table(
    'user_recipes',
    db.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
    sa.Column('recipes_id', sa.Integer, sa.ForeignKey('recipes.id'), primary_key=True)
)


class Recipes(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    title: so.MappedColumn[str] = so.mapped_column(sa.String(64))
    description: so.MappedColumn[str] = so.mapped_column(sa.String(128))
    author: so.WriteOnlyMapped['User'] = so.relationship('User', secondary=user_recipes, back_populates='users')

    def __repr__(self):
        return f'Tour: {self.title}'


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64))
    email: so.Mapped[str] = so.mapped_column(sa.String(64))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    users: so.WriteOnlyMapped[Recipes] = so.relationship('Recipes', secondary=user_recipes, back_populates='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
