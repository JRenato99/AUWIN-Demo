from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models.topologia import get_topologia  # Import absoluto
from app.utils.topologia_utils import encontrar_padre, encontrar_nodo_por_id  # Import absoluto

bp = Blueprint('nodo', __name__)

# Variables globales (en un caso real, considerar usar session o base de datos)
nodo_seleccionado = None
info_tecnicos = {}  
nodo_trabajo_info = None
nodo_padre_info = None

@bp.route('/api/nodo-seleccionado', methods=['POST'])
def guardar_nodo_seleccionado():
    global nodo_seleccionado, nodo_padre_info
    data = request.get_json()
    nodo_seleccionado = data

    datos_completos = get_topologia()
    nodo_padre_info = encontrar_padre(datos_completos, data['id']) 
    nodo_actual = encontrar_nodo_por_id(datos_completos, data['id'])
    hijos_directos = nodo_actual.get('children', []) if nodo_actual else [] 

    return jsonify({
        'status': 'success', 
        'nodo': nodo_seleccionado, 
        'nodo_padre': nodo_padre_info, 
        'nodo_hijos': hijos_directos
    })

@bp.route('/api/info-tecnico', methods=['POST'])
def guardar_info_tecnico():
    global info_tecnicos
    data = request.get_json()
    nodo_id = data['nodo']['id']
    info_tecnicos[nodo_id] = {
        'nodo': data['nodo'],
        'hayTecnico': data['hayTecnico'],
        'timestamp': data['timestamp'],
        'fecha_actualizacion': datetime.now().isoformat()
    }
    return jsonify({'status': 'success', 'info_tecnico': info_tecnicos[nodo_id]})

@bp.route('/api/nodo-trabajo', methods=['POST'])
def guardar_nodo_trabajo():
    global nodo_trabajo_info, nodo_seleccionado, nodo_padre_info
    data = request.get_json()
    nodo_trabajo_info = {
        'nodo_trabajo': data['nodo_trabajo'],
        'nodo_infraestructura': data['nodo_infraestructura'],
        'nodo_padre': nodo_padre_info,
        'timestamp': data['timestamp'],
        'fecha_actualizacion': datetime.now().isoformat()
    }
    return jsonify({'status': 'success', 'nodo_trabajo': nodo_padre_info})

@bp.route('/api/nodo-seleccionado', methods=['GET'])
def obtener_nodo_seleccionado():
    return jsonify({
        'nodo_seleccionado': nodo_seleccionado, 
        'nodo_padre': nodo_padre_info, 
        'info_tecnicos': info_tecnicos, 
        'nodo_trabajo': nodo_trabajo_info
    })

@bp.route('/api/reset', methods=['POST'])
def reset_estado():
    global nodo_seleccionado, nodo_trabajo_info, nodo_padre_info, info_tecnicos
    print(nodo_seleccionado)
    print("******************************************************************")
    print( nodo_trabajo_info)
    print("******************************************************************")
    print( nodo_padre_info)
    print("******************************************************************")
    print( info_tecnicos)
    nodo_seleccionado = nodo_trabajo_info = nodo_padre_info = None
    info_tecnicos = {}
    return jsonify({'status': 'reset'})