import logging

from flask import render_template #Renderiza una plantilla creada con jinja2
from flask import redirect #redirige al cliente a una pagina especifica
from flask import url_for #crea un url a partir del nombre de la función que contiene el decorador route

from flask_login import current_user, login_required #Implementa el Login de usuarios
from flask import abort

from app.models import Post
from . import admin_bp
from .forms import PostForm

from app.auth.decorators import admin_required  # lo creamos nosotros

logger = logging.getLogger(__name__)#creo un logger para este modulo

# Lista todo los posts
@admin_bp.route("/admin/posts/")
@login_required
@admin_required
def list_posts():
    posts = Post.get_all()
    return render_template("admin/posts.html", posts=posts)

# Crea un nuevo Post en el Blog
@admin_bp.route("/admin/post/", methods=['GET', 'POST'])
@login_required #comprueba si el usuario esta autenticado
@admin_required #comprueba si el usuario es administrador (is_admin=True)
def post_form():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data        
        content = form.content.data
        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()
        logger.info(f'Guardando nuevo post {title}')#este logger me muestra el modulo completo
        return redirect(url_for('admin.list_posts'))
    return render_template("admin/post_form.html", form=form)


# Actualiza un post existente en el Blog
@admin_bp.route("/admin/post/<string:post_id>", methods=['GET', 'POST'])
@login_required #comprueba si el usuario esta autenticado
@admin_required #comprueba si el usuario es administrador (is_admin=True)
def update_post_form(post_id):
    post = Post.get_by_id(post_id)
    if post is None:
        logger.info(f'El post {post_id} no existe')
        abort(404)
    # Crea un formulario inicializando los campos con los valores del post
    form = PostForm(obj=post)
    if form.validate_on_submit():
        # Actualiza los campos del post existente
        post.title = form.title.data
        post.content = form.content.data        
        post.save()
        logger.info(f'Actualizando post {post_id}')#este logger me muestra el modulo completo
        return redirect(url_for('admin.list_posts'))
    return render_template("admin/post_form.html", form=form, post=post)