from flask import Blueprint

admin_bp = Blueprint('admin', __name__, template_folder='templates')

from . import routes #'.' significa el directorio raiz, para este caso es admin