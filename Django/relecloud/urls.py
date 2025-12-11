## APP (relecloud)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('destinations', views.destination, name='destination'),
    path('destination/<int:pk>', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('destination/<int:pk>/purchase', views.purchase_destination, name='purchase_destination'),
    path('destination/<int:pk>/review', views.create_destination_review, name='create_destination_review'),
    path('cruise/<int:pk>', views.CruiseDetailView.as_view(), name='cruise_detail'),
    path('cruise/<int:pk>/purchase', views.purchase_cruise, name='purchase_cruise'),
    path('cruise/<int:pk>/review', views.create_cruise_review, name='create_cruise_review'),
    path('info_request', views.InfoRequestCreate.as_view(), name='info_request'),
]