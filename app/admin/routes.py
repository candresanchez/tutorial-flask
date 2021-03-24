import logging

from flask import render_template #Renderiza una plantilla creada con jinja2
from flask import redirect #redirige al cliente a una pagina especifica
from flask import url_for #crea un url a partir del nombre de la función que contiene el decorador route

from flask_login import current_user, login_required #Implementa el Login de usuarios

from app.models import Post
from . import admin_bp
from .forms import PostForm

loggeer = logging.getLogger(__name__)#creo un logger para este modulo

#Crea o Modifica una entrada en el Blog
@admin_bp.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None}) #crea un nuevo post
@admin_bp.route("/admin/post/<int:post_id>", methods=['GET', 'POST']) #modifica un post ya existente
@login_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data        
        content = form.content.data
        loggeer.info('Creando un post del blog')#este logger me muestra el modulo completo

        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()        

        return redirect(url_for('public.index'))
    return render_template("admin/post_form.html", form=form)