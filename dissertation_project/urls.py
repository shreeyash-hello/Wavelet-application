from django.conf import settings
from django.contrib import admin
from django.urls import path
from wavelet_webapp import views as wavelet_views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', wavelet_views.upload_image, name='upload_image'),
    path('encrypt/<int:uploaded_image_id>/', wavelet_views.encrypt_image, name='encrypt_image'),
    path('decrypt/', wavelet_views.decrypt_image, name='decrypt_image'),
    path('compress/<int:uploaded_image_id>/', wavelet_views.compress_image_view, name='compress_image'),
    path('enhance/<int:uploaded_image_id>/', wavelet_views.process_image, name='enhance_image'),
    path('', wavelet_views.home_view, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)