# Script para agregar datos de prueba de compras y reviews
# Ejecutar desde Django shell: python manage.py shell < add_sample_reviews.py

from django.contrib.auth.models import User
from relecloud.models import Destination, Cruise, Purchase, Review

# Crear un usuario de prueba si no existe
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
    print(f"✓ Usuario creado: {user.username}")
else:
    print(f"✓ Usuario existente: {user.username}")

# Obtener algunos destinos y cruceros
destinations = Destination.objects.all()[:3]
cruises = Cruise.objects.all()[:2]

# Crear compras de prueba
print("\n--- Creando compras de prueba ---")
for destination in destinations:
    purchase, created = Purchase.objects.get_or_create(
        user=user,
        destination=destination,
        defaults={'purchase_type': 'destination'}
    )
    if created:
        print(f"✓ Compra creada: {destination.name}")

for cruise in cruises:
    purchase, created = Purchase.objects.get_or_create(
        user=user,
        cruise=cruise,
        defaults={'purchase_type': 'cruise'}
    )
    if created:
        print(f"✓ Compra creada: {cruise.name}")

# Crear reviews de prueba
print("\n--- Creando reviews de prueba ---")
reviews_data = [
    {'rating': 5, 'comment': 'Amazing destination! Highly recommended.'},
    {'rating': 4, 'comment': 'Great experience, would visit again.'},
    {'rating': 5, 'comment': 'Absolutely stunning views and great service.'},
]

for i, destination in enumerate(destinations):
    if i < len(reviews_data):
        review, created = Review.objects.get_or_create(
            user=user,
            destination=destination,
            defaults=reviews_data[i]
        )
        if created:
            print(f"✓ Review creada para: {destination.name} ({review.rating}★)")

cruise_reviews_data = [
    {'rating': 5, 'comment': 'Perfect cruise experience! Exceeded expectations.'},
    {'rating': 4, 'comment': 'Very enjoyable cruise with excellent staff.'},
]

for i, cruise in enumerate(cruises):
    if i < len(cruise_reviews_data):
        review, created = Review.objects.get_or_create(
            user=user,
            cruise=cruise,
            defaults=cruise_reviews_data[i]
        )
        if created:
            print(f"✓ Review creada para: {cruise.name} ({review.rating}★)")

print("\n✅ Datos de prueba agregados exitosamente!")
print(f"\nPara probar el sistema:")
print(f"1. Ve a http://127.0.0.1:8000/admin")
print(f"2. Inicia sesión con: username='testuser', password='testpass123'")
print(f"3. Navega a los destinos y cruceros para ver las reviews")
