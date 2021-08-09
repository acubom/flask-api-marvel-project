from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid

from flask_marshmallow import Marshmallow

from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Char', backref = 'owned', lazy = True)

    def __init__(self, name, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.name = name
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(24)

class Char(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    first_appeared = db.Column(db.String(50))    
    super_power = db.Column(db.String(100))   
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)    
    owner = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, first_appeared, super_power, owner, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.first_appeared = first_appeared        
        self.super_power = super_power
        self.owner = owner

    def set_id(self):
        return (secrets.token_urlsafe())

class CharSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description','first_appeared', 'super_power']   

char_schema = CharSchema()
chars_schema = CharSchema(many=True)