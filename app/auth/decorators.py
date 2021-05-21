from functools import wraps
from flask import abort
from flask_login import current_user

#from werkzeug.exceptions import Unauthorized

# Comprueba si el objeto current_user tiene el atributo is_admin y su valor es True.
# Si es así, ejecuta la función f.  En caso contrario devuelve un error 401,
# no permitiendo la ejecución de f.
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        is_admin = getattr(current_user, 'is_admin', False)
        if not is_admin:
            abort(401)
            #raise Unauthorized() tambièn funciona con este 
        return f(*args, **kws)
    return decorated_function