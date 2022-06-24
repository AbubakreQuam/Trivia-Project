from importlib.resources import contents
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from settings import DB_USER, DB_PASSWORD
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase): 
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, "localhost:5432", "triivia")
        setup_db(self.app, self.database_path)
        self.create_question = {"question": "Programmer's Name?", "answer": "Abubakre Quamarudeen", "category": 5, "difficulty": 2, "rating":4}
       
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
        
    '''1. Testing for Getting all questions based on pagination'''"""Test _____________ """
    
    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalQuestions'], len(Question.query.all()))

    def test_for_questions_error(self):
        res = self.client().get('/questions?page=1000')
        data= json.loads(res.data)
        mes = self.client().post('/questions')
        datum= json.loads(mes.data)
     

        self.assertEqual(mes.status_code, 405)
        self.assertEqual(datum['success'], False)
        self.assertEqual(datum['message'], 'Method Not Allowed')

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    '''2. Testing for Getting all categories'''"""Test _____________ """

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    

    def test_for_categories_error(self):
        res = self.client().get('/categories/3')
        mes = self.client().post('/categories')
        data= json.loads(mes.data)
        datum= json.loads(res.data)

        self.assertEqual(mes.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

        self.assertEqual(res.status_code, 404)
        self.assertEqual(datum['success'], False)
        self.assertEqual(datum['message'], 'Resource Not Found')

    '''3. Testing for Deleting a Particular Question'''"""Test _____________ """

    def test_delete_a_particular_question(self):
        '''Specify another question_id between (5-13)'''
        res = self.client().delete('/delete/7')
        
        #Checking crude persistence
        deleted_value = Question.query.get(7)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(deleted_value, None)
    

    def test_for_deleting_questions_error(self):
        res = self.client().delete('/delete/5000')
        data= json.loads(res.data)
        mes = self.client().post('/categories')
        datum= json.loads(mes.data)


        self.assertEqual(mes.status_code, 405)
        self.assertEqual(datum['success'], False)
        self.assertEqual(datum['message'], 'Method Not Allowed')

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        

    '''4. Testing for Getting all questions based on category'''"""Test _____________ """

    def test_get_all_questions_based_on_category(self):
        res = self.client().get('/categories/1/questions')
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        

    def test_all_questions_based_on_category_error(self):
        res = self.client().get('/categories/100/questions')
        data= json.loads(res.data)
        mes = self.client().post('/categories/3/questions')
        datum= json.loads(mes.data)
     

        self.assertEqual(mes.status_code, 405)
        self.assertEqual(datum['success'], False)
        self.assertEqual(datum['message'], 'Method Not Allowed')

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    '''5. Testing for Searching for questions'''"""Test _____________ """

    def test_for_searching_questions(self):
        res = self.client().post('/questions/search', json={"searchTerm": "What"})
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        

    def test_for_searching_error(self):
        res = self.client().post('/questions/search')
        data= json.loads(res.data)
        mes = self.client().get('/questions/search')
        datum= json.loads(mes.data)
     

        self.assertEqual(mes.status_code, 405)
        self.assertEqual(datum['success'], False)
        self.assertEqual(datum['message'], 'Method Not Allowed')

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    '''6. Testing for Creating for questions'''"""Test _____________ """

    def test_for_creating_questions(self):
        res = self.client().post('/create', json=self.create_question)
        data= json.loads(res.data)

        #Checking Crud persistence
        Inserted_data = Question.query.filter(Question.question=="Programmer's Name?", Question.answer=="Abubakre Quamarudeen")
        for a in Inserted_data:
            print()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(a.question, "Programmer's Name?")

    def test_for_creating_questions_error(self):
        res = self.client().post('/create')
        data= json.loads(res.data)
        mes = self.client().get('/create')
        datum= json.loads(mes.data)
     

        self.assertEqual(mes.status_code, 405)
        self.assertEqual(datum['success'], False)
        self.assertEqual(datum['message'], 'Method Not Allowed')

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    '''7. Testing for Playing a quizzes'''"""Test _____________ """

    def test_for_quizzes(self):
        res = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category":"ALL"})
        data= json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
        

    def test_for_quizzes_error(self):
        res = self.client().post('/quizzes')
        data= json.loads(res.data)
        mes = self.client().get('/quizzes')
        datum= json.loads(mes.data)
     

        self.assertEqual(mes.status_code, 405)
        self.assertEqual(datum['success'], False)
        self.assertEqual(datum['message'], 'Method Not Allowed')

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    '''7. Testing for Creating a Category'''"""Test _____________ """

    def test_for_creating_category(self):
        res = self.client().post('/add', json={"type":"Agriculture"})
        data= json.loads(res.data)

        #Checking Crud persistence
        Inserted_data = Category.query.filter(Category.type=="Agriculture")
        for a in Inserted_data:
            print()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(a.type, "Agriculture")

    def test_for_creating_category_error(self):
        res = self.client().post('/add')
        data= json.loads(res.data)
        mes = self.client().get('/add')
        datum= json.loads(mes.data)
     

        self.assertEqual(mes.status_code, 405)
        self.assertEqual(datum['success'], False)
        self.assertEqual(datum['message'], 'Method Not Allowed')

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

        
    
    
     

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()