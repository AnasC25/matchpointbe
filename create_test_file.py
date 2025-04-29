import pandas as pd

# Créer un DataFrame avec des données de test
data = {
    'name': ['Raquette Pro', 'Balle Tennis', 'Sac Sport'],
    'description': ['Raquette professionnelle', 'Balle de tennis standard', 'Sac de sport grande capacité'],
    'quantity': [1, 12, 1],
    'available': [True, True, True],
    'brand': ['Wilson', 'Dunlop', 'Nike'],
    'category': ['Raquettes', 'Accessoires', 'Sacs'],
    'price': [299.99, 24.99, 89.99],
    'prix_barre': [349.99, 29.99, 99.99],
    'stock': [10, 100, 20],
    'image_url': ['https://example.com/raquette.jpg', 'https://example.com/balle.jpg', 'https://example.com/sac.jpg']
}

df = pd.DataFrame(data)
df.to_excel('test_products.xlsx', index=False)
print("Fichier test_products.xlsx créé avec succès!") 