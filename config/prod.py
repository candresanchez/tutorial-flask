from .default import *

#Define un parametro a nivel de aplicación para generar un token, protege contra ataques CSRF.
SECRET_KEY = '5e04a4955d8878191923e86fe6a0dfb24edb226c87d6c7787f35ba4698afc86e95cae409aebd47f7'

APP_ENV = APP_ENV_PRODUCTION

# Ejemplo configuración URI para una bd
SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@host:port/db_name'