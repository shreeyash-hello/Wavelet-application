from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('compress/<int:pk>/', views.compress, name='compress'),
]
