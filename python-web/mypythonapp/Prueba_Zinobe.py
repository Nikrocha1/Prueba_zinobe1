
#!/usr/bin/env python
# coding: utf-8

# In[24]:
import os, sys
sys.path.append('/home/nikole/.ipython')

#se importan las librerias necesarias
import requests
import json 
import random
import pandas as pd
from hashlib import sha1
from time import time
import sqlite3
#from IPython.display import HTML, display_html, display

def regions_app(url, headers):
    #se realiza la consulta y se guardan en formato JSON	
    result = requests.request("GET", url, headers=headers).json()

    #se crea lista vacia para guardar las regiones existentes
    without_region =[]
    regions = []
    for item in result:
    	#al realizar el ciclo se encontro que se acumulaba un elemento vacio
    	#esto sucede porque Bouvet island (Noruega), Heard island and Mcdonald Island (Australia) 	  no tienen una region definida.
    	#por lo tanto, se les asignara 'N/A'
    	if item['region']=='':
        	item['region'] = 'N/A'
        	without_region.append(item)
    	#se llena la lista regions 
    	if item['region'] not in regions:
        	regions.append(item['region'])
    return regions, without_region

def country_data(regions, without_region):
    reg =[]
    city = [] 
    lang = []
    time_ejec = []
    df = pd.DataFrame(columns=('Region', 'City name', 'Language', 'Time(ms)'), index=None)

    for op in regions:
        #print(op)
        if isinstance(op, str):
            
            if op != 'N/A':
                t_i = time()
                url = "https://restcountries.eu/rest/v2/region/" + op
                countries = requests.request("GET", url).json()
                #print(countries)
                country_select = random.choice(countries)
                
                for lang_data in country_select['languages']:
                    language_name = sha1(lang_data['name'].encode('utf-8')).hexdigest()
                reg.append(op)
                city.append(country_select['name'])
                lang.append(language_name) 
                t_f = time()
                time_ejec.append(float("%.2f" % ((t_f-t_i)*1000)))
            elif op == 'N/A':
                t_i2 = time()
                country_select = random.choice(without_region)
                #bouvet island no tiene un idioma definido, por lo tanto se le asigna N/A
                if country_select['languages']== []:
                    country_select['languages'] = 'N/A'
                for lang_data in country_select['languages']:
                    language_name = sha1(lang_data.encode('utf-8')).hexdigest()
                reg.append(op)
                city.append(country_select['name'])
                lang.append(language_name)
                t_f2 = time()
                time_ejec.append(float("%.2f" % ((t_f2-t_i2)*1000)))
                df['Region'] = reg
                df['City name'] = city
                df['Language'] = lang
                df['Time(ms)'] = time_ejec
                time_max = df['Time(ms)'].max()
                time_min = df['Time(ms)'].min()
                time_total = df['Time(ms)'].sum().round(2)
                time_ave = df['Time(ms)'].mean().round(2)
                return df, time_max, time_min, time_total, time_ave
            else:
                print('No es una opcion valida')
        else:
            print('Tipo de dato no valido: {0}. Por favor, ingrese un valor de tipo String.'.format(type(op)))

def table_insert(table_data):
    conn = sqlite3.connect('Prueba_Z.db')
    #c = conn.cursor()
    table_data.to_sql(name='Tabla_Regiones', con=conn)
    #recuerde cambiar la direccion en la que se guarda, esto varia dependiendo de cada equipo.
    table_data.to_json(r'/home/nikole/Escritorio/data.json')
    
    

