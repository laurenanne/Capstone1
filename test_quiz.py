"""Quiz tests"""

from utils import *
from app import app, CURR_USER_KEY, RESPONSES_KEY, HOUSE_KEY

from unittest import TestCase
from quiz import Question, find_wizard_name, determine_house, response_key

from models import db, User
from flask import session

os.environ['DATABASE_URL'] = "postgresql:///hp-test"


db.create_all()


class QuizTestCase(TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_quiz(self):
        ques = Question("Which sport do you most like to play?", [
            response_key['A'][2], response_key['B'][2], response_key['C'][2], response_key['D'][2]]),

        self.assertEqual(
            "Which sport do you most like to play?", ques[0].question)

        self.assertIn(
            "Swimming", ques[0].choices)

    def test_start(self):
        with self.client as c:

            resp = c.post(
                '/start', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                'How do you like to spend your free time?', str(resp.data))

    def test_incorrect_ques(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[RESPONSES_KEY] = []
                sess[HOUSE_KEY] = []

            resp = c.get('/ques/3')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/ques/0')
            self.assertIn(('message', 'Invalid question 3'),
                          session['_flashes'])

    def test_correct_ques(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[RESPONSES_KEY] = ['Outside playing tag or trying a new move on the monkey bars', 'Red', 'Basketball', 'Hot fudge sundae',
                                       'Doing any type of physical activity', 'You start experimenting with household items for fun', 'You bravely decide to climb the tree and free the cat yourself']
                sess[HOUSE_KEY] = []

            resp = c.get('/ques/7')

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                'Your parents take you out to dinner at a new restaurant', str(resp.data))

    def test_response(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[RESPONSES_KEY] = ['Outside playing tag or trying a new move on the monkey bars', 'Red', 'Basketball', 'Hot fudge sundae',
                                       'Doing any type of physical activity']
                sess[HOUSE_KEY] = []

            resp = c.post('/response')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/ques/5')

    def test_response_done(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[RESPONSES_KEY] = ['Working on perfecting your latest writing assignment or leading a game of soccer', 'Green', 'Fencing', 'Souffle', "Relax? Don't tell me to relax...I'm working on fine tuning my piano skills", 'You will be working solo on this one',
                                       'You call for rescure and lead the rescue squad to the tree', 'You decide to try the dish which sounds the most flavorful', 'You choose the dog that listens to your commands', 'To work on mastering your tennis skills']
                sess[HOUSE_KEY] = []

            resp = c.post('/response', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

    def test_result(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[RESPONSES_KEY] = ['Working on perfecting your latest writing assignment or leading a game of soccer', 'Green', 'Fencing', 'Souffle', "Relax? Don't tell me to relax...I'm working on fine tuning my piano skills", 'You will be working solo on this one',
                                       'You call for rescure and lead the rescue squad to the tree', 'You decide to try the dish which sounds the most flavorful', 'You choose the dog that listens to your commands', 'To work on mastering your tennis skills']

                responses = sess[RESPONSES_KEY]
                results = determine_house(responses)
                sess[HOUSE_KEY] = results

            resp = c.get('/result')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Slytherin', str(resp.data))

    def test_result_with_curr_user(self):
        with self.client as c:
            with c.session_transaction() as sess:
                user = User(first_name='First', last_name='Last', username='test_user',
                            password='password1', image_url=None, house='Ravenclaw')

                db.session.add(user)
                db.session.commit()

                sess[RESPONSES_KEY] = ['Working on perfecting your latest writing assignment or leading a game of soccer', 'Green', 'Fencing', 'Souffle', "Relax? Don't tell me to relax...I'm working on fine tuning my piano skills", 'You will be working solo on this one',
                                       'You call for rescure and lead the rescue squad to the tree', 'You decide to try the dish which sounds the most flavorful', 'You choose the dog that listens to your commands', 'To work on mastering your tennis skills']

                responses = sess[RESPONSES_KEY]
                results = determine_house(responses)
                sess[HOUSE_KEY] = results
                sess[CURR_USER_KEY] = user.id

            resp = c.get('/result', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

    def test_determine_house(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[RESPONSES_KEY] = ['Playing guitar or helping a friend with an art project', 'Yellow', 'Volleyball', ' Cake to share with friends', "As long as I'm sorrounded by friends I'm calm",
                                       'You grab your friends together and decide to do a group project', 'You feel quite terrible for the poor cat', 'You decide to order an old favorite', 'You pick the dog that looks a bit sad and lonely in the corner', 'Volunteer your time ']

            responses = sess[RESPONSES_KEY]
            results = determine_house(responses)

            self.assertEqual(results, 'Hufflepuff')

    def test_find_wizard_name(self):
        with self.client as c:
            wiz_name = find_wizard_name(
                {'name': 'User1', 'month': 'Jan', 'color': 'pink'})

            self.assertEqual(wiz_name, 'User1 Mimdore')
