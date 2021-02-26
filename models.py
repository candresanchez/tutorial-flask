from flask_login import UserMixin #implementa propiedades y metodos (is_authenticated, is_active, get_id(), etc)
from werkzeug.security import generate_password_hash, check_password_hash
from run import db #importo la bd
from bson.objectid import ObjectId #convertir un String a ObjectId

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

from slugify import slugify
from flask import url_for #crea un url a partir del nombre de la función que contiene el decorador route

#Modelo Post 
class Post():
    def __init__(self, user_id, title, content):
        self.id = None
        self.user_id = user_id
        self.title = title
        self.title_slug = None #debe ser unico
        self.content = content
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    def save(self):        
        if not self.title_slug:
            self.title_slug = slugify(self.title)
            print(self.title_slug)
        existe_slug = existe_slug = Post.get_by_slug(self.title_slug) #verifica si el slug ya existe
        count = 0
        #si el slug existe genera agrega un número al final
        while existe_slug is not None:
            count += 1
            self.title_slug = f'{slugify(self.title)}-{count}'
            existe_slug = existe_slug = Post.get_by_slug(self.title_slug)
        if not self.id:            
            post = {
                "user_id": self.user_id,
                "title": self.title,
                "title_slug": self.title_slug,
                "content": self.content
                }
            post_id=db['post'].insert_one(post).inserted_id
            return post_id
    
    def public_url(self):
        return url_for('show_post', slug=self.title_slug)
    
    @staticmethod
    def get_by_slug(slug):        
        t_s = db['post'].find_one({ "title_slug": slug })        
        if t_s is not None:            
            post = Post(t_s['user_id'], t_s['title'], t_s['content'])
            post.id= t_s['_id']            
            post.title_slug = t_s['title_slug']
            return post
        return None
    
    @staticmethod
    def get_all():
        posts = []
        for p in db['post'].find():
            post = Post(p['user_id'], p['title'], p['content'])
            post.id= p['_id']            
            post.title_slug = p['title_slug'] 
            posts.append(post) 
        return posts

        