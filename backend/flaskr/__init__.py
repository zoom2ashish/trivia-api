import os
from flask import Flask, request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug import exceptions as _exceptions
from models import setup_db, Question, Category
import json
import math
import sys

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  DONE: @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": { "origins": "*" }})

  # Setup CORS header
  '''
  DONE: @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE')
    return response

  def getPaginatedResult(result, page, size = QUESTIONS_PER_PAGE):
    start = QUESTIONS_PER_PAGE * (page - 1)
    end = QUESTIONS_PER_PAGE * page
    return result[start:end]

  '''
  DONE: @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route('/api/categories', methods=['GET'])
  def get_categories():
    categories = {
      category.id: category.type for category in Category.query.all()
    }
    return jsonify({
      'categories': categories,
      'total_categories': len(categories)
    })


  '''
  DONE: @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
  @app.route('/api/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = QUESTIONS_PER_PAGE * (page - 1)
    end = QUESTIONS_PER_PAGE * page
    queryResult = Question.query.all()

    total_questions = len(queryResult)
    maxPages = math.ceil(total_questions / QUESTIONS_PER_PAGE)
    if (total_questions > 0 and page > maxPages):
      abort(Response("Invalid Page Number"))

    questionsPerPage = getPaginatedResult(queryResult, page)

    questions = [
      question.format() for question in questionsPerPage
    ]
    categories = {
      category.id: category.type for category in Category.query.all()
    }

    return jsonify({
      'questions': questions,
      'total_questions': total_questions,
      'categories': categories,
      'current_category': None
    })

  '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
  @app.route('/api/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    question = Question.query.filter(Question.id == id).one_or_none()
    try:
      if question is not None:
        question.delete()

      return jsonify({
        'message': 'Question deleted successfully'
      })
    except:
      print(sys.exc_info())
      abort(400, 'Failed to delete question with requested id')

  '''
  @TODO: DONE
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
  @app.route('/api/questions', methods=['POST'])
  def add_question():
    try:
      data = request.get_json()
    except:
      abort(400, 'Invalid data')

    question = data.get('question')
    answer = data.get('answer')
    difficulty = data.get('difficulty')
    category = data.get('category')

    if not question or not answer or not difficulty or not category:
      abort(400, 'Invalid question data.')

    category = Category.query.filter(Category.id == category).one_or_none()
    if category is None:
      abort(400, 'Specified category not found.')

    try:
      question = Question(question, answer, category.id, difficulty)
      question.category = category
      question.insert()

      return jsonify(question.format())
    except:
      abort(500, "Failed to save question")

  '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
  @app.route('/api/questions/search', methods=['POST'])
  def search_questions():
    data = request.get_json()
    searchTerm = data['searchTerm']
    page = 1
    queryResult = Question.query.filter(Question.question.ilike('%{}%'.format(searchTerm))).all()
    total_questions = len(queryResult)
    questionsPerPage = getPaginatedResult(queryResult, page)

    questions = [
      question.format() for question in questionsPerPage
    ]

    return jsonify({
      'questions': questions,
      'total_questions': total_questions,
      'current_category': None
    })

  '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  @app.route('/api/categories/<int:id>/questions')
  def get_questions_by_category(id):
    category = Category.query.filter(Category.id == id).one_or_none()
    if category is None:
      abort(400, "Category not found")

    questions = [ question.format() for question in Question.query.filter(Question.category_id == category.id).all() ]
    return jsonify({
      'questions': questions,
      'total_questions': len(questions),
      'current_category': id
    })

  '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  @app.errorhandler(500)
  def handle_internal_server_error(e):
    return jsonify({
      'code': 500,
      'error': 'Internal Server Error',
      'details': e.description
    }), 500

  @app.errorhandler(400)
  def handle_internal_server_error(e):
    return jsonify({
      'code': 400,
      'error': 'Bad Request',
      'details': e.description
    }), 400

  return app

