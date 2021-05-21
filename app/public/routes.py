import logging

from flask import abort
from flask import render_template #Renderiza una plantilla creada con jinja2
#from flask import current_app

from app.models import Post
from . import public_bp

loggeer = logging.getLogger(__name__)#creo un logger para este modulo

@public_bp.route('/')
def index():
    #current_app.logger.info('Mostrando los posts del blog') este logger no muestra el modulo completo
    loggeer.info('Mostrando los posts del blog')#este logger me muestra el modulo completo
    posts = Post.get_all() #obtiene una lista de Objetos Post   
    return render_template("public/index.html", posts=posts)

from werkzeug.exceptions import NotFound

#ejemplo para usar slug
@public_bp.route("/p/<string:slug>/")#muestra un post
def show_post(slug):
    loggeer.info('Mostrando un post')
    loggeer.debug(f'Slug: {slug}')
    post = Post.get_by_slug(slug)
    if post is None:
        #abort(404) este también funciona
        raise NotFound(slug)
    return render_template("public/post_view.html", post=post)

#Ejemplo mostrar error divisiòn por cero
@public_bp.route("/error")
def show_error():    
    res = 1 / 0
    posts = Post.get_all()
    return render_template("public/index.html", posts=posts)