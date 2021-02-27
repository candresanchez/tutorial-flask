from flask import url_for #crea un url a partir del nombre de la función que contiene el decorador route
from slugify import slugify #crea un slug a partir de una cadena


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