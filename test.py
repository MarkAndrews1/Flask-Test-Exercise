from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home_page(self):
        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIn(b"<b>High Score:", res.data)
            self.assertIn(b"Current Score:", res.data)
            self.assertIn(b"Timer:", res.data)
        
    def test_valid_word(self):
        with self.client as client:
          with client.session_transaction() as ses:
            ses['board'] = [["W", "H", "A", "W", "E"], 
                            ["T", "H", "E", "F", "Z"], 
                            ["H", "E", "C", "K", "B"], 
                            ["C", "R", "Q", "X", "K"], 
                            ["J", "G", "O", "T", "P"]]
        res = self.client.get("/word-check?word=the")
        self.assertEqual(res.json['result'], "ok")

    def test_not_word(self):
       self.client.get("/")
       res = self.client.get("/word-check?word=xdcjna")
       self.assertEqual(res.json['result'], 'not-word')