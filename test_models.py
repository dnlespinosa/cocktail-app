import os
from unittest import TestCase

from models import db, User, FavoriteCocktail

os.environ['DATABASE_URL'] = "postgresql:///cocktail-test"

from app import app

db.create_all()


class UserModelTestCase(TestCase):

    def setUp(self):

        User.query.delete()

        self.client = app.test_client()

        user1 = User.signup('user1', 'youremail@gmail.com', 'password')
        user2 = User.signup('user2', 'youreemail2@gmail.com', 'password')
        user1.id=1
        user2.id=2
        db.session.commit()

        self.user1 = user1
        self.user2 = user2
        self.user1.id = 1
        self.user2.id = 2

    def test_user_model(self):
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()
        self.assertEqual(u.id, 1)
        self.assertEqual(u.email, "test@test.com")
    def test_authenticate(self):
        self.assertTrue(self.user1.username, self.user1.password)

class FavoriteCocktailModelTestCase(TestCase):
    def test_user_model(self):
        cocktail = FavoriteCocktail(
            name='Mojito', 
            user_id=6
        )

        db.session.add(cocktail)
        db.session.commit()
        self.assertEqual(cocktail.name, 'Mojito')
        self.assertEqual(cocktail.user_id, 6)