# -*- coding: utf-8 -*-

import os, sys
import pandas as pd
sys.path.append('/home/nikole/python_zinobe/trunk/python-web/mypythonapp')

def application(environ, start_response): 
    import Prueba_Zinobe as p_z
    #url donde se extraen todas las caracteristicas de cada pais
    url = "https://restcountries-v1.p.rapidapi.com/all"

    #datos necesarios para poder realizar la consulta
    headers = {
    'x-rapidapi-host': "restcountries-v1.p.rapidapi.com",
    'x-rapidapi-key': "f16396a031msh378ea696111f464p1c6474jsn5a574454b661"
    }
    [regions, without_region] = p_z.regions_app(url, headers)
    [table_data, max_t, min_t, total_t, ave_t] = p_z.country_data(regions, without_region)
    #p_z.table_insert(table_data)

    output = bytes(table_data.to_html(justify='center'), encoding= 'utf-8')
 
    # Inicio una respuesta al navegador 
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')]) 
    # Retorno el contenido HTML 
    return [output]
