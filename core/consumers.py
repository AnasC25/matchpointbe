import json
import pandas as pd
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Equipment
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class ProductImportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            file_content = data.get('file_content')
            user_id = data.get('user_id')
            
            # Convertir le contenu en DataFrame
            df = pd.read_excel(pd.BytesIO(file_content.encode()))
            
            # Récupérer l'utilisateur
            user = await self.get_user(user_id)
            
            if not user:
                await self.send(text_data=json.dumps({
                    'status': 'error',
                    'message': 'Utilisateur non trouvé'
                }))
                return

            # Traiter les données et créer les produits
            success_count = 0
            error_count = 0
            errors = []

            for _, row in df.iterrows():
                try:
                    await self.create_product(row, user)
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append(str(e))

            await self.send(text_data=json.dumps({
                'status': 'success',
                'message': f'Import terminé: {success_count} succès, {error_count} erreurs',
                'errors': errors
            }))

        except Exception as e:
            await self.send(text_data=json.dumps({
                'status': 'error',
                'message': str(e)
            }))

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @database_sync_to_async
    def create_product(self, row, user):
        Equipment.objects.create(
            name=row.get('name', ''),
            description=row.get('description', ''),
            quantity=row.get('quantity', 1),
            available=row.get('available', True),
            brand=row.get('brand', ''),
            category=row.get('category', ''),
            price=row.get('price', 0),
            prix_barre=row.get('prix_barre'),
            stock=row.get('stock', 0),
            image_url=row.get('image_url'),
            vendeur=user
        ) 