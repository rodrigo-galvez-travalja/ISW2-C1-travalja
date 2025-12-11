from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .views_reviews import create_destination_review, create_cruise_review
from .views_purchase import purchase_destination, purchase_cruise

# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def destination(request):
    all_destinations = models.Destination.objects.annotate(
        avg_rating=Avg('destination_reviews__rating'),
        num_reviews=Count('destination_reviews')
    ).order_by('-avg_rating', '-num_reviews')
    return render(request,'destination.html',{'destinations':all_destinations})

class DestinationDetailView(generic.DetailView):
    model = models.Destination
    template_name = 'destination_detail.html'
    context_object_name = 'destination'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = self.get_object()
        
        # Obtener todas las reviews
        context['reviews'] = destination.destination_reviews.all()
        context['average_rating'] = destination.average_rating()
        context['total_reviews'] = destination.destination_reviews.count()
        
        # Verificar si el usuario ha comprado este destino
        if self.request.user.is_authenticated:
            context['has_purchased'] = models.Purchase.objects.filter(
                user=self.request.user,
                destination=destination
            ).exists()
            
            # Verificar si ya dejó una review
            context['user_review'] = models.Review.objects.filter(
                user=self.request.user,
                destination=destination
            ).first()
        else:
            context['has_purchased'] = False
            context['user_review'] = None
        
        return context

class CruiseDetailView(generic.DetailView):
    model = models.Cruise
    template_name = 'cruise_detail.html'
    context_object_name = 'cruise'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cruise = self.get_object()
        
        # Obtener todas las reviews
        context['reviews'] = cruise.cruise_reviews.all()
        context['average_rating'] = cruise.average_rating()
        context['total_reviews'] = cruise.cruise_reviews.count()
        
        # Verificar si el usuario ha comprado este crucero
        if self.request.user.is_authenticated:
            context['has_purchased'] = models.Purchase.objects.filter(
                user=self.request.user,
                cruise=cruise
            ).exists()
            
            # Verificar si ya dejó una review
            context['user_review'] = models.Review.objects.filter(
                user=self.request.user,
                cruise=cruise
            ).first()
        else:
            context['has_purchased'] = False
            context['user_review'] = None
        
        return context

class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = 'Thank you, %(name)s! We will email you when we have more information about %(cruise)s!'

    def form_valid(self, form):
        response = super().form_valid(form)
        
        info_request = self.object
        
        # --- Correo interno a la empresa ---
        subject = f"New information request for {info_request.cruise.name}"
        message = "\n".join([
            "A new information request has been submitted from the website.",
            "",
            f"Name: {info_request.name}",
            f"Email: {info_request.email}",
            f"Cruise: {info_request.cruise.name}",
            "",
            "Notes:",
            info_request.notes,
        ])
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        
        # --- Correo de confirmación para el usuario ---
        confirmation_subject = "We received your information request"
        confirmation_message = (
            f"Hi {info_request.name},\n\n"
            f"Thank you for your interest in our cruise \"{info_request.cruise.name}\".\n"
            "We have received your request and will contact you with more information soon.\n\n"
            "Best regards,\n"
            "ReleCloud Team"
        )
        
        send_mail(
            subject=confirmation_subject,
            message=confirmation_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[info_request.email],
            fail_silently=False,
        )
        
        return response