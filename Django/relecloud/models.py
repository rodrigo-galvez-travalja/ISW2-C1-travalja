from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

# Create your models here.
class Destination(models.Model):
    name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=50
    )
    description = models.TextField(
        max_length=2000,
        null= False,
        blank=False
    )
    slug = models.SlugField()
    # image = models.ImageField(
    #     upload_to='destinations/',
    #     null=True,
    #     blank=True,
    #     help_text="Imagen del destino"
    # )
    
    def __str__(self) -> str:
        return self.name
    
    def average_rating(self):
        """Calcula la valoración media de las reviews"""
        avg = self.destination_reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

class Cruise(models.Model):
    name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=50
    )
    description = models.TextField(
        max_length=2000,
        null= False,
        blank=False
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name='destinations',
        )
    def __str__(self) -> str:
        return self.name
    
    def average_rating(self):
        """Calcula la valoración media de las reviews"""
        avg = self.cruise_reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0
    
class InfoRequest(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    email = models.EmailField()
    notes = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.PROTECT
    )

class Purchase(models.Model):
    """Modelo para registrar las compras de usuarios"""
    PURCHASE_TYPE_CHOICES = [
        ('destination', 'Destination'),
        ('cruise', 'Cruise'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    purchase_type = models.CharField(max_length=20, choices=PURCHASE_TYPE_CHOICES)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True, related_name='purchases')
    cruise = models.ForeignKey(Cruise, on_delete=models.CASCADE, null=True, blank=True, related_name='purchases')
    purchase_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['user', 'destination'], ['user', 'cruise']]
    
    def __str__(self):
        if self.purchase_type == 'destination':
            return f"{self.user.username} - {self.destination.name}"
        return f"{self.user.username} - {self.cruise.name}"

class Review(models.Model):
    """Modelo para reviews de destinos y cruceros"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True, related_name='destination_reviews')
    cruise = models.ForeignKey(Cruise, on_delete=models.CASCADE, null=True, blank=True, related_name='cruise_reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    comment = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        if self.destination:
            return f"{self.user.username} - {self.destination.name} ({self.rating}★)"
        return f"{self.user.username} - {self.cruise.name} ({self.rating}★)"
    