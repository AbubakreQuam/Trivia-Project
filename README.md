## The Brain Storming Trivia Web Application
A Brain Storming Trivia Web Application is a database application for creating and running competitive trivia games. With Brain Storming Trivia Web Application a user can play this trivia game which is educative. The Brain Storming Trivia Web Application game allows user to create new category, in which questions are create based on the category. A user can play the Trivia game 5 times and at the end of the game a result is displayed to show the user's total score. The Brain Storming Trivia Web Application will need to store information (Questions and categories) in order to play the trivia games. 


All backend code follows PEP8 style guidelines.


### Getting Started
Pre-requisites and Local Development
Developers using this project should already have Python3, pip and node installed on their local machines.

### Backend
From the backend folder run pip install requirements.txt. All required packages are included in the requirements file.

To run the application run the following commands:

export FLASK_APP=flaskr

export FLASK_ENV=development

flask run

These commands put the application in development and directs our application to use the __init__.py file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the Flask documentation.

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

### Frontend
From the frontend folder, run the following commands to start the client:

npm install // only once to install dependencies
npm start 
By default, the frontend will run on localhost:3000.

### Tests
In order to run tests navigate to the backend folder and run the following commands:

dropdb trivia_test

createdb trivia_test

psql trivia_test < trivia.psql

python test_flaskr.py

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.


### API Reference

### Getting Started

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

Authentication: This version of the application does not require authentication or API keys.

### Error Handling

The API will return four error types when requests fail:

400: Bad Request

404: Resource Not Found

422: Not Processable

405: Method Not Allowed

Errors are returned as JSON objects in the following format:

{

        "success": False, 
        "error": 404,
        "message": "Resource Not Found"
		
}

{

        "success": False, 
        "error": 422,
        "message": "unprocessable"
		
}

{

        "success": False, 
        "error": 400,
        "message": "Bad Request"
		
}

{

        "success": False, 
        "error": 405,
        "message": "Method Not Allowed"
		
}

### Endpoints

### GET /categories

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

- Sample: curl  http://127.0.0.1:5000/categories

{

    "success": True,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
  }
  
}



### GET /questions

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: 'page' - integer (Include a request argument to choose page number, starting from 1.)
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

- curl http://127.0.0.1:5000/questions shows the first page content
- curl http://127.0.0.1:5000/questions?page=3 which specify and shows the content of page 3

{

    {
	
	  "categories": {
		"1": "Science", 
		"2": "Art", 
		"3": "Geography", 
		"4": "History", 
		"5": "Entertainment", 
		"6": "Sports"
	  }, 
	  "questions": [
		{
		  "answer": "Abubakre Quamarudeen", 
		  "category": "5", 
		  "difficulty": 2, 
		  "id": 1, 
		  "question": "Programmer's Name?", 
		  "rating": 4
		}, 
		{
		  "answer": "George Washington Carver", 
		  "category": "4", 
		  "difficulty": 2, 
		  "id": 9, 
		  "question": "Who invented Peanut Butter?\t", 
		  "rating": 3
		}
	  ], 
	  "success": true, 
	  "totalQuestions": 2
	}

}


### GET /categories/{categories_id}/questions 

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: 'categories_id'- integer
- Returns: An object with questions for the specified category, total questions, and current category string

- curl  http://127.0.0.1:5000/categories/4/questions 

	{

	  "currentCategory": "Entertainment", 
	  "questions": [
		{
		  "answer": "Abubakre Quamarudeen", 
		  "category": "5", 
		  "difficulty": 2, 
		  "id": 1, 
		  "question": "Programmer's Name?", 
		  "rating": 4
		}
	  ], 
	  "success": true, 
	  "totalQuestions": 1

	}

### DELETE /delete/{question_id}

- Deletes a specified question using the id of the question
- Request Arguments: 'question_id' - integer
- Returns: Only the appropriate HTTP status code. 

- curl -X DELETE http://127.0.0.1:5000/delete/10

{

    "success": True,
    "state_code": 200


}


### POST /questions/search

- Sends a post request in order to search for a specific question by search term
- Request Body:

{

	"searchTerm": "this is the term the user is looking for"
	
}

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

- curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{ "searchTerm": "this is the term the user is looking for}'


	{

		"success": True,
		"questions": [
			{
			"id": 1,
			"question": "This is a question",
			"answer": "This is an answer",
			"difficulty": 5,
			"category": 5,
			"rating": 4
			}
		],
		"totalQuestions": 100,
		"currentCategory": "Entertainment"

	}


### POST /quizzes

- Sends a post request in order to get the next question
- Request Body:

	{

		"previous_questions": [1, 4, 20, 15]
		"quiz_category": "category_id"

	 }


- Returns: a single new question object

- curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{ 'previous_questions': [1, 4, 20, 15], 'quiz_category':'category_id'}'


	{

		"success": True,
		"question": {
			"id": 1,
			"question": "This is a question",
			"answer": "This is an answer",
			"difficulty": 5,
			"category": 4,
			"rating": 3
		}

	}



### POST  /create

- Sends a post request in order to add a new question
- Request Body:


	{

	  "question": "Heres a new question string",
	  "answer": "Heres a new answer string",
	  "difficulty": 1,
	  "category": 3,
	  "rating":3

	}

- Returns: Does not return any new data

- curl http://127.0.0.1:5000/create -X POST -H "Content-Type: application/json" -d '{'question':'Heres a new question string', 'answer':'Heres a new answer string', 'category':3, 'difficulty':1, 'rating':3}'

	{

		"success": True


	}



### POST  /add

- Sends a post request in order to add a new category
- Request Body:


	{

	  "type": "Agriculture Science",


	}

- Returns: Does not return any new data

- curl http://127.0.0.1:5000/add -X POST -H "Content-Type: application/json" -d '{'type': 'Agriculture Science'}


	{

		 "success": True


	}


### Deployment N/A

### Authors
Yours truly, Software Developer Abubakre Quamarudeen

### Acknowledgements
The awesome team at Udacity and all of the students, soon to be full stack extraordinaires!
