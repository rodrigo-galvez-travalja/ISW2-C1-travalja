from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models

@login_required
def create_destination_review(request, pk):
    """Vista para crear una review de un destino (solo una vez por compra)"""
    destination = get_object_or_404(models.Destination, pk=pk)
    
    # Verificar que el usuario ha comprado este destino
    has_purchased = models.Purchase.objects.filter(
        user=request.user,
        destination=destination
    ).exists()
    
    if not has_purchased:
        messages.error(request, 'Debes comprar este destino antes de dejar una opinión.')
        return redirect('destination_detail', pk=pk)
    
    # Verificar si ya dejó una review
    existing_review = models.Review.objects.filter(
        user=request.user,
        destination=destination
    ).exists()
    
    if existing_review:
        messages.error(request, 'Ya has valorado este destino. Cómpralo de nuevo para dejar otra opinión.')
        return redirect('destination_detail', pk=pk)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        # Crear review
        models.Review.objects.create(
            user=request.user,
            destination=destination,
            rating=rating,
            comment=comment
        )
        
        # Eliminar la compra para forzar recompra si quiere dejar otra review
        models.Purchase.objects.filter(
            user=request.user,
            destination=destination
        ).delete()
        
        messages.success(request, 'Review submitted successfully!')
        return redirect('destination_detail', pk=pk)
    
    return redirect('destination_detail', pk=pk)

@login_required
def create_cruise_review(request, pk):
    """Vista para crear una review de un crucero (solo una vez por compra)"""
    cruise = get_object_or_404(models.Cruise, pk=pk)
    
    # Verificar que el usuario ha comprado este crucero
    has_purchased = models.Purchase.objects.filter(
        user=request.user,
        cruise=cruise
    ).exists()
    
    if not has_purchased:
        messages.error(request, 'Debes comprar este crucero antes de dejar una opinión.')
        return redirect('cruise_detail', pk=pk)
    
    # Verificar si ya dejó una review
    existing_review = models.Review.objects.filter(
        user=request.user,
        cruise=cruise
    ).exists()
    
    if existing_review:
        messages.error(request, 'Ya has valorado este crucero. Cómpralo de nuevo para dejar otra opinión.')
        return redirect('cruise_detail', pk=pk)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        # Crear review
        models.Review.objects.create(
            user=request.user,
            cruise=cruise,
            rating=rating,
            comment=comment
        )
        
        # Eliminar la compra para forzar recompra si quiere dejar otra review
        models.Purchase.objects.filter(
            user=request.user,
            cruise=cruise
        ).delete()
        
        messages.success(request, '¡Opinión enviada con éxito!')
        return redirect('cruise_detail', pk=pk)
    
    return redirect('cruise_detail', pk=pk)
