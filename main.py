from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/user/add', methods=['POST'])
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

@app.route('/users')
def get_users():
    users = mongo.db.user.find()
    count = mongo.db.user.estimated_document_count()
    responses = {"message":"Data found!", "data":users, "total_records":count}
    res = dumps(responses)
    return res

@app.route('/user/<id>')
def get_user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    res = dumps({"message":"User found!", "data":user})
    return res

@app.route('/user/update', methods=['PUT'])
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

@app.route('/user/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id':ObjectId(id)})
    res = jsonify(message="Delete user successfully!")
    return res

if __name__ == '__main__':
    app.run(debug=True)