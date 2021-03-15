from flask import Flask  #Toda app Flask es una instancia WSGI de la clase Flask
from flask_login import LoginManager #Implementa el Login de usuarios
from pymongo import MongoClient #driver para MongoDb

login_manager = LoginManager() #crea un objeto
#Conexión a MongoDb
client = MongoClient("mongodb://localhost:27017/")
db = client['miniblog']

def create_app(settings_module):
    app = Flask(__name__, instance_relative_config=True) # Creamos una instancia y pasamos como argumento el nombre del mód o app
    # Carga los parámetros de configuración especificado por la variable de entorno APP
    app.config.from_object(settings_module)    
    # Carga la configuración del directorio instance
    if app.config.get('TESTING', False) :
        app.config.from_pyfile('config-testing.py',silent=True)        
    else:
        app.config.from_pyfile('config.py', silent=True)        

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

    