import os
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ImageForm
from .models import ImageModel
from PIL import Image
import numpy as np
import pywt

def home(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return redirect('compress', pk=instance.pk)
    else:
        form = ImageForm()
    return render(request, 'wavelet_webapp/home.html', {'form': form})

def compress(request, pk):
    image_instance = ImageModel.objects.get(pk=pk)
    original_image_path = os.path.join(settings.MEDIA_ROOT, image_instance.image.name)
    original_image = Image.open(original_image_path)
    image_array = np.array(original_image)

    # Perform wavelet transform
    coeffs = pywt.wavedec2(image_array, 'haar', level=1)
    coeffs[0] *= 0.5  # Simple compression by reducing the approximation coefficients
    compressed_image_array = pywt.waverec2(coeffs, 'haar')
    compressed_image = Image.fromarray(np.uint8(compressed_image_array))

    # Save compressed image
    compressed_image_path = os.path.join(settings.MEDIA_ROOT, 'images/compressed/', f'compressed_{os.path.basename(image_instance.image.name)}')
    compressed_image.save(compressed_image_path)

    # Update model with compressed image path
    image_instance.compressed_image = f'images/compressed/compressed_{os.path.basename(image_instance.image.name)}'
    image_instance.save()

    return render(request, 'wavelet_webapp/compress.html', {
        'original_image': image_instance.image.url,
        'compressed_image': image_instance.compressed_image.url,
        'original_size': original_image.size,
        'compressed_size': compressed_image.size,
    })
