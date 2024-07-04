import os
import numpy as np
import matplotlib.pyplot as plt
from django.conf import settings
from django.shortcuts import render, redirect
from .models import UploadedImage, EncryptedData
from .forms import UploadImageForm
from .encryption import chaotic_wavelet_encrypt, chaotic_wavelet_decrypt


def home_view(request):
    return redirect('upload_image')  # Redirect to the upload image page


def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            return redirect('encrypt_image', uploaded_image_id=uploaded_image.id)
    else:
        form = UploadImageForm()
    return render(request, 'wavelet_webapp/upload_image.html', {'form': form})


def encrypt_image(request, uploaded_image_id):
    uploaded_image = UploadedImage.objects.get(pk=uploaded_image_id)

    if request.method == 'POST':
        # Load the uploaded image
        image_path = uploaded_image.image.path
        image = plt.imread(image_path)

        # Ensure image is grayscale (if RGB, convert to grayscale)
        if image.ndim == 3:
            image = np.mean(image, axis=2).astype(np.float32)

        # Encrypt the image
        encrypted_image, permuted_indices = chaotic_wavelet_encrypt(image)

        # Save encrypted image
        encrypted_image_path = os.path.join(settings.MEDIA_ROOT, 'encrypted', 'encrypted_image.png')
        os.makedirs(os.path.dirname(encrypted_image_path), exist_ok=True)
        plt.imsave(encrypted_image_path, encrypted_image, cmap='gray')

        # Save npz file
        npz_file_path = os.path.join(settings.MEDIA_ROOT, 'npz', 'encrypted_data.npz')
        os.makedirs(os.path.dirname(npz_file_path), exist_ok=True)
        np.savez_compressed(npz_file_path, encrypted_image=encrypted_image.astype(np.float32),
                            permuted_indices=permuted_indices)

        # Save EncryptedData instance
        encrypted_data = EncryptedData.objects.create(
            image=uploaded_image,
            encrypted_image='encrypted/encrypted_image.png',
            npz_file='npz/encrypted_data.npz'
        )

        return render(request, 'wavelet_webapp/encryption_success.html', {'encrypted_data': encrypted_data})

    return render(request, 'wavelet_webapp/encrypt_image.html', {'uploaded_image': uploaded_image})


def decrypt_image(request):
    if request.method == 'POST':
        npz_file = request.FILES['npz_file']
        with np.load(npz_file) as data:
            encrypted_image = data['encrypted_image']
            permuted_indices = data['permuted_indices']

        # Decrypt the image
        decrypted_image = chaotic_wavelet_decrypt(encrypted_image, permuted_indices)

        # Save decrypted image
        decrypted_image_path = os.path.join(settings.MEDIA_ROOT, 'decrypted', 'decrypted_image.png')
        os.makedirs(os.path.dirname(decrypted_image_path), exist_ok=True)
        plt.imsave(decrypted_image_path, decrypted_image, cmap='gray')

        # Construct the URL for the decrypted image
        decrypted_image_url = os.path.join(settings.MEDIA_URL, 'decrypted', 'decrypted_image.png')

        return render(request, 'wavelet_webapp/decryption_success.html', {'decrypted_image_path': decrypted_image_url})

    return render(request, 'wavelet_webapp/decrypt_image.html')
