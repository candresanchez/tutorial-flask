from os.path import abspath, dirname

# Define el directorio de la aplicación
BASE_DIR = dirname(dirname(abspath(__file__)))

#Define un parametro a nivel de aplicación para generar un token, protege contra ataques CSRF.
SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

# Configuración de la BD

# Entornos de App
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''