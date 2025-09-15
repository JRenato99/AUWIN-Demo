from functools import lru_cache

@lru_cache(maxsize=1)

def get_topologia():
    return generar_datos_red()

def generar_datos_red():
    datos = {
        'id': 'RED-WIN-LIMA',
        'nombre': 'Red WIN Lima',
        'tipo': 'RAIZ',
        'children': []
    }
    
    # Generar OLTs (3)
    for olt_id in range(1, 2): # 1 OLT
        olt = {
            'id': f'OLT-{olt_id}',
            'nombre': f'OLT {olt_id}',
            'tipo': 'OLT',
            'children': []
        }
        
        odf_id = 1
        splitter_id = 1
        cto_id = 0
        
        # Generar SLOTs (16 por OLT)
        for slot_id in range(1, 5): # 2 SLOTS
            slot = {
                'id': f'OLT-{olt_id}-SLOT-{slot_id}',
                'nombre': f'SLOT {slot_id}',
                'tipo': 'SLOT',
                'children': []
            }
            num_port = 0
            # Generar PORTS (16 por SLOT)
            for port_id in range(1, 17):
                port = {
                    'id': f'OLT-{olt_id}-SLOT-{slot_id}-PORT-{port_id}',
                    'nombre': f'PORT {port_id}',
                    'tipo': 'PORT',
                    'children': []
                }
                
                # Generar Splitter ODF (1 por puerto)
                splitter_odf = {
                    'id': f'OLT-{olt_id}-SLOT-{slot_id}-PORT-{port_id}-SPLITTER',
                    'nombre': f'Splitter ODF {port_id}',
                    'tipo': 'SPLITTER_ODF',
                    'children': []
                }
                if num_port >= 48:
                    odf_id +=1
                    num_port = 0    

                num_port +=1
                
                # Generar ODF (48 SplitterODF se concentran en 1 ODF)
                odf = {
                    'id': f'OLT-{olt_id}-SLOT-{slot_id}-PORT-{port_id}-ODF',
                    'nombre': f'ODF {odf_id}',
                    'tipo': 'ODF',
                    'children': []
                }
                
                # Generar CORE (96 fibras por ODF)
                core = {
                    'id': f'OLT-{olt_id}-SLOT-{slot_id}-PORT-{port_id}-CORE',
                    'nombre': f'CABLE CORE {odf_id}',
                    'tipo': 'CORE',
                    'children': []
                }
                
                # Generar Mufa Distribución (1 por core)
                mufa_dist = {
                    'id': f'OLT-{olt_id}-SLOT-{slot_id}-PORT-{port_id}-MUFADIST',
                    'nombre': f'Mufa Distribución {odf_id}',
                    'tipo': 'MUFA_DIST',
                    'children': []
                }
                
                # Generar Mufa PortaSplitter (4 por mufa distribución)
                for mufa_ps_id in range(1, 5):
                    mufa_ps = {
                        'id': f'OLT-{olt_id}-SLOT-{slot_id}-PORT-{port_id}-MUFADIST-MUFAPS-{mufa_ps_id}',
                        'nombre': f'Mufa PortaSplitter {mufa_ps_id}',
                        'tipo': 'MUFA_PS',
                        'children': []
                    }
                    
                    # Generar Splitter (4 por mufa portasplitter)
                    for split in range(1, 5):
                        splitter = {
                            'id': f'OLT-{olt_id}-SLOT-{slot_id}-PORT-{port_id}-MUFADIST-MUFAPS-{mufa_ps_id}-SPLITTER-{splitter_id}',
                            'nombre': f'Splitter {splitter_id }',
                            'tipo': 'SPLITTER',
                            'children': []
                        }

                        cto = {
                            'id': f'OLT-{olt_id}-SLOT-{slot_id}-PORT-{port_id}-MUFADIST-MUFAPS-{mufa_ps_id}-SPLITTER-{splitter_id}-CTO-{cto_id+1}',
                            'nombre': f'CTO {cto_id+1}',
                            'tipo': 'CTO',
                            'children': [
                                {                                        
                                    'id': f'OLT-{olt_id}-SLOT-{slot_id}-PORT-{port_id}-MUFADIST-MUFAPS-{mufa_ps_id}-SPLITTER-{splitter_id}-CTO-{cto_id+2}',
                                    'nombre': f'CTO {cto_id+2}',
                                    "tipo": "CTO",
                                    "children": [
                                        {
                                            'id': f'OLT-{olt_id}-SLOT-{slot_id}-PORT-{port_id}-MUFADIST-MUFAPS-{mufa_ps_id}-SPLITTER-{splitter_id}-CTO-{cto_id+3}',
                                            'nombre': f'CTO {cto_id+3}',
                                            "tipo": "CTO",
                                            "children": [
                                                {
                                                    'id': f'OLT-{olt_id}-SLOT-{slot_id}-PORT-{port_id}-MUFADIST-MUFAPS-{mufa_ps_id}-SPLITTER-{splitter_id}-CTO-{cto_id+4}',
                                                    'nombre': f'CTO {cto_id+4}',
                                                    "tipo": "CTO",
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                        splitter_id = splitter_id + 1
                        cto_id = cto_id + 4
                        splitter['children'].append(cto)
                        
                        mufa_ps['children'].append(splitter)
                    
                    mufa_dist['children'].append(mufa_ps)
                    
                
                core['children'].append(mufa_dist)
                odf['children'].append(core)

                
                splitter_odf['children'].append(odf)

                port['children'].append(splitter_odf)
                slot['children'].append(port)
            
            olt['children'].append(slot)
        
        datos['children'].append(olt)
    
    return datos