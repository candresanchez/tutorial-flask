pip freeze: Lista todas las dependencias de nuestra aplicación
FLASK_RUN_PORT: configurar puerto diferernte al 5000 que tiene por defecto flask
FLASK_ENV="development"  Automaticamente activa el modo debud a desarrollo para que los cambios en el código
                         automáticamente reinicie el servidor.  Se deseo desactivarlo configuro FLASK_DEBUG=FALSE
flask run --port 6000: al ejecutar flask se configura el puerto
flask run --host 0.0.0.0 : aceptar peticiones de otros ordenadores de nuestra red

LANZAR SERVIDOR INTERNO QUE VIENE CON FLASK (SOLO DESARROLLO)
1. Indicar al servidor qué aplicación debe lanzar, configurando la variable de entorno FLASK_APP
2. Editar el archivo activate.  
   En Linux/Mac export FLASK_APP="run.py". Windows: set "FLASK_APP=run.py"
3. Ejecutar: 
    flask run o 
    python -m flask run