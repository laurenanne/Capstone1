"""Model tests"""

from utils import *
from app import app

from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Potion, Spell, UserPotion, UserSpell

os.environ['DATABASE_URL'] = "postgresql:///hp-test"


with app.app_context():
    db.create_all()


class UserModelTestCase(TestCase):

    def setUp(self):
        with app.app_context():    
            db.drop_all()
            db.create_all()

            self.client = app.test_client()

    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_user_model(self):
        """test user model works"""
        with app.app_context():
            user = User(first_name='First', last_name='Last', username='test_user',
                    password='password1', image_url=None, house='Ravenclaw')

            db.session.add(user)
            db.session.commit()

            self.assertTrue(user)

# Signup tests
    def test_valid_signup(self):
        with app.app_context():
            valid = User.signup('First', 'Last', 'username',
                            'password', None, 'Hufflepuff')

            valid.id = 2600
            db.session.commit()

            valid = User.query.get(2600)
            self.assertIsNotNone(valid)
            self.assertEqual(valid.username, 'username')
            self.assertEqual(valid.house, 'Hufflepuff')
            self.assertNotEqual(valid.password, 'password')
            self.assertTrue(valid.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        with app.app_context():
            invalid = User.signup('First', 'Last', None,
                              'password', None, 'Hufflepuff')

            db.session.add(invalid)

            with self.assertRaises(exc.IntegrityError) as context:
                db.session.commit()

    def test_invalid_first_name_signup(self):
        with app.app_context():
            invalid = User.signup(None, 'Last', 'username',
                              'password', None, 'Hufflepuff')

            db.session.add(invalid)

            with self.assertRaises(exc.IntegrityError) as context:
                db.session.commit()

    def test_invalid_last_name_signup(self):
        with app.app_context():
            invalid = User.signup('First', None, 'username',
                              'password', None, 'Hufflepuff')

            db.session.add(invalid)

            with self.assertRaises(exc.IntegrityError) as context:
                db.session.commit()

    def test_invalid_password_signup(self):

        with self.assertRaises(ValueError) as context:
            User.signup('First', 'Last', 'username',
                        None, None, 'Hufflepuff')

        with self.assertRaises(ValueError) as context:
            User.signup('First', 'Last', 'username',
                        "", None, 'Hufflepuff')

    def test_invalid_house_signup(self):
        with app.app_context():
            invalid = User.signup('First', 'Last', 'username',
                              'password', None, None)

            db.session.add(invalid)

            with self.assertRaises(exc.IntegrityError) as context:
                db.session.commit()


# Authentication tests

    def test_valid_auth(self):
        with app.app_context():
            valid = User.signup('First', 'Last', 'username',
                            'password', None, 'Hufflepuff')

            valid.id = 3000
            db.session.commit()

            auth = User.auth('username', 'password')
            self.assertIsNotNone(auth)
            self.assertEqual(auth.id, valid.id)

    def test_invalid_username(self):
        with app.app_context():
            valid = User.signup('First', 'Last', 'username',
                            'password', None, 'Hufflepuff')

            valid.id = 3000
            db.session.commit()

            self.assertFalse(User.auth('wrongusername', 'password'))

    def test_invalid_password(self):
        with app.app_context():
            valid = User.signup('First', 'Last', 'username',
                            'password', None, 'Hufflepuff')

            valid.id = 3000
            db.session.commit()

            self.assertFalse(User.auth('username', 'wrongpassword'))


# Potion tests


    def test_potion_model(self):
        """test potion model works"""
        with app.app_context():
            potion = Potion(id='potionid', name='TestPotion',
                        img_url=None)

            db.session.add(potion)
            db.session.commit()

            self.assertTrue(potion)

    def test_user_potion_model(self):
        """test userpotion model works"""
        with app.app_context():
            potion = Potion(id='potionid', name='TestPotion',
                        img_url=None)
            db.session.add(potion)
            db.session.commit()

            user = User(first_name='First', last_name='Last', username='test_user',
                    password='password1', image_url=None, house='Ravenclaw')
            db.session.add(user)
            db.session.commit()

            userpotion = UserPotion(user_id=user.id, potion_id=potion.id)
            db.session.add(userpotion)
            db.session.commit()

            self.assertTrue(userpotion)

# Spell tests
    def test_spell_model(self):
        """test spell model works"""
        with app.app_context():
            spell = Spell(id='spellid', name='TestSpell',
                      img_url=None)

            db.session.add(spell)
            db.session.commit()

            self.assertTrue(spell)

    def test_user_spell_model(self):
        """test userspell model works"""
        with app.app_context():
            spell = Spell(id='spellid', name='TestSpell',
                      img_url=None)
            db.session.add(spell)
            db.session.commit()

            user = User(first_name='First', last_name='Last', username='test_user',
                    password='password1', image_url=None, house='Ravenclaw')
            db.session.add(user)
            db.session.commit()

            userspell = UserSpell(user_id=user.id, spell_id=spell.id)
            db.session.add(userspell)
            db.session.commit()

            self.assertTrue(userspell)
