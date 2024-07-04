from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('encrypt/<int:uploaded_image_id>/', views.encrypt_image, name='encrypt_image'),
    path('decrypt/', views.decrypt_image, name='decrypt_image'),
]
