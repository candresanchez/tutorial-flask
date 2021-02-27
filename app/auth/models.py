from flask_login import UserMixin #implementa propiedades y metodos (is_authenticated, is_active, get_id(), etc)
from werkzeug.security import generate_password_hash, check_password_hash #hash a la contraseña
from bson.objectid import ObjectId #convertir un String a ObjectId

from run import db #importo la bd


class User(UserMixin):
    def __init__(self, name, email, is_admin=False):
        self.id = None
        self.name = name
        self.email = email
        self.password = None
        self.is_admin = is_admin

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            user = {
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "is_admin": self.is_admin
                }
            user_id=db['user'].insert_one(user).inserted_id
            return user_id
    
    def __repr__(self):
        return '<User {}>'.format(self.email)
    
    @staticmethod
    def get_by_id(user_id):
        u = None
        if ObjectId.is_valid(user_id): #chequea si un string OID es válido, tiene la notación de MongoDB      
            u = db['user'].find_one({ "_id": ObjectId(user_id)})        
        if u is not None:            
            user = User(u['name'], u['email'], u['is_admin'])
            user.password = u['password']
            user.id = u['_id']            
            return user
    
    @staticmethod
    def get_by_email(email):        
        u = db['user'].find_one({ "email": email })        
        if u is not None:            
            user = User(u['name'], u['email'], u['is_admin'])
            user.password = u['password']
            user.id = u['_id']        
            return user
        return None