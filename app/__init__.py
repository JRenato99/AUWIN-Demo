from flask import Flask
import os
# Registrar blueprints (reutilizar modulos)
from .routes.main_routes import bp as main_bp
from .routes.nodo_routes import bp as nodo_bp
from .routes.diagnostico_routes import bp as diagnostico_bp

def create_app():
    # Obtener la ruta absoluta de la carpeta app
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Configurar las rutas correctamente
    template_path = os.path.join(base_dir, 'templates')
    static_path = os.path.join(base_dir, 'static')
    
    app = Flask(__name__, 
                template_folder=template_path,
                static_folder=static_path,
                static_url_path='/static')
        
    app.register_blueprint(main_bp)
    app.register_blueprint(nodo_bp)
    app.register_blueprint(diagnostico_bp)
    
    return app