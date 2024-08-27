import tweepy
import time
import requests
import os
import random
from prodiapy import Prodia
from io import BytesIO
from keep_alive import keep_alive
keep_alive()

# Credenciales de la API de Twitter
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

# Autenticación en Twitter
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
apiv1 = tweepy.API(auth)
client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

# Autenticación en Prodia
prodia = Prodia(
    api_key=os.environ.get('API_KEY')
)

# Lista de 24 prompts
prompts = [
    "A dense forest at dawn.",
    "A calm lake surrounded by mountains.",
    "A misty meadow with wildflowers.",
    "A rocky coastline at sunset.",
    "A river flowing through a canyon.",
    "A solitary tree in an open field.",
    "Snow-covered mountains under a clear sky.",
    "A sandy beach with gentle waves.",
    "A waterfall in a tropical jungle.",
    "A winding path through autumn woods.",
    "A grassy hill under a cloudy sky.",
    "A serene desert landscape at twilight.",
    "A lush valley with a winding river.",
    "A peaceful lakeshore at sunrise.",
    "A vibrant coral reef in clear waters.",
    "A mountain peak with a view of the horizon.",
    "A dense jungle with rays of sunlight filtering through.",
    "A quiet forest path covered in fallen leaves.",
    "A frozen tundra under a starry night sky.",
    "A wildflower meadow at golden hour.",
    "A tranquil pond with water lilies.",
    "A rugged mountain landscape with a stormy sky.",
    "A tropical island with crystal-clear waters.",
    "A forest clearing with a view of distant mountains.",
    "A sun-drenched savannah with acacia trees.",
    "A foggy harbor with anchored boats.",
    "A lush rainforest with a flowing river.",
    "A snow-covered forest under the northern lights.",
    "A mountain stream cascading over rocks.",
    "A lavender field in full bloom at sunset.",
    "A rocky desert with cacti and distant mesas.",
    "A calm fjord surrounded by steep cliffs.",
    "A coastal town with colorful houses on a hillside.",
    "A dense pine forest in the middle of winter.",
    "A hot spring surrounded by snowy peaks.",
    "A vast prairie under a wide blue sky.",
    "A river delta with winding waterways.",
    "A mist-covered mountain range at dawn.",
    "A sunflower field under a bright blue sky.",
    "A secluded beach with towering palm trees.",
    "A lush garden with blooming flowers and a fountain.",
    "A quiet mountain village nestled in a valley.",
    "A crystal-clear lake reflecting the surrounding forest.",
    "A dark forest under a full moon.",
    "A rugged coastline with crashing waves.",
    "A serene pasture with grazing sheep.",
    "A hot desert with rolling sand dunes.",
    "A highland moor with heather in bloom.",
    "A peaceful riverbank lined with willows.",
    "A vibrant autumn forest with falling leaves.",
    "A remote cabin in a snowy wilderness.",
    "A foggy morning in a mountain valley.",
    "A secluded glade with a small pond.",
    "A mountain ridge with sweeping views.",
    "A tranquil bay with still waters.",
    "A field of poppies under a stormy sky.",
    "A misty forest with towering redwoods.",
    "A lush vineyard in the rolling hills.",
    "A frozen lake surrounded by snowy trees.",
    "A tropical rainforest with exotic birds.",
    "A sunlit forest with dappled shadows.",
    "A winding river through a vast canyon.",
    "A serene lagoon with clear turquoise waters.",
    "A stormy ocean with towering waves.",
    "A peaceful countryside with rolling hills.",
    "A cherry blossom orchard in full bloom.",
    "A rocky mountain pass with distant peaks.",
    "A tranquil meadow at sunrise.",
    "A fog-covered field at dawn.",
    "A sunflower field swaying in the wind.",
    "A serene alpine lake with crystal-clear water.",
    "A rugged coastline with dramatic cliffs.",
    "A wildflower-covered hillside at sunset.",
    "A lush forest with a hidden waterfall.",
    "A remote beach with crashing waves.",
    "A peaceful river winding through the countryside.",
    "A snow-capped mountain range under a bright blue sky.",
    "A calm lake with a reflection of the mountains.",
    "A vibrant coral reef teeming with life.",
    "A foggy forest with tall pine trees.",
    "A vast desert landscape with distant mountains.",
    "A secluded mountain lake with crystal-clear water.",
    "A peaceful meadow filled with daisies.",
    "A dark, mysterious forest with thick underbrush.",
    "A tranquil beach with soft, white sand.",
    "A field of lavender under a cloudy sky.",
    "A dense forest with a winding stream.",
    "A remote island with rugged cliffs.",
    "A snow-covered landscape under a clear starry sky.",
    "A quiet bay with gently lapping waves.",
    "A vast expanse of rolling green hills.",
    "A colorful sunset over a calm ocean.",
    "A serene forest with rays of sunlight filtering through.",
    "A tranquil river surrounded by lush vegetation.",
    "A rugged mountain landscape with a view of the valley below.",
    "A hidden waterfall deep in the forest.",
    "A peaceful pond with ducks swimming.",
    "A stormy sky over a windswept plain.",
    "A dense fog rolling over the mountains.",
    "A vibrant spring meadow with blooming flowers."
]


# Función para generar la imagen con un prompt cíclico
def generate_image(index):
    prompt = random.choice(prompts)  # Selección aleatoria de un prompt
    job = prodia.sd.generate(prompt=prompt)
    result = prodia.wait(job)
    return result.image_url

# Función para descargar la imagen desde la URL generada
def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        return BytesIO(response.content)  # Devuelve la imagen como un objeto de archivo en memoria
    else:
        return None

# Función para subir la imagen a Twitter sin comentario
def upload_image_to_twitter(image_file):
    # Primero, sube el archivo
    media_response = apiv1.media_upload(filename="image.jpg", file=image_file)
    media_id = media_response.media_id

    # Luego, tuitea con el ID del archivo
    client.create_tweet(text='', media_ids=[media_id])

# Función principal para manejar la generación y subida cada hora
def post_images_every_hour():
    index = 0
    while True:
        image_url = generate_image(index)
        image_file = download_image(image_url)
        if image_file:
            upload_image_to_twitter(image_file)
            print(f"Posted image {index + 1}")
        index += 1
        time.sleep(3600)  # Espera 1 hora (3600 segundos)

# Inicia el proceso de publicación
post_images_every_hour()
