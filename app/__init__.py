from flask import Flask  #Toda app Flask es una instancia WSGI de la clase Flask
from flask_login import LoginManager #Implementa el Login de usuarios
from pymongo import MongoClient #driver para MongoDb

login_manager = LoginManager() #crea un objeto
#Conexión a MongoDb
client = MongoClient("mongodb://localhost:27017/")
db = client['miniblog']

def create_app():
    app = Flask(__name__) # Creamos una instancia y pasamos como argumento el nombre del mód o app

    #Define un parametro a nivel de aplicación para generar un token, protege contra ataques CSRF.
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

    login_manager.init_app(app)#registra el login para toda la aplicación
    login_manager.login_view = "auth.login" #El usuario será redirigido a la página de login en lugar de ver el error 401 cuando intenta acceder a una vista protegida.

    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    return app

    