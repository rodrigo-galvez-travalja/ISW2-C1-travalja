from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Destination, Cruise, InfoRequest, Purchase, Review


class DestinationModelTest(TestCase):
    """Tests para el modelo Destination"""
    
    def setUp(self):
        self.destination = Destination.objects.create(
            name="París",
            description="La ciudad del amor",
            slug="paris"
        )
    
    def test_destination_creation(self):
        """Verifica que se cree correctamente un destino"""
        self.assertEqual(self.destination.name, "París")
        self.assertEqual(str(self.destination), "París")
    
    def test_average_rating_without_reviews(self):
        """Verifica que la valoración promedio sin reviews sea 0"""
        self.assertEqual(self.destination.average_rating(), 0)
    
    def test_average_rating_with_reviews(self):
        """Verifica el cálculo correcto de valoración promedio"""
        user = User.objects.create_user(username="testuser", password="12345")
        Review.objects.create(user=user, destination=self.destination, rating=4)
        Review.objects.create(user=user, destination=self.destination, rating=5)
        self.assertGreater(self.destination.average_rating(), 0)


class CruiseModelTest(TestCase):
    """Tests para el modelo Cruise"""
    
    def setUp(self):
        self.cruise = Cruise.objects.create(
            name="Crucero Mediterráneo",
            description="Un viaje inolvidable"
        )
        self.destination = Destination.objects.create(
            name="Barcelona",
            description="Ciudad costera",
            slug="barcelona"
        )
        self.cruise.destinations.add(self.destination)
    
    def test_cruise_creation(self):
        """Verifica que se cree correctamente un crucero"""
        self.assertEqual(self.cruise.name, "Crucero Mediterráneo")
        self.assertEqual(str(self.cruise), "Crucero Mediterráneo")
    
    def test_cruise_destinations(self):
        """Verifica la relación many-to-many con destinos"""
        self.assertEqual(self.cruise.destinations.count(), 1)
        self.assertIn(self.destination, self.cruise.destinations.all())


class InfoRequestModelTest(TestCase):
    """Tests para el modelo InfoRequest"""
    
    def setUp(self):
        self.cruise = Cruise.objects.create(
            name="Crucero del Caribe",
            description="Paraíso tropical"
        )
    
    def test_info_request_creation(self):
        """Verifica que se cree correctamente una solicitud de información"""
        info_request = InfoRequest.objects.create(
            name="Juan Pérez",
            email="juan@example.com",
            notes="Quisiera más información",
            cruise=self.cruise
        )
        self.assertEqual(info_request.name, "Juan Pérez")
        self.assertEqual(info_request.email, "juan@example.com")


class ViewsTest(TestCase):
    """Tests para las vistas principales"""
    
    def setUp(self):
        self.client = Client()
        self.destination = Destination.objects.create(
            name="Roma",
            description="La ciudad eterna",
            slug="roma"
        )
        self.cruise = Cruise.objects.create(
            name="Crucero Adriático",
            description="Explora el Adriático"
        )
    
    def test_index_view(self):
        """Verifica que la página principal cargue correctamente"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_about_view(self):
        """Verifica que la página about cargue correctamente"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
    
    def test_destination_list_view(self):
        """Verifica que la lista de destinos cargue correctamente"""
        response = self.client.get(reverse('destination'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'destination.html')
        self.assertContains(response, "Roma")
    
    def test_destination_detail_view(self):
        """Verifica que el detalle de un destino cargue correctamente"""
        response = self.client.get(reverse('destination_detail', kwargs={'pk': self.destination.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'destination_detail.html')
        self.assertContains(response, "Roma")
    
    def test_cruise_detail_view(self):
        """Verifica que el detalle de un crucero cargue correctamente"""
        response = self.client.get(reverse('cruise_detail', kwargs={'pk': self.cruise.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cruise_detail.html')


class PurchaseModelTest(TestCase):
    """Tests para el modelo Purchase"""
    
    def setUp(self):
        self.user = User.objects.create_user(username="buyer", password="pass123")
        self.destination = Destination.objects.create(
            name="Tokio",
            description="Capital de Japón",
            slug="tokio"
        )
    
    def test_purchase_creation(self):
        """Verifica que se cree correctamente una compra"""
        purchase = Purchase.objects.create(
            user=self.user,
            purchase_type='destination',
            destination=self.destination
        )
        self.assertEqual(purchase.user, self.user)
        self.assertEqual(purchase.destination, self.destination)
        self.assertIsNotNone(purchase.purchase_date)


class ReviewModelTest(TestCase):
    """Tests para el modelo Review"""
    
    def setUp(self):
        self.user = User.objects.create_user(username="reviewer", password="pass456")
        self.destination = Destination.objects.create(
            name="Londres",
            description="La capital británica",
            slug="londres"
        )
    
    def test_review_creation(self):
        """Verifica que se cree correctamente una review"""
        review = Review.objects.create(
            user=self.user,
            destination=self.destination,
            rating=5,
            comment="¡Excelente destino!"
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "¡Excelente destino!")
        self.assertIn("5★", str(review))
