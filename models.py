"""SQLAlchemy models for HP"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """connect database to HP app"""
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    image_url = db.Column(db.Text, default="/static/images/userimage.jpeg")
    house = db.Column(db.Text, nullable=False)

    potions = db.relationship(
        'UserPotion', backref="user", cascade="all, delete")
    spells = db.relationship(
        'UserSpell', backref="users", cascade="all, delete")

    def __repr__(self):
        return f'<User #{self.id}: {self.username}>'

    @classmethod
    def signup(cls, first_name, last_name, username, password, image_url, house):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=hashed_pwd,
            image_url=image_url,
            house=house
        )

        db.session.add(user)
        return user

    @classmethod
    def auth(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Potion(db.Model):

    __tablename__ = 'potions'

    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)
    img_url = db.Column(db.Text)

    # direct navigation: Potion -> UserPotion and back
    user_potion = db.relationship('UserPotion', backref='potion')


class Spell(db.Model):

    __tablename__ = 'spells'

    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)
    img_url = db.Column(db.Text)

    # direct navigation: Spell -> UserSpell and back
    user_spell = db.relationship('UserSpell', backref='spell')


class UserPotion(db.Model):

    __tablename__ = "users_potions"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), primary_key=True)
    potion_id = db.Column(db.Text, db.ForeignKey(
        "potions.id"), primary_key=True)


class UserSpell (db.Model):

    __tablename__ = "users_spells"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), primary_key=True)
    spell_id = db.Column(db.Text, db.ForeignKey(
        "spells.id"), primary_key=True)
