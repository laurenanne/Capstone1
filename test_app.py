"""HP App tests"""

from utils import *
from app import app, CURR_USER_KEY, WIZARD_KEY

from unittest import TestCase
from models import db, User, Potion, Spell, UserPotion, UserSpell
from quiz import find_wizard_name

os.environ['DATABASE_URL'] = "postgresql:///hp-test"


db.create_all()


class UserRoutesTestCase(TestCase):
    """test user routes"""

    def setUp(self):

        db.drop_all()
        db.create_all()

        user = User(first_name='First', last_name='Last', username='test_user',
                    password='password1', image_url=None, house='Ravenclaw')

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_home(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            resp = c.get('/home')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f'/user/{self.user_id}')

    def test_main_page(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            resp = c.get(f'/user/{self.user_id}')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_user', str(resp.data))
            self.assertIn('Ravenclaw', str(resp.data))
            self.assertIn('Retake Quiz', str(resp.data))
            self.assertIn('My Potion Shelf', str(resp.data))

    def test_potion_shelf(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            resp = c.get(f'/user/{self.user_id}/potions')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('My Potion Shelf', str(resp.data))
            self.assertIn('Search', str(resp.data))

    def test_spell_book(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            resp = c.get(f'/user/{self.user_id}/spells')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('My Spell Book', str(resp.data))
            self.assertIn(
                '<p>You have no spells in your book yet. Click search below to add some!</p>', str(resp.data))

    def test_user_edit(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            resp = c.get(f'/user/{self.user_id}/edit')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit User Information', str(resp.data))
            self.assertIn('First Name', str(resp.data))
            self.assertIn('Last Name', str(resp.data))
            self.assertIn('Username', str(resp.data))
            self.assertIn('Password', str(resp.data))
            self.assertIn('Image URL', str(resp.data))

    def test_delete_user(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            resp = c.get(f'/user/{self.user_id}/delete')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/')
            user = User.query.get(self.user_id)
            self.assertIs(user, None)

    def test_wizard_name(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            resp = c.get(f'/user/{self.user_id}/wizardname')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('First Name', str(resp.data))
            self.assertIn('Birth Month', str(resp.data))
            self.assertIn('Favorite Color', str(resp.data))

    def test_add_wizard_name(self):
        with self.client as c:
            wiz_name = find_wizard_name(
                {'name': 'User1', 'month': 'Jan', 'color': 'blue'})

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id
                sess[WIZARD_KEY] = wiz_name

            resp = c.post(f'/user/{self.user_id}/add-wizardname')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/home')


# Test Potion Routes

    def test_potions_search(self):
        with self.client as c:

            resp = c.get('/potions/search')

            self.assertIn('Kissing Concoction', str(resp.data))
            self.assertIn('Weakness Potion', str(resp.data))

    def test_potions_display(self):
        with self.client as c:

            resp = c.get('/potions')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Potion starts with...', str(resp.data))

    def test_potion_details(self):
        potion = Potion(id='84d0e169-1b55-45b3-8328-29942238e535', name='Ageing Potion',
                        img_url='https://static.wikia.nocookie.net/harrypotter/images/5/51/Ageing_Potion_PM.png')

        db.session.add(potion)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            resp = c.get('/potions/84d0e169-1b55-45b3-8328-29942238e535')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Characteristics', str(resp.data))
            self.assertIn('Difficulty', str(resp.data))
            self.assertIn('Ingredients', str(resp.data))
            self.assertIn('Ageing Potion', str(resp.data))

    def test_potion_add_like(self):
        potion = Potion(id='84d0e169-1b55-45b3-8328-29942238e535', name='Ageing Potion',
                        img_url='https://static.wikia.nocookie.net/harrypotter/images/5/51/Ageing_Potion_PM.png')

        db.session.add(potion)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            resp = c.post(
                '/potions/84d0e169-1b55-45b3-8328-29942238e535/add_like', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('My Potion Shelf', str(resp.data))
            self.assertIn('Ageing Potion', str(resp.data))

    def test_potion_remove_like(self):
        potion = Potion(id='84d0e169-1b55-45b3-8328-29942238e535', name='Ageing Potion',
                        img_url='https://static.wikia.nocookie.net/harrypotter/images/5/51/Ageing_Potion_PM.png')

        db.session.add(potion)

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            userpotion = UserPotion(user_id=self.user_id, potion_id=potion.id)

            db.session.add(userpotion)
            db.session.commit()

            resp = c.post(
                '/potions/84d0e169-1b55-45b3-8328-29942238e535/add_like', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('My Potion Shelf', str(resp.data))
            self.assertNotIn('Ageing Potion', str(resp.data))

# Test Spell Routes
    def test_spells_search(self):
        with self.client as c:

            resp = c.get('/spells/search')

            self.assertIn('Cruciatus Curse', str(resp.data))
            self.assertIn('Stunning Spell', str(resp.data))

    def test_spells_display(self):
        with self.client as c:

            resp = c.get('/spells')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Spell starts with...', str(resp.data))

    def test_spell_details(self):
        spell = Spell(id='b854d1e6-6e10-405a-86f5-1e8215e36353', name='Levitation Charm', img_url='https://static.wikia.nocookie.net/harrypotter/images/c/cf/Levitation_Charm_PSF.gif'
                      )

        db.session.add(spell)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            resp = c.get('/spells/b854d1e6-6e10-405a-86f5-1e8215e36353')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Category', str(resp.data))
            self.assertIn('Effect', str(resp.data))
            self.assertIn('Levitation Charm', str(resp.data))

    def test_spell_add_like(self):
        spell = Spell(id='b854d1e6-6e10-405a-86f5-1e8215e36353', name='Levitation Charm', img_url='https://static.wikia.nocookie.net/harrypotter/images/c/cf/Levitation_Charm_PSF.gif'
                      )

        db.session.add(spell)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            resp = c.post(
                '/spells/b854d1e6-6e10-405a-86f5-1e8215e36353/add_like', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('My Spell Book', str(resp.data))
            self.assertIn('Levitation Charm', str(resp.data))

    def test_spell_remove_like(self):
        spell = Spell(id='b854d1e6-6e10-405a-86f5-1e8215e36353', name='Levitation Charm', img_url='https://static.wikia.nocookie.net/harrypotter/images/c/cf/Levitation_Charm_PSF.gif'
                      )

        db.session.add(spell)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_id

            userspell = UserSpell(user_id=self.user_id, spell_id=spell.id)

            db.session.add(userspell)
            db.session.commit()

            resp = c.post(
                '/spells/b854d1e6-6e10-405a-86f5-1e8215e36353/add_like', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('My Spell Book', str(resp.data))
            self.assertNotIn('Levitation Charm', str(resp.data))
