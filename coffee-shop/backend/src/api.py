import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

# get drinks for the public users - No permissions are checked here
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    }), 200



'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

# details is allowed onl for users/roles with permission get:drinks-detail
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }), 200


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

# post:drinks permission is required
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(payload):
    try:
        data = request.get_json()
        title = data['title']
        recipe = data ['recipe']
        new_drink = Drink(title = title, recipe = json.dumps(recipe))
        new_drink.insert()
        # drinks = Drink.query.all()
    except:
        abort(400)
    return jsonify({
        'success': True,
        'drinks': [new_drink.long()]  #only the newly created drink #[drink.long() for drink in drinks]
    }), 200


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

# permission patch:drinks is required
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    try:
        data = request.get_json()
        drink = Drink.query.get(id)
        if not drink:       #if not found, abort with proper error code
            abort(404)
        
        title = data.get('title')
        recipe = data.get('recipe')
        
        if title:
            drink.title = data['title']
        if recipe:
            drink.recipe = json.dumps(recipe)
        drink.update()
        # drinks = Drink.query.all()
    except:
        abort(400)
    return jsonify({
        'success': True,
        'drinks': [drink.long()] #[d.long() for d in drinks] requirements only for the updated drink
    }), 200



'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

# check for delete:drinks permission
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        drink = Drink.query.get(id)
        if not drink:
            abort(404)
        drink.delete()
    except:
        abort(400)
    return jsonify({
        'success': True,
        'delete': id
    }), 200


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "bad request"
                    }), 400


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify(e.error), e.status_code
