from flask import Blueprint, request, jsonify
from marvel_inventory.helpers import token_required
from marvel_inventory.models import db, Char, char_schema, chars_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 800}

@api.route('/chars', methods = ['POST'])
@token_required
def create_char(current_user_token):
    name = request.json['name']
    description = request.json['description']
    first_appeared = request.json['first_appeared']
    super_power = request.json['super_power']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    char = Char(name, description, first_appeared, super_power, user_token = user_token)
    

    db.session.add(char)
    db.session.commit()

    response = char_schema.dump(char)
    return jsonify(response)

@api.route('/chars', methods = ['GET'])
@token_required
def get_chars(current_user_token):
    owner = current_user_token.token
    chars = Char.query.filter_by(user_token = owner).all()
    response = chars_schema.dump(chars)
    return jsonify(response)

@api.route('/chars/<id>', methods = ['GET'])
@token_required
def get_char(current_user_token, id):
    char = Char.query.get(id)
    response = char_schema.dump(char)
    return jsonify(response)

@api.route('/chars/<id>', methods = ['POST'])
@token_required
def update_char(current_user_token, id):
    char = Char.query.get(id)
    print(char)
    print(current_user_token)
    if char:
        char.name = request.json['name']
        char.description = request.json['description']
        char.first_appeared = request.json['first_appeared']
        char.super_power = request.json['super_power']
        char.user_token = current_user_token.token
        db.session.commit()
        response = char_schema.dump(char)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That char does not exist!'})
    
@api.route('/chars/<id>', methods = ['DELETE'])
@token_required
def delete_char(current_user_token, id):
    char = Char.query.get(id)
    if char:
        db.session.delete(char)
        db.session.commit()
        response = char_schema.dump(char)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That car does not exist!'})