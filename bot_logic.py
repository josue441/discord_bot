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

#funcion para solicitar imagenes de patos
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
        # Página principal de los aviones
        url = "https://wiki.warthunder.com/aviation"
        response = requests.get(url)

        # Verificar si la solicitud fue exitosa
        if response.status_code != 200:
            return f"Error: No se pudo acceder a la página. Código {response.status_code}"

        # Analizar el HTML de la página
        bs = BeautifulSoup(response.text, "lxml")

        # Extraer los enlaces de los aviones
        temp = bs.find_all("a", "wt-tree_item-link")
        links = [post.get("href") for post in temp]
        nombres = [link.split("/")[-1] for link in links]  # Extraer solo el nombre del avión

        # Buscar el nombre más parecido al ingresado por el usuario
        coincidencias = difflib.get_close_matches(avion.lower(), nombres, n=1, cutoff=0.6)
        if coincidencias:
            nombre_avion = coincidencias[0]
            return f"https://wiki.warthunder.com{links[nombres.index(nombre_avion)]}"  # Retorna el enlace completo
        else:
            return "No se encontró un avión similar."

    except Exception as e:
        return f"Error: {e}"
