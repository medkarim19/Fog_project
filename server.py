import asyncio
import websockets
import numpy as np
from PIL import Image
import base64
import io
import jwt
import ssl
from config import SECRET_KEY
import matplotlib.pyplot as plt  # Pour afficher l'image

# Charger et diviser l'image en parties
def split_image(image_path, n_parts):
    image = Image.open(image_path).convert('RGB')
    width, height = image.size
    part_height = height // n_parts
    parts = []

    for i in range(n_parts):
        left = 0
        top = i * part_height
        right = width
        bottom = (i + 1) * part_height if i < n_parts - 1 else height
        part = image.crop((left, top, right, bottom))
        parts.append(part)

    return parts

# Encoder une partie de l'image en base64
def encode_image(image):
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# Décoder la matrice reçue
def decode_matrix(data, part_height, width):
    matrix_bytes = base64.b64decode(data)
    matrix = np.frombuffer(matrix_bytes, dtype=np.uint8)
    return matrix.reshape((part_height, width))

async def distribute_tasks(websocket, path):
    global task_count
    token = await websocket.recv()

    # Vérifiez le jeton JWT
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("Token validé")
    except jwt.ExpiredSignatureError:
        print("Token expiré")
        return
    except jwt.InvalidTokenError:
        print("Token invalide")
        return

    if task_count >= n_clients:
        await websocket.send("No more tasks available")
        return
    
    # Envoyer la partie de l'image au client
    part = parts[task_count]
    encoded_part = encode_image(part)
    part_height = part.height
    await websocket.send(encoded_part)
    task_count += 1

    # Recevoir la matrice en niveaux de gris
    data = await websocket.recv()
    matrix = decode_matrix(data, part_height, part.width)
    results.append(matrix)
    
    # Afficher la matrice reçue du client
    print(f"Grayscale matrix received from client {task_count}.")

    # Une fois toutes les tâches terminées, combinez les résultats
    if len(results) == n_clients:
        final_matrix = np.vstack(results)
        print("All parts received, combining results...")
        
        # Afficher l'image en niveaux de gris
        plt.imshow(final_matrix, cmap='gray')
        plt.axis('off')  # Masquer les axes pour une meilleure vue de l'image
        plt.show()  # Affiche l'image et bloque l'exécution jusqu'à la fermeture de la fenêtre
        print("Server process finished.")

async def main():
    global parts, results, n_clients, task_count
    image_path = r'image.jpg'
    n_clients = 2  # Nombre de clients (y compris votre propre machine)
    task_count = 0
    parts = split_image(image_path, n_clients)
    results = []

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    async with websockets.serve(distribute_tasks, "localhost", 5000, ssl=ssl_context):
        print("Server is running on wss://localhost:5000")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
