import sys
import json
import requests
import poke_validation as pv
from get_module import get_info
import random
from string import Template
import menu as o
import validador as v

#Genera el span para el html
def genera_span(lista):
    diccionario_es={
        "normal":"Normal", "fire":"Fuego", "flying":"Volador", "steel":"Acero",
        "water":"Agua", "electric":"Electrico", "grass":"Planta", "ice":"Hielo",
        "fighting":"Lucha", "poison":"Venenoso", "ground":"Tierra", "psychic":"Psiquico",
        "bug":"Bicho", "rock":"Roca", "ghost":"Fantasma", "dragon":"Dragon", "dark":"Siniestro",
        "fairy":"Hada","legendary":"Legendario"
    }

    span_str=""
    for item in lista:
        item_es = diccionario_es.get(item)

        span_str= span_str + f'<span class="label {item}">{item_es}</span>'

    return span_str

#Devuelve las caracteristicas de acuerdo a los requerimiento ingresado en a y b
def caracteristicas(tipos,a,b):
    lista_caracteristicas=[]
    lista_caracteristicas_nueva=[]
    i=len(tipos)
    contador=0

    while(contador<i):
        tipo_pokemon=tipos[contador]
        url_fortaleza_debilidades = f'https://pokeapi.co/api/v2/type/{tipo_pokemon}'
        data_fortaleza_debilidades=get_info(url_fortaleza_debilidades)
    
    
    
        for item in data_fortaleza_debilidades:
            base_caracteristicas = data_fortaleza_debilidades[a][b]
        
        
        for item in base_caracteristicas:
            lista_caracteristicas.append(item["name"])
            
        for item in lista_caracteristicas:
            if item not in lista_caracteristicas_nueva:
                lista_caracteristicas_nueva.append(item)

        contador+=1
        
    return lista_caracteristicas_nueva

def indicadores(indicador, dict_species):
    
    resultado = dict_species[f'is_{indicador}']
    return resultado

def get_species(id):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{id}/"
    return get_info(url)

def indicador(valor):
    
    return f'<span class="label normal">{valor}</span>'

#####################-----------------------------------########################


op = o.menu()
opcion = v.validador(op)
if opcion == "1":
    name = input("Introduzca el nombre del Pokémon a procesar: ")
    name = pv.validate(name.lower())
   
if opcion=="2":
    print('En otra oportunidad jugamos, te esperamos!!')
    exit()
   
url_base = f'https://pokeapi.co/api/v2/pokemon/{name}'
data_base=get_info(url_base)
pok_n = data_base["id"]
pok_nombre=name.capitalize()

dict_species = get_species(pok_n)
legendario = indicadores('legendary', dict_species)
mitico = indicadores('mythical', dict_species)
bebe = indicadores('baby', dict_species)

stats = data_base["stats"]
indicadores = []
for item in stats:
    indicadores.append(item["base_stat"])

pok_hp, pok_ataque, pok_defensa, pok_ataqueEspecial, pok_defensaEspecial, pok_velocidad = indicadores

pok_img=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{data_base["id"]}.png'



#Aqui se determina el parametro del pokemon anterior si existe
url_previa = f'https://pokeapi.co/api/v2/pokemon-species/{name}'
data_etapa_previa = get_info(url_previa)
pok_etapa_previa = data_etapa_previa['evolves_from_species']
if pok_etapa_previa is not None:
    pok_etapa_previa = pok_etapa_previa["name"]
else:
    pok_etapa_previa = ""

if pok_etapa_previa!= "":
    pok_etapa_previa = f'Etapa Previa: {pok_etapa_previa.capitalize()}'


#Se genera lista de tipos pokemon
tipos_lista = data_base["types"]
tipos = []
for item in tipos_lista:
    tipos.append(item["type"]["name"])


### Procesamiento del comentario sobre el pokemon en español

comentarios = data_etapa_previa["flavor_text_entries"]
filtro = [item["flavor_text"].replace("\n"," ") for item in comentarios if item["language"]["name"] == 'es']
pok_comentario = random.choice(filtro)
pok_tipo=pok_comentario



#Se genera la caracterisca de acuerdo al tipo de habilidad o debilidad
lista_efectivo=caracteristicas(tipos,"damage_relations","double_damage_to")
lista_debilidades=caracteristicas(tipos,"damage_relations","double_damage_from")
lista_resistente=caracteristicas(tipos,"damage_relations","half_damage_from")
lista_pocoEficaz=caracteristicas(tipos,"damage_relations","half_damage_to")
lista_inmune= caracteristicas(tipos,"damage_relations","no_damage_from")
lista_ineficaz= caracteristicas(tipos,"damage_relations","no_damage_to")



#se traspasan los valores a las variables del html
span_tipo = genera_span(tipos)
span_superEfectivo = genera_span(lista_efectivo)
span_debiContra = genera_span(lista_debilidades)
span_resistenteContra=genera_span(lista_resistente)
span_pocoEficaz=genera_span(lista_pocoEficaz)
span_inmuneContra=genera_span(lista_inmune)
span_ineficazContra=genera_span(lista_ineficaz)

#Template
with open('base.html','r',encoding="utf-8") as infile:
    entrada=infile.read()


document_template= Template(entrada)
document_template_new = document_template.substitute(
    pok_n=pok_n,
    pok_nombre=pok_nombre,
    pok_img=pok_img,
    pok_etapa_previa=pok_etapa_previa,
    pok_hp=pok_hp,
    pok_ataque=pok_ataque,
    pok_defensa=pok_defensa,
    pok_ataqueEspecial=pok_ataqueEspecial,
    pok_defensaEspecial=pok_defensaEspecial,
    pok_velocidad=pok_velocidad,
    span_tipo=span_tipo,
    pok_tipo=pok_tipo,
    span_superEfectivo=span_superEfectivo,
    span_debiContra=span_debiContra,
    span_resistenteContra=span_resistenteContra,
    span_pocoEficaz=span_pocoEficaz,
    span_inmuneContra=span_inmuneContra,
    span_ineficazContra=span_ineficazContra,
    span_legendario = indicador('Legendario') if legendario == True else '',
    span_mitico = indicador('Mítico') if mitico == True else '', 
    span_bebe = indicador('Bebé') if bebe == True else ''
    
    
     )
     

with open('salida.html','w',encoding="utf-8") as outfile:
    outfile.write(document_template_new)





