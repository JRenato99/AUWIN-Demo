from flask import Blueprint, render_template, jsonify, send_from_directory
from app.models.topologia import get_topologia
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/red')
def obtener_datos_red():
    datos_red = get_topologia()
    return jsonify(datos_red)

# Ruta para debuggear archivos estáticos
@bp.route('/debug-static')
def debug_static():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app_dir = os.path.dirname(base_dir)  # Subir un nivel a la carpeta app
    static_dir = os.path.join(app_dir, 'static')
    
    files = []
    if os.path.exists(static_dir):
        files = os.listdir(static_dir)
    
    return jsonify({
        'static_directory': static_dir,
        'static_exists': os.path.exists(static_dir),
        'files': files,
        'current_working_dir': os.getcwd()
    })

# Ruta para servir archivos estáticos manualmente (si es necesario)
@bp.route('/manual-static/<path:filename>')
def manual_static(filename):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app_dir = os.path.dirname(base_dir)
    static_dir = os.path.join(app_dir, 'static')
    
    return send_from_directory(static_dir, filename)