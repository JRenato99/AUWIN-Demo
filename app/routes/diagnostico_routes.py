from flask import Blueprint, jsonify
from app.models.topologia import get_topologia  # Import absoluto
from app.utils.topologia_utils import encontrar_padre, encontrar_nodo_por_id, es_hijo_directo  # Import absoluto

bp = Blueprint('diagnostico', __name__)

# Importar variables globales desde nodo_routes
from app.routes.nodo_routes import nodo_seleccionado, nodo_trabajo_info, nodo_padre_info

@bp.route('/api/generar-diagnostico', methods=['GET'])
def generar_diagnostico():
    
    def es_descendiente(nodo, posible_ancestro):
        if not nodo or not posible_ancestro:
            return False

        def buscar_ancestro(nodo_actual, objetivo_id):
            if nodo_actual.get('id') == objetivo_id:
                return True
            if 'children' in nodo_actual:
                for child in nodo_actual['children']:
                    if buscar_ancestro(child, objetivo_id):
                        return True
            return False

        return buscar_ancestro(posible_ancestro, nodo['id'])    

    diagnostico = {
        'tipo': 'Indeterminado',
        'mensaje': 'No se puede determinar la relación',
        'detalles': ''
    }
  
    if not nodo_seleccionado:
        diagnostico['mensaje'] = 'Falta información: seleccione un nodo y especifique dónde trabaja el técnico'

    elif not nodo_trabajo_info:
        hijos_directos = nodo_seleccionado.get('children', []) if nodo_seleccionado else []
        datos_completos = get_topologia()
        nodo_padre_info_local = encontrar_padre(datos_completos, nodo_seleccionado['id']) 
        nombres_hijos = ', '.join(hijo['nombre'] for hijo in hijos_directos)

        diagnostico = {
            'tipo': 'Falla',
            'mensaje': 'Tecnico no Detectado',
            'detalles': (
                f"1. Revisar en el punto: {nodo_seleccionado['nombre']}\n"
                f"2. Revisar el/los {len(hijos_directos)} Cable(s) hacia {nombres_hijos}\n"
                f"3. Revisar el punto: {nodo_padre_info_local['nombre']}\n"
            )
        }

    else:
        nodo_trabajo = nodo_trabajo_info.get('nodo_trabajo', {})
        nodo_infra = nodo_trabajo_info.get('nodo_infraestructura', {})
        
        es_directo, _ = es_hijo_directo(nodo_trabajo, nodo_seleccionado)

        if nodo_trabajo.get('id') == nodo_seleccionado.get('id'):
            diagnostico = {
                'tipo': 'exacto',
                'mensaje': 'El técnico está trabajando EXACTAMENTE en el punto seleccionado',
                'detalles': f"1. Revisar en el punto: {nodo_trabajo.get('nombre')} ({nodo_trabajo.get('id')})\n"
                            f"2. Revisar el Cableado entre el {nodo_infra.get('nombre')} ({nodo_infra.get('id')}) y el {nodo_padre_info.get('nombre')} ({nodo_padre_info.get('id')}) \n"
                            f"3. Revisar la salida del {nodo_padre_info.get('nombre')} ({nodo_padre_info.get('id')}) \n"
            }
            
        elif nodo_padre_info and nodo_trabajo.get('id') == nodo_padre_info.get('id'):
            diagnostico = {
                'tipo': 'padre',
                'mensaje': 'El técnico está trabajando en el nodo PADRE del punto seleccionado',
                'detalles': f"1. Revisar en el punto: {nodo_trabajo.get('nombre')} - ({nodo_trabajo.get('id')})\n"
                            f"2. Revisar en el Cableado entre el {nodo_trabajo.get('nombre')} ({nodo_trabajo.get('id')}) y el {nodo_infra.get('nombre')} ({nodo_infra.get('id')}) \n"                            
                            f"3. Revisar el punto {nodo_infra.get('nombre')} ({nodo_infra.get('id')} \n"
            }            
        
        elif es_directo: 
            diagnostico = {
                'tipo': 'hijo',
                'mensaje': 'El técnico está trabajando en un nodo HIJO del punto seleccionado',
                'detalles': f"1. Revisar el punto {nodo_trabajo.get('nombre')} ({nodo_trabajo.get('id')})\n"
                            f"2. Revisar en el Cableado entre el {nodo_trabajo.get('nombre')} ({nodo_trabajo.get('id')}) y el {nodo_infra.get('nombre')} ({nodo_infra.get('id')})\n"
                            f"3. Revisar el punto {nodo_infra.get('nombre')} ({nodo_infra.get('id')} \n"
                            f"4. Revisar el Cableado entre el {nodo_infra.get('nombre')} ({nodo_infra.get('id')}) y el {nodo_padre_info.get('nombre')} ({nodo_padre_info.get('id')}) \n"
                            f"5. Revisar la salida del {nodo_padre_info.get('nombre')} ({nodo_padre_info.get('id')}) \n"
            }

        elif es_descendiente(nodo_trabajo, nodo_seleccionado):
            diagnostico = {
                'tipo': 'misma_infra',
                'mensaje': 'El técnico está trabajando en un punto SIN RELACIÓN DIRECTA con el seleccionado',
                'detalles': f"1. Revisar en el punto: {nodo_infra.get('nombre')} ({nodo_infra.get('id')})\n"
                            f"2. Revisar el Cableado entre el {nodo_infra.get('nombre')} ({nodo_infra.get('id')}) y el {nodo_padre_info.get('nombre')} ({nodo_padre_info.get('id')}) \n"
                            f"3. Revisar la salida del {nodo_padre_info.get('nombre')} ({nodo_padre_info.get('id')}) \n"
            }

        else:
            diagnostico = {
                'tipo': 'sin_relacion',
                'mensaje': 'Avería sin intervencion del Técnico',
                'detalles': f"1. Revisar en el punto: {nodo_infra.get('nombre')} ({nodo_infra.get('id')})\n"
                            f"2. Revisar el Cableado entre el {nodo_infra.get('nombre')} ({nodo_infra.get('id')}) y el {nodo_padre_info.get('nombre')} ({nodo_padre_info.get('id')}) \n"
                            f"3. Revisar la salida del {nodo_padre_info.get('nombre')} ({nodo_padre_info.get('id')}) \n"
            }
    
    return jsonify(diagnostico)