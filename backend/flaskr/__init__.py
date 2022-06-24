import os
from typing import KeysView
from flask import Flask, flash, redirect, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import null
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, DELETE,')
        return response

   

    @app.route("/questions")
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        questions = paginate_questions(request, selection)

    
        list_categories = Category.query.order_by(Category.id).all()
        categories= {a.id:a.type for a in list_categories}
        totalQuestions= len(Question.query.all())
        

        if len(questions) == 0:
            abort(404)

        return jsonify(
            {
               "success": True,
                "questions": questions,
                "totalQuestions": totalQuestions,
                "categories": categories                
            }
                        
                
          
        )
    


    @app.route('/categories')
    def retrieve_categories():
        list_categories = Category.query.order_by(Category.id).all()
        categories= {a.id:a.type for a in list_categories}
        
        if len(list_categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": categories
              
            }
        )
   
    @app.route('/delete/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question_to_delete= Question.query.filter(Question.id==question_id).one_or_none()  

            question_to_delete.delete()

            return jsonify(
                {
                    "success": True,
                    "state_code": 200

                }
            )
        except Exception:
            abort(422)

    @app.route('/categories/<int:categories_id>/questions', methods=['GET'])
    def category_based_questions(categories_id):
        try:
            question = Question.query.filter(Question.category==str(categories_id)).all()
            total_questions=Question.query.filter(Question.category==str(categories_id)).count()
            category_name=Category.query.get(categories_id)
            questions = paginate_questions(request, question)
            current_category=category_name.type
            
            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "totalQuestions": total_questions,
                    "currentCategory": current_category
                        
                            
                }
            )
        except Exception:
            abort(422)
        
        

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()

        search_term = body.get("searchTerm", None)

        if search_term is None:
            flash('Error', 'Input a question to search')
        
        try:
            search_questions= '%' + search_term + '%'
            response=Question.query.filter(Question.question.ilike(search_questions)).all()
            total_questions=Question.query.filter(Question.question.ilike(search_questions)).count()
            questions = paginate_questions(request, response)

            return jsonify({
                'success': True,
                'questions': questions,
                'totalQuestions': total_questions,
            })
        except Exception:
            abort(404)

    @app.route("/create", methods=["POST"])
    def create_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)
        new_rating = body.get("rating", None)

        if new_question =='' and  new_answer =='':
            abort(400)

        try:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty, rating= new_rating)
            question.insert()
            
            return jsonify(
                {
                    "success": True
                }
            )

        except Exception:
            abort(422)


    '''Route Handler for adding new Category'''
    @app.route("/add", methods=["POST"])
    def create_category():
        body = request.get_json()

       
        new_category = body.get("type", None)
        

        if new_category =='':
            abort(400)


        try:
            question = Category(type=new_category)
            question.new()
            
            return jsonify(
                {
                    "success": True
                }
            )

        except Exception:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        body = request.get_json()
        data=[]
        
        question_list = body.get("previous_questions", None)
        print("question_list=", question_list)
        quiz_cat = body.get("quiz_category", None)

        '''Used My Own format to return randomized questions based on each category and for all in general'''
        try:
            if len(quiz_cat) == 3:
                next_question =Question.query.all()
                for info in next_question:
                    data.append(info.id)
                print()
                if question_list==[]:
                    value= random.choice(data)

                    next_question =Question.query.filter(Question.id==value)
                    for question in next_question:
                        print()

                    return jsonify(
                        {
                            "success": True,
                            "data": data,
                            'question': {
                        'id': question.id,
                        'question': question.question,
                        'answer': question.answer,
                        'difficulty': question.difficulty,
                        'category': question.category,
                        'rating': question.rating
                        }
                            
                        }
                        )
                else:
                    for list in question_list: data.remove(list)
                    if len(data)==0:
                        return jsonify(
                            {
                                
                                'question': False
                                
                            }
                            )
                    else:
                        value= random.choice(data)

                        next_question =Question.query.filter(Question.id==value)
                        for question in next_question:
                            print()


                        return jsonify(
                            {
                                "success": True,
                                "data": data,
                                'question': {
                            'id': question.id,
                            'question': question.question,
                            'answer': question.answer,
                            'difficulty': question.difficulty,
                            'category': question.category,
                            'rating': question.rating
                            }
                                
                            }
                            )
            else:
                next_question =Question.query.filter(Question.category==quiz_cat)
                for info in next_question:
                    data.append(info.id)
                print(data)
                if question_list==[]:
                    value= random.choice(data)

                    next_question =Question.query.filter(Question.id==value)
                    for question in next_question:
                        print()

                    return jsonify(
                        {
                            "success": True,
                            "data": data,
                            'question': {
                        'id': question.id,
                        'question': question.question,
                        'answer': question.answer,
                        'difficulty': question.difficulty,
                        'category': question.category,
                        'rating': question.rating
                        }
                            
                        }
                        )
                else:
                    for list in question_list: data.remove(list)
                    if len(data)==0:
                        return jsonify(
                            {
                                
                                'question': False
                                
                            }
                            )
                    else:
                        value= random.choice(data)

                        next_question =Question.query.filter(Question.id==value)
                        for question in next_question:
                            print()


                        return jsonify(
                            {
                                "success": True,
                                "data": data,
                                'question': {
                            'id': question.id,
                            'question': question.question,
                            'answer': question.answer,
                            'difficulty': question.difficulty,
                            'category': question.category,
                            'rating': question.rating
                            }
                                
                            }
                            )               
        except Exception:
            abort(404)

            

          
    @app.errorhandler(404)
    def Not_found(error):
        return jsonify({
        "success": False, 
        "error": 404,
        "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad Request"
        }), 400

    @app.errorhandler(405)
    def wrong_method(error):
        return jsonify({
        "success": False, 
        "error": 405,
        "message": "Method Not Allowed"
        }), 405
    return app
    
    

