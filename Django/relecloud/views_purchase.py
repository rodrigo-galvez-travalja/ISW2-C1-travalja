from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models

@login_required
def purchase_destination(request, pk):
    """Vista para comprar un destino"""
    destination = get_object_or_404(models.Destination, pk=pk)
    
    # Si ya existe una review, eliminarla para permitir una nueva
    models.Review.objects.filter(
        user=request.user,
        destination=destination
    ).delete()
    
    # Crear la compra (permitir compras múltiples)
    models.Purchase.objects.create(
        user=request.user,
        destination=destination,
        purchase_type='destination'
    )
    messages.success(request, f'¡Has comprado {destination.name} con éxito! Ahora puedes dejar una opinión.')
    
    return redirect('destination_detail', pk=pk)

@login_required
def purchase_cruise(request, pk):
    """Vista para comprar un crucero"""
    cruise = get_object_or_404(models.Cruise, pk=pk)
    
    # Si ya existe una review, eliminarla para permitir una nueva
    models.Review.objects.filter(
        user=request.user,
        cruise=cruise
    ).delete()
    
    # Crear la compra (permitir compras múltiples)
    models.Purchase.objects.create(
        user=request.user,
        cruise=cruise,
        purchase_type='cruise'
    )
    messages.success(request, f'¡Has comprado {cruise.name} con éxito! Ahora puedes dejar una opinión.')
    
    return redirect('cruise_detail', pk=pk)
