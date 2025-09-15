from app.models.topologia import get_topologia  # Import absoluto

def encontrar_padre(nodo_actual, objetivo_id, padre_actual=None):
    #Busca el nodo padre de un nodo con un ID específico.
    if nodo_actual.get('id') == objetivo_id:
        return padre_actual
    for child in nodo_actual.get('children', []):
        resultado = encontrar_padre(child, objetivo_id, nodo_actual)
        if resultado:
            return resultado
    return None

def encontrar_nodo_por_id(nodo_actual, objetivo_id):
    #Busca un nodo en la estructura de la red por su ID
    if nodo_actual.get('id') == objetivo_id:
        return nodo_actual
    for child in nodo_actual.get('children', []):
        resultado = encontrar_nodo_por_id(child, objetivo_id)
        if resultado:
            return resultado
    return None

def es_hijo_directo(nodo_trabajo, nodo_seleccionado):
    if not nodo_trabajo or not nodo_seleccionado: 
        return False, None
        
    datos_completos = get_topologia()
    nodo_seleccionado_completo = encontrar_nodo_por_id(datos_completos, nodo_seleccionado['id'])
    
    if not nodo_seleccionado_completo: 
        return False, None
    
    if 'children' not in nodo_seleccionado_completo or not nodo_seleccionado_completo['children']:
        return False, nodo_seleccionado_completo
    
    for hijo_directo in nodo_seleccionado_completo['children']:
        if hijo_directo.get('id') == nodo_trabajo['id']:
            return True, nodo_seleccionado_completo
                
    return False, nodo_seleccionado_completo