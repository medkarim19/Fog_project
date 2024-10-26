import asyncio
import websockets
import numpy as np
from PIL import Image
import base64
import io
import jwt
import ssl  # Importer le module SSL
from config import SECRET_KEY  # Importer la clé secrète depuis config.py

# Fonction pour générer un jeton JWT
def generate_jwt_token(client_id):
    payload = {"client_id": client_id}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Décodez l'image base64
def decode_image(encoded_image):
    image_data = base64.b64decode(encoded_image)
    return Image.open(io.BytesIO(image_data))

# Calculer la matrice en niveaux de gris
def compute_grayscale_matrix(image):
    grayscale_image = image.convert('L')
    return np.array(grayscale_image)

# Encodez la matrice pour l'envoi via WebSocket
def encode_matrix(matrix):
    matrix_bytes = matrix.tobytes()
    return base64.b64encode(matrix_bytes).decode('utf-8')

async def process_image_part():
    uri = "wss://localhost:5000"  # Utilisez wss:// pour la connexion sécurisée
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False  # Ne pas vérifier le nom d'hôte
    ssl_context.verify_mode = ssl.CERT_NONE  # Ignorer la vérification du certificat

    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        print("Connected to server")

        # Générer et envoyer le jeton
        token = generate_jwt_token("client_123")
        await websocket.send(token)
        print("Token sent to server")

        # Recevoir l'image depuis le serveur
        encoded_image = await websocket.recv()
        image = decode_image(encoded_image)
        print("Received image part")

        # Calculer la matrice en niveaux de gris
        grayscale_matrix = compute_grayscale_matrix(image)
        encoded_matrix = encode_matrix(grayscale_matrix)
        await websocket.send(encoded_matrix)
        print("Grayscale matrix sent to server")

if __name__ == "__main__":
    asyncio.run(process_image_part())
