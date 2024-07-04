from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class EncryptedData(models.Model):
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE)
    encrypted_image = models.ImageField(upload_to='encrypted/')
    npz_file = models.FileField(upload_to='npz/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
