import os
import unittest
import json
from random import randint
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}@{}/{}".format(
            'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        self.ctx.push()
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
        self.ctx.pop()

    def insert_questions_for_test(self, category, count=15):
        questions = []
        for i in range(count):
            question = Question('Q%s' % i, 'A%s' %
                                i, category.id, randint(1, 4))
            question.category = category
            question.insert()
            questions.append(question)
        return questions

    def delete_questions(self, questions=[]):
        for question in questions:
            question.delete()

    """
    DONE: TODO
    Write at least one test for each test for successful operation and
    for expected errors.
    """

    def test_get_questions_no_records(self):
        response = self.client().get('/api/questions')
        data = response.get_json()
        self.assertEqual(data['questions'], [])
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(response.status_code, 200)

    def test_get_questions_one_record(self):
        category = Category("Science")
        category.insert()
        question = Question('Q1', 'A1', "1", category.id)
        question.category = category
        question.insert()
        response = self.client().get('/api/questions')
        data = response.get_json()
        print(data)
        # self.assertEqual(data['questions'], [])
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(response.status_code, 200)
        question.delete()
        category.delete()

    def test_get_questions_handle_multiple_pages(self):
        # Insert Records for
        category = Category("Science")
        category.insert()
        questions = self.insert_questions_for_test(category)

        response = self.client().get('/api/questions?page=2')
        data = response.get_json()
        self.assertEqual(data['total_questions'], 15)
        self.assertEqual(len(data['questions']), 5)

        self.delete_questions(questions)
        category.delete()

    def test_get_questions_by_category_valid_category(self):
        category = Category("Science")
        category.insert()
        questions = self.insert_questions_for_test(category, 15)

        response = self.client().get(
            '/api/categories/{}/questions'.format(category.id))
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_questions'], len(questions))

        self.delete_questions(questions)
        category.delete()

    def test_get_questions_by_category_invalid_category(self):
        category = Category("Science")
        category.insert()
        questions = self.insert_questions_for_test(category, 15)

        response = self.client().get('/api/categories/{}/questions'.format(0))
        data = response.get_json()
        self.assertEqual(response.status_code, 400)

        self.delete_questions(questions)
        category.delete()

    def test_add_question_valid_payload(self):
        category = Category('Dummy')
        category.insert()
        response = self.client().post('/api/questions', json={
            'question': 'Who moved my cheese?',
            'answer': 'Not Me!',
            'difficulty': 5,
            'category': category.id
        })

        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['question'], 'Who moved my cheese?')
        self.assertEqual(data['category_id'], category.id)

        question = Question.query.filter(Question.id == data['id']).first()
        self.assertEqual(question.question, data['question'])
        self.assertEqual(question.category_id, category.id)

        question.delete()
        category.delete()

    def test_add_question_invalid_category_in_payload(self):
        response = self.client().post('/api/questions', json={
            'question': 'Who moved my cheese?',
            'answer': 'Not Me!',
            'difficulty': 5,
            'category': 1
        })
        self.assertEqual(response.status_code, 400)

    def test_add_question_invalid_question_data(self):
        category = Category('Dummy')
        category.insert()
        response = self.client().post('/api/questions', json={
            'question': '',
            'answer': 'Not Me!',
            'difficulty': 5,
            'category': category.id
        })
        self.assertEqual(response.status_code, 400)

        response = self.client().post('/api/questions', json={
            'question': 'Valid Question',
            'answer': '',
            'difficulty': 5,
            'category': category.id
        })
        self.assertEqual(response.status_code, 400)

        response = self.client().post('/api/questions', json={
            'question': 'Valid Question',
            'answer': 'Valid Answer',
            'difficulty': 0,
            'category': category.id
        })
        self.assertEqual(response.status_code, 400)

        category.delete()

    def test_search_questions_matching_word(self):
        category = Category("Science")
        category.insert()
        question = Question('Who moved my cheese', 'Not Me!', "1", category.id)
        question.category = category
        question.insert()

        response = self.client().post('/api/questions/search',
                                      json={'searchTerm': 'cheese'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_questions'], 1)

        question.delete()
        category.delete()

    def test_search_questions_non_matching_word(self):
        category = Category("Science")
        category.insert()
        question = Question('Who moved my cheese', 'Not Me!', "1", category.id)
        question.category = category
        question.insert()

        response = self.client().post('/api/questions/search',
                                      json={'searchTerm': 'happy'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['total_questions'], 0)

        question.delete()
        category.delete()

    def test_delete_question_valid_id(self):
        category = Category("Science")
        category.insert()
        question = Question(
            'Who moved my cheese', 'Not Me!', "1",
            category.id)
        question.category = category
        question.insert()

        response = self.client().delete(
            '/api/questions/{}'.format(question.id))
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        dbEntry = Question.query.filter(
            Question.id == question.id).one_or_none()
        self.assertEqual(dbEntry, None)

        question.delete()
        category.delete

    def test_delete_question_invalid_id(self):
        category = Category("Science")
        category.insert()
        question = Question('Who moved my cheese', 'Not Me!', "1", category.id)
        question.category = category
        question.insert()

        response = self.client().delete('/api/questions/1')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        dbEntry = Question.query.filter(
            Question.id == question.id).one_or_none()
        self.assertNotEqual(dbEntry, None)
        self.assertEqual(dbEntry.question, question.question)

        question.delete()
        category.delete

    def test_get_random_question(self):
        category = Category("Science")
        category.insert()
        question = Question('Who moved my cheese', 'Not Me!', "1", category.id)
        question.category = category
        question.insert()

        response = self.client().post('/api/quizzes', json={
            'previous_questions': [],
            'quiz_category': None
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('question').get(
            'question'), question.question)

        question.delete()
        category.delete()

    def test_get_random_question_for_last_question(self):
        category = Category("Science")
        category.insert()
        question = Question('Who moved my cheese', 'Not Me!', "1", category.id)
        question.category = category
        question.insert()

        response = self.client().post('/api/quizzes', json={
            'previous_questions': [question.id],
            'quiz_category': None
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('question'), None)

        question.delete()
        category.delete()

    def test_get_random_question_handle_category(self):
        category = Category("Science")
        category.insert()
        question = Question('Who moved my cheese', 'Not Me!', "1", category.id)
        question.category = category
        question.insert()

        response = self.client().post('/api/quizzes', json={
            'previous_questions': [],
            'quiz_category': category.id
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('question').get(
            'question'), question.question)

        question.delete()
        category.delete()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
