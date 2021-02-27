from flask import render_template #Renderiza una plantilla creada con jinja2
from flask import redirect #redirige al cliente a una pagina especifica
from flask import url_for #crea un url a partir del nombre de la función que contiene el decorador route
from flask import request #contiene toda la información que el cliente envia al sevidor

from flask_login import current_user, login_user, logout_user #Implementa el Login de usuarios
from werkzeug.urls import url_parse #analiza una URL de una cadena

from app import login_manager
from . import auth_bp
from .forms import SignupForm, LoginForm
from .models import User

#registro de usuario nuevo en el Blog
@auth_bp.route("/signup/", methods=["GET", "POST"]) #la vista acepta peticiones POST y GET
def show_signup_form():
    if current_user.is_authenticated:#si ya esta autenticado lo envio a la pagina principal
        return redirect(url_for('public.index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        #Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email)
            user.set_password(password)
            user_id = user.save()
            user.id = user_id            
            # Dejamos el usuario logueado           
            login_user(user, remember=True)
            next_page = request.args.get('next', None)        
            if not next_page or url_parse(next_page).netloc !='':
                next_page = url_for('public.index')
            return redirect(next_page)        
    return render_template("auth/signup_form.html", form=form, error=error)


#Logueo de un usuario ya existene en el blog
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #objeto de flask_login que verifica si el usuario actual ya esta autenticado 
        return redirect(url_for('public.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data) #Objeto del archivo models.py                       
        if user is not None and user.check_password(form.password.data):#verificamos si existe un usuario con ese email y si el password coincide
            login_user(user, remember=form.remember_me.data)#funcion de flask_login que loguea un usuario
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template('auth/login_form.html', form=form)


#Cerrar la sesión de un usuario registrado
@auth_bp.route('/logout')
def logout():
    logout_user()#función de flask_login para cerrar la sesión de un usuario    
    return redirect(url_for('public.index'))


#Accede al usuario cuyo ID se encuentra almacenado en sesión. 
#Este callback toma como parametro un string con el ID del usuario que se encuentra en sesión
#y debe devolver el correspondiente objeto User o None si el ID no es válido
@login_manager.user_loader #callback que es llamado por el método user_loader del objeto login_manager
def load_user(user_id):    
    return User.get_by_id(user_id)