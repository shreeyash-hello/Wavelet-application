from django.db import models

class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')
    compressed_image = models.ImageField(upload_to='images/compressed/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
