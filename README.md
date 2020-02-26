# Udacity Full Stack Development Nanodegree

This is the project for **Identity and Access Management** of Udacity's Full Stack Development Nanodegree

---

## Up & Running

### Build Images

The building of frontend would take some time because of npm install. Grab a coffee and have a break before you continue!

```bash
docker-compose build
```

### Prepare Database

#### Identify PG Instance

First, identify Postgres DB instance by typing the following command. Select the one whose name contains **db**

```bash
docker ps -a
```

<img src="doc/01-services.png" alt="Services"/>

#### Restore Database

Then, enter the instance and restore data by typing:

```bash
# enter postgres instance:
docker exec -it trivia_db_1_ac29f1755358 bash
# restore db:
psql -U udacity -d triviaapp < trivia.psql
```

### Check Host Ports

Make sure the following ports are not used on local host:
* **8080** This port will be used by **PG adminer** for web-browser based DB admin
* **60080** This port will be used by Trivia backend for easy debugging
* **3000** This port will be used by Trivia frontend for React app serving

### Launch

Launch the system using docker-compose. Note: the services will communicate using docker internal network
```bash
docker-compose up
```

---

## API Endpoints

### Overview

| Method |               Request URL              |                                                                                               Description                                                                                              |                             Request Arguments                            |                                                Response                                                |
|:------:|:--------------------------------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------:|
|   GET  |           /api/v1/questions/           |                                                                    get questions with pagination (default to 10 questions per page)                                                                    |                           query parameter page                           |              a list of questions, number of total questions, current category, categories              |
|   GET  |           /api/v1/categories/          |                                                                                      get all available categories                                                                                      |                                   None                                   | an object with a single key, categories, that contains a object of id: category_string key:value pairs |
| DELETE |       /api/v1/questions/<int:id>       |                                                                                   delete question using a question ID                                                                                  |                                   None                                   |              an object with key, success, to indicate whether the operation is successful              |
|  POST  |           /api/v1/questions/           |                                                                                           post a new question                                                                                          | POSTed JSON object with key question, answer, difficulty and category_id |              an object with key, success, to indicate whether the operation is successful              |
|  POST  | /api/v1/categories/<int:id>/questions/ |                                                                                     get questions based on category                                                                                    |                                   None                                   |                    a list of questions, number of total questions, current category                    |
|  POST  |        /api/v1/questions/search/       |                                                                 get questions based on whether the search term is inside question body                                                                 |                  POSTed JSON object with key searchTerm                  |                    a list of questions, number of total questions, current category                    |
|  POST  |            /api/v1/quizzes/            | get questions to play the quiz: it takes category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions |     POSTed JSON object with key previous questions and quiz category     |                an object with key question. if no more questions the value will be null                |

### Examples

#### GET /api/v1/questions/

Response
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category_id": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category_id": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category_id": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category_id": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category_id": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category_id": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category_id": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category_id": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category_id": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category_id": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "total_questions": 20
}
```

#### GET /api/v1/categories/

Response
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }
}
```

### DELETE /api/v1/questions/5

Response
```json
{
    "success": true
}
```

### POST /api/v1/categories/1/questions/

Response
```json
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category_id": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category_id": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category_id": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "ANSWER 42", 
      "category_id": 1, 
      "difficulty": 5, 
      "id": 25, 
      "question": "QUESTION 42"
    }
  ], 
  "total_questions": 4
}
```

### POST /api/v1/questions/search/

Request using cURL
```bash
curl -H 'Content-Type: application/json' -X POST -d '{"searchTerm": "What"}' http://localhost:60080/api/v1/questions/search/
```

Response
```json
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category_id": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category_id": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category_id": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category_id": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category_id": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Liver", 
      "category_id": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }
  ], 
  "total_questions": 6
}
```

### POST /api/v1/quizzes/

Request using cURL
```bash
curl -H 'Content-Type: application/json' -X POST -d '{"previous_questions": [], "quiz_category": {"id": 0}}' http://localhost:60080/api/v1/quizzes/
```

Response
```json
{
  "question": {
    "answer": "Apollo 13", 
    "category_id": 5, 
    "difficulty": 4, 
    "id": 2, 
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  }
}
```

---

## Testing

### Overview

All the 7 API endpoints are covered by test cases. See 

### Up & Running

First, identify Postgres DB instance by typing the following command. Select the one whose name contains **backend**

```bash
docker ps -a
```

<img src="doc/01-services.png" alt="Services"/>

Then, enter the instance and execute the tests by typing:

```bash
# enter backend instance:
docker exec -it trivia_backend_1_7e56e27c3b0a bash
# run tests:
flask test
```

Coverage analysis is also enabled. Use the following command to get the coverage analysis report:
```bash
# inside backend instance, type:
flask test --coverage=True
```

<img src="doc/02-coverage-analysis.png" alt="Coverage Analysis"/>

---

## Review

### Code Quality & Documentation

#### Write Clear, Concise and Well Documented Code

I have refactored the project structure following [Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure)'s recommended best practices

#### Write an Informative README

This README includes instructions for:

* How to get the system up & running

* API endpoints documentation

#### Leverage Environment Controls

Volumes for Docker persistent storage are ignored by the Git

### Handling HTTP Requests

#### Follow RESTful Principles

All RESTful APIs are implemented inside [here](/workspace/trivia/backend/application/api/)

#### Utilize Multiple HTTP Request Methods

* Endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
    [here](https://github.com/AlexGeControl/Full-Stacker--06-flask-restful-api-development/blob/ed03644bfe497ff4659546c5b6d5711545798794/workspace/trivia/backend/application/api/questions.py#L47)

* Endpoint to handle GET requests for all available categories.
    [here](https://github.com/AlexGeControl/Full-Stacker--06-flask-restful-api-development/blob/ed03644bfe497ff4659546c5b6d5711545798794/workspace/trivia/backend/application/api/categories.py#L9)

* Endpoint to DELETE question using a question ID.
    [here](https://github.com/AlexGeControl/Full-Stacker--06-flask-restful-api-development/blob/ed03644bfe497ff4659546c5b6d5711545798794/workspace/trivia/backend/application/api/questions.py#L127)

* Endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
    [here](https://github.com/AlexGeControl/Full-Stacker--06-flask-restful-api-development/blob/ed03644bfe497ff4659546c5b6d5711545798794/workspace/trivia/backend/application/api/questions.py#L12)

* Create a GET endpoint to get questions based on category.
    [here](https://github.com/AlexGeControl/Full-Stacker--06-flask-restful-api-development/blob/ed03644bfe497ff4659546c5b6d5711545798794/workspace/trivia/backend/application/api/categories.py#L28)

* Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
    [here](https://github.com/AlexGeControl/Full-Stacker--06-flask-restful-api-development/blob/ed03644bfe497ff4659546c5b6d5711545798794/workspace/trivia/backend/application/api/questions.py#L83)

* Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
    [here](https://github.com/AlexGeControl/Full-Stacker--06-flask-restful-api-development/blob/ed03644bfe497ff4659546c5b6d5711545798794/workspace/trivia/backend/application/api/quizzes.py#L14)

#### Handle Common Errors

All error handlers are registered inside [here](https://github.com/AlexGeControl/Full-Stacker--06-flask-restful-api-development/blob/ed03644bfe497ff4659546c5b6d5711545798794/workspace/trivia/backend/application/api/errors.py#L5)

### API Testing & Documentation

#### Use unittest to Test Flask Application for Expected Behavior

Test cases for all the 7 endpoints are implemented [here](/workspace/trivia/backend/tests)

#### Demonstrate Validity of API Responses

For the three resources, the coverage rates are all above 70%

