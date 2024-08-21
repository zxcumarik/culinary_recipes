from typing import Optional

from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(UserMixin, db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    username: so.MappedColumn[str] = so.mapped_column(sa.String(64))
    email: so.MappedColumn[str] = so.mapped_column(sa.String(64))
    password_hash: so.MappedColumn[Optional[str]] = so.mapped_column(sa.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))