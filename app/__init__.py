from flask import Flask  #Toda app Flask es una instancia WSGI de la clase Flask
from flask_login import LoginManager #Implementa el Login de usuarios
from pymongo import MongoClient #driver para MongoDb
from flask import render_template
import logging
from logging.handlers import SMTPHandler #Manejador de loggin por correo

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

    configure_logging(app)
    
    login_manager.init_app(app)#registra el login para toda la aplicación
    login_manager.login_view = "auth.login" #El usuario será redirigido a la página de login en lugar de ver el error 401 cuando intenta acceder a una vista protegida.

    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    # Personalizar controladores de errores
    register_error_handler(app)    

    return app

#Paginas de error personalizadas
def register_error_handler(app):
    
    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500
    
    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(401)
    def error_401_handler(e):
        return render_template('401.html'), 401

#Modificando la configuración del logger por defecto de Flask
def configure_logging(app) :
    # Eliminamos los posibles manejadores, si existen, del logger por defecto
    del app.logger.handlers[:]

    # Añadimos el logger por defecto a la lista de loggers
    loggers = [app.logger, ]
    handlers = []

    # Creamos un manejador para escribir los mensajes por consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter())

    # Código para Crear un manejador para escribir los mensajes en archivo
    #file_handler = logging.FileHandler('ARCHIVO_LOG')
    #file_handler.setFormatter(verbose_formatter())    
    #handlers.append(file_handler)

    # Configuro el handler de acuerdo al entorno configurado
    if (app.config['APP_ENV'] == app.config['APP_ENV_LOCAL']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_TESTING']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']) :
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)

        mail_handler = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            app.config['DONT_REPLY_FROM_EMAIL'], app.config['ADMINS'],
            '[Error] [{}] La aplicación falló'.format(app.config['APP_ENV']),
            (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),())        
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_handler_formatter())
        handlers.append(mail_handler)

    # Asociamos cada uno de los handlers a cada uno de los loggers
    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)
    
    # Código para la Creación un logger con un handler especifico para escribir en disco para un módulo especifico
    #l = logging.getLogger('app.public.routes')
    #file_handler = logging.FileHandler('ARCHIVO_LOG')
    #file_handler.setFormatter(verbose_formatter())
    #l.addHandler(file_handler)
    
    
    
# Formateador Detallado para nuestros mensajes logger

# Este formateador registra la fecha en que se escribe el mensaje, 
# el nivel de gravedad, el nombre del logger que lo escribe, l
# a función/método dónde se escribe, la línea de código y el propio texto del mensaje.
def verbose_formatter() :
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s\t [%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/ %m/ %Y %H:%M:%S'
    )


# Formateador para SMTPHandler
def mail_handler_formatter() :
    return logging.Formatter(
        '''
            Message type:   %(levelname)s
            Location:       %(pathname)s:%(lineno)d
            Module:         %(module)s
            Function:       %(funcName)s
            Time:           %(asctime)s.%(msecs)d
            Message:        %(message)s
        ''',
        datefmt='%d/%m/%Y %H:%M:%S'
    )
    