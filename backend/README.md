# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Object Types
### Category
  ```
  {
    id: Integer;
    type: String;
    questions: Question[];
  }
  ```
### Question
```
{
  id: Integer;
  question: String,
  difficulty: String,
  category_id: String,
  category: Category
}
```

## Endpoints

### Get Categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string
```
GET /api/categories
```
#### Response
```
{
  categories: { id: category_string},
  total_categories: Interger
}
```
#### Example Response:
```
{
  'categories': {
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
  },
  'total_categories': 6
}
```

### Get Questions
- Fetch paginated list of questions and dictionary of categories. Result is divided in to default page size of 10.
- Returns 400 Invalid Page Number if
```
GET /api/questions
```
#### Request Params

Param | Type | Optional? | Default Value
--- | --- | --- | ---
page | Integer | Yes | 1

#### Response
```
{
  'questions': Question[];
  'total_questions': Integer,
  'categories': { id: category_string},
  'total_categories': Integer
}
```

#### Sample Response
```
{
  'questions': [
    {
      'id': 1,
      'question': 'Where is TajMahal?',
      'answer': 'India',
      'difficulty': 1,
      'category_id': 3
    },
    {
      'id': 2,
      'question': 'What is full name of MLK?',
      'answer': 'Martin Luther King',
      'difficulty': 1,
      'category_id': 4
    }
  ],
  'total_questions': 2,
  'categories': {
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
  },
  'total_categories': 6
}
```

#### Errors
Code | Description | Condition
--- | --- | ---
400 | Invalid Page Number | When 'page' query param value exceeds maximum number of pages


### Delete Question
- Finds the question by question id and removes it from database
```
DELETE /api/questions/<int:id>
```
#### Response
```
{
  'message': String;
}
```
#### Example Response
```
{
  'message': 'Question deleted successfully'
}
```
#### Errors
Code | Description | Condition
--- | --- | ---
400 | Failed to delete | When enable to delete question

### Create Question
- Create question with given configuration.
- Returns question if created successfully
```
POST /api/questions
```
#### Request Body
```
{
  'question': String;
  'answer': String;
  'difficulty: 'Integer';
  'category': Integer;
}
```
#### Response
```
{
  'id': Integer;
  'question': String;
  'answer': String;
  'difficulty: 'Integer';
  'category': Integer;
}
```
#### Example Response
```
{
  'id': 1,
  'question': 'Who moved my cheese?',
  'answer': 'Thanos',
  'difficulty': 5,
  'category': 1
}
```
#### Errors
Code | Description | Condition
--- | --- | ---
400 | Invalid question data | When anyone of the field is empty
400 | Category not found | When category with specified category id not found
500 | Failed to save question | When system is unable to save question

### Search Questions
- Fetch questions containing search term.
```
GET /api/questions/search
```
#### Request Body
```
{
  'searchTerm': String;
}
```
#### Response
```
{
  'questons': Question[];
  'total_questions': Integer,
  'current_category': Integer
}
```
#### Example Resonse
```
{
  'questions': [
    {
      'id': 1,
      'question': 'Where is TajMahal?',
      'answer': 'India',
      'difficulty': 1,
      'category_id': 3
    },
    {
      'id': 2,
      'question': 'What is full name of MLK?',
      'answer': 'Martin Luther King',
      'difficulty': 1,
      'category_id': 4
    }
  ],
  'total_questions': 2,
  'current_category': 1
}
```

### Get Questions By Category
- Fetch questions filtered by specified category id
```
GET /api/categories/<int:id>/questions
```
#### Request Params
Param | Type | Optional? | Default Value | Description
--- | --- | --- | --- | ---
id | Integer | No | | Category Id

#### Response
```
{
  'questons': Question[];
  'total_questions': Integer,
  'current_category': Integer
}
```
#### Example Resonse
```
{
  'questions': [
    {
      'id': 1,
      'question': 'Where is TajMahal?',
      'answer': 'India',
      'difficulty': 1,
      'category_id': 3
    },
    {
      'id': 2,
      'question': 'What is full name of MLK?',
      'answer': 'Martin Luther King',
      'difficulty': 1,
      'category_id': 4
    }
  ],
  'total_questions': 2,
  'current_category': 1
}
```

### Get Random Question By Category
- Fetch randomly selected question from the list of questions for given category and not already served
- 'previous_questions' in request body specified questions already served. Hence, these questions will be excluded while picking next question
```
POST /api/quizzes
```
#### Request Body
```
{
  'previous_questions': Integer[];
  'quiz_category': Integer
}
```
#### Response
```
{
  'question': String;
}
```
#### Example Response
```
{
  'question': {
    'id': 1,
    'question': 'Where is TajMahal?',
    'answer': 'India',
    'difficulty': 1,
    'category_id': 3
  }
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```