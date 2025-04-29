import asyncio
import websockets
import json
import base64

async def test_websocket():
    uri = "ws://localhost:8000/ws/product/import/"
    
    # Lire le fichier Excel
    with open('test_products.xlsx', 'rb') as file:
        file_content = base64.b64encode(file.read()).decode('utf-8')
    
    # Préparer les données à envoyer
    data = {
        'file_content': file_content,
        'user_id': 1  # Remplacez par l'ID d'un utilisateur existant dans votre base de données
    }
    
    async with websockets.connect(uri) as websocket:
        # Envoyer les données
        await websocket.send(json.dumps(data))
        
        # Recevoir et afficher les réponses
        while True:
            try:
                response = await websocket.recv()
                print(f"Réponse reçue: {response}")
            except websockets.exceptions.ConnectionClosed:
                print("Connexion fermée")
                break

# Exécuter le test
asyncio.get_event_loop().run_until_complete(test_websocket()) 