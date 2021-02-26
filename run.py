from flask import Flask  #Toda app Flask es una instancia WSGI de la clase Flask
from flask import render_template #Renderiza una plantilla creada con jinja2
from flask import request #contiene toda la información que el cliente envia al sevidor
from flask import redirect #redirige al cliente a una pagina especifica
from flask import url_for #crea un url a partir del nombre de la función que contiene el decorador route
from flask import abort

#importa la clase que maneja los formularios del archivo forms.py
from forms import SignupForm 
from forms import PostForm
from forms import LoginForm

from flask_login import LoginManager, current_user, login_user, logout_user, login_required #Implementa el Login de usuarios

from werkzeug.urls import url_parse #analiza una URL de una cadena

from pymongo import MongoClient #driver para MongoDb

app = Flask(__name__) # Creamos una instancia y pasamos como argumento el nombre del mód o app
#Define un parametro a nivel de aplicación para generar un token, protege contra ataques CSRF.
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

login_manager = LoginManager(app) #registra el login para toda la aplicación
login_manager.login_view = "login" #El usuario será redirigido a la página de login en lugar de ver el error 401 cuando intenta acceder a una vista protegida.

#Conexión a MongoDb
client = MongoClient("mongodb://localhost:27017/")
db = client['miniblog']

from models import User, Post #importa las Clases Modelo del archivo models.py

@app.route('/')
def index():
    posts = Post.get_all() #obtiene una lista de Objetos Post   
    return render_template("index.html", posts=posts)

#ejemplo para usar slug
@app.route("/p/<string:slug>/")#muestra un post
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("post_view.html", post=post)

#Crea o Modifica una entrada en el Blog
@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None}) #crea un nuevo post
@app.route("/admin/post/<int:post_id>", methods=['GET', 'POST']) #modifica un post ya existente
@login_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data        
        content = form.content.data

        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()        

        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)

#registro de usuario nuevo en el Blog
@app.route("/signup/", methods=["GET", "POST"]) #la vista acepta peticiones POST y GET
def show_signup_form():
    if current_user.is_authenticated:#si ya esta autenticado lo envio a la pagina principal
        return redirect(url_for('index'))
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
                next_page = url_for('index')
            return redirect(next_page)        
    return render_template("signup_form.html", form=form, error=error)

#Accede al usuario cuyo ID se encuentra almacenado en sesión. 
#Este callback toma como parametro un string con el ID del usuario que se encuentra en sesión
#y debe devolver el correspondiente objeto User o None si el ID no es válido
@login_manager.user_loader #callback que es llamado por el método user_loader del objeto login_manager
def load_user(user_id):    
    return User.get_by_id(user_id)

#Logueo de un usuario ya existene en el blog
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #objeto de flask_login que verifica si el usuario actual ya esta autenticado 
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data) #Objeto del archivo models.py                       
        if user is not None and user.check_password(form.password.data):#verificamos si existe un usuario con ese email y si el password coincide
            login_user(user, remember=form.remember_me.data)#funcion de flask_login que loguea un usuario
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

#Cerrar la sesión de un usuario registrado
@app.route('/logout')
def logout():
    logout_user()#funcio´n de flask_login para cerrar la sesión de un usuario    
    return redirect(url_for('index'))