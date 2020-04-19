from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request, Response
from werkzeug.security import generate_password_hash
from flask_swagger_ui import get_swaggerui_blueprint

@app.route('/api/user/add', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    # validate the received values
    if _name and _email and _password and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)
        mongo.db.user.insert({'name':_name, 'email':_email, 'password':_hashed_password})
        res = jsonify(message='User added successfully')
        res.status_code = 200
        return res
    else:
        return jsonify('Failed to add user.')

@app.route('/api/user')
def get_users():
    users = mongo.db.user.find()
    count = mongo.db.user.estimated_document_count()
    responses = {"message":"Data found!", "data":users, "total_records":count}
    res = dumps(responses)
    return Response(res, mimetype="application/json")

@app.route('/api/user/<id>')
def get_user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    res = dumps({"message":"User found!", "data":user})
    return Response(res, mimetype="application/json")

@app.route('/api/user/update', methods=['PUT'])
def update_user():
    _json = request.json
    _id = _json['_id']
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    if _name and _email and _password and _id and request.method == 'PUT':
        _hashed_password = generate_password_hash(_password)
        mongo.db.user.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set':{'name':_name, 'email':_email, 'password':_hashed_password}})
        res = jsonify(message="Update user successfully!")
        res.status_code = 200
        return res
    else:
        return jsonify("Failed to update user")

@app.route('/api/user/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id':ObjectId(id)})
    res = jsonify(message="Delete user successfully!")
    return res

@app.route('/swagger')
def root():
    return app.send_static_file('swagger.json')

if __name__ == '__main__':
    swagger_url = "/api-docs"
    api_url = "http://localhost:5000/swagger"

    swaggerui_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={
            'swagger': '2.0',
            'app_name': "Rest API with Flask and MongoDB"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)
    app.run(debug=True)

