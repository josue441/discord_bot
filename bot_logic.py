import random, requests, difflib
from bs4 import BeautifulSoup

def gen_pass(pass_length):
    #elementos de la contraseña
    elements = "ABCDEFGHIJKLMNOPQRSTUVWXYZ+-/*!&$#?=@<>abcdefghijklmnopqrstuvwxyz"
    password = ""

    for i in range(pass_length):
        #se eligen los caracteres que estaran en la contraseña y los pasa a "password"
        password += random.choice(elements)

    return password

def imagenes_de_perros():    
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']

#funcion para solicitar imagenes de patos|
def get_duck():
    url = "https://random-d.uk/api/random"
    res = requests.get(url)
    data = res.json()
    return data["url"]

#link de los videos
videos = [
        "https://www.youtube.com/watch?v=QrAta9gqYNQ&t=25s",
        "https://www.youtube.com/watch?v=6_zxPQuK1PY",
        "https://www.youtube.com/watch?v=uBMW8QM_iSI"
]
#funcion  que elige 1 de los 3 videos
def videos_choice():
    return random.choice(videos)

def buscar_avion(avion):
    try:
        # Reemplazar espacios por guiones bajos
        enlace = f"https://wiki.warthunder.com/{avion}"

        # Verificar si el enlace es válido
        response = requests.get(enlace)
        if response.status_code == 404:
            return None  # Retorna None si el avión no existe

        return enlace  # Retorna el enlace si existe

    except Exception as e:
        return f"Error: {e}"
