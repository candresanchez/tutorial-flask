from flask import abort
from flask import render_template #Renderiza una plantilla creada con jinja2

from app.models import Post
from . import public_bp

@public_bp.route('/')
def index():
    posts = Post.get_all() #obtiene una lista de Objetos Post   
    return render_template("public/index.html", posts=posts)


#ejemplo para usar slug
@public_bp.route("/p/<string:slug>/")#muestra un post
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("public/post_view.html", post=post)