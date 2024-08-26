import tweepy
import time
import requests
from prodiapy import Prodia
from io import BytesIO

# Credenciales de la API de Twitter
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAJcBvgEAAAAA3LsruGyvQXRDXfLbyyuieON0rvM%3DuRA4K5nttUM4W0UnARtc5TRrqelHq2KtGHrh7UcpYajQ3ddM1w' 
consumer_key = 'CVdrBpgj87rQMzOgMWbLbAUgb'
consumer_secret = '0l9Xy5OvWPkucc4yl9GPRoDLLNGv15AxeHJi4fvng1wPLjWOH3'
access_token = '1826682670505480192-CITJTWvBL93bEs3AZnjtNIz0Ai4yWD'
access_token_secret = 'RWoDsUtOBbtt7ju0HdgR7uUc9pJRKhzAVZepZnJcX55HE'

# Autenticación en Twitter
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
apiv1 = tweepy.API(auth)
client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

# Autenticación en Prodia
prodia = Prodia(
    api_key="ab05637d-f6f9-4713-995f-52af812d1432"
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
    "A forest clearing with a view of distant mountains."
]

# Función para generar la imagen con un prompt cíclico
def generate_image(index):
    prompt = prompts[index % len(prompts)]  # Selección cíclica de prompts
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
