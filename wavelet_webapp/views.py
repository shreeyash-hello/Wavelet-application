from django.conf import settings
from django.shortcuts import render, redirect
from django.shortcuts import render
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image
import base64
from io import BytesIO
from .enhancement import nl_means_denoising, compute_psnr, compute_ssim, wavelet_denoising, add_gaussian_noise
from .models import UploadedImage, EncryptedData
from .forms import UploadImageForm
from .encryption import chaotic_wavelet_encrypt, chaotic_wavelet_decrypt, resize_image, psnr
from .compression import compress_image, decompress_image, calculate_compression_ratio, calculate_psnr
from skimage import io, img_as_float
import os
from PIL import Image


def home_view(request):
    return redirect('upload_image')

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            operation = form.cleaned_data['operation']
            if operation == 'encrypt':
                return redirect('encrypt_image', uploaded_image_id=uploaded_image.id)
            elif operation == 'compress':
                return redirect('compress_image', uploaded_image_id=uploaded_image.id)
            elif operation == 'enhance':
                return redirect('enhance_image', uploaded_image_id=uploaded_image.id)
    else:
        form = UploadImageForm()
    return render(request, 'wavelet_webapp/upload_image.html', {'form': form})


def encrypt_image(request, uploaded_image_id):
    uploaded_image = UploadedImage.objects.get(pk=uploaded_image_id)

    if request.method == 'POST':
        image_path = uploaded_image.image.path
        image = plt.imread(image_path)

        if image.ndim == 3:
            r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
            image = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.float32)

        encrypted_image, permuted_indices = chaotic_wavelet_encrypt(image)

        encrypted_image = resize_image(encrypted_image, image.shape)

        original_image_path = os.path.join(settings.MEDIA_ROOT, 'original', 'original_image.npy')
        os.makedirs(os.path.dirname(original_image_path), exist_ok=True)
        np.save(original_image_path, image)

        encrypted_image_path = os.path.join(settings.MEDIA_ROOT, 'encrypted', 'encrypted_image.png')
        os.makedirs(os.path.dirname(encrypted_image_path), exist_ok=True)
        plt.imsave(encrypted_image_path, encrypted_image, cmap='gray')

        npz_file_path = os.path.join(settings.MEDIA_ROOT, 'npz', 'encrypted_data.npz')
        os.makedirs(os.path.dirname(npz_file_path), exist_ok=True)
        np.savez_compressed(npz_file_path, encrypted_image=encrypted_image.astype(np.float32),
                            permuted_indices=permuted_indices)

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

        decrypted_image = chaotic_wavelet_decrypt(encrypted_image, permuted_indices)

        decrypted_image_path = os.path.join(settings.MEDIA_ROOT, 'decrypted', 'decrypted_image.png')
        os.makedirs(os.path.dirname(decrypted_image_path), exist_ok=True)
        plt.imsave(decrypted_image_path, decrypted_image, cmap='gray')

        original_image_path = os.path.join(settings.MEDIA_ROOT, 'original', 'original_image.npy')
        original_image = np.load(original_image_path)

        decrypted_image = resize_image(decrypted_image, original_image.shape)

        psnr_value = psnr(original_image, decrypted_image)

        decrypted_image_url = os.path.join(settings.MEDIA_URL, 'decrypted', 'decrypted_image.png')

        return render(request, 'wavelet_webapp/decryption_success.html',
                      {'decrypted_image_path': decrypted_image_url, 'psnr_value': psnr_value})

    return render(request, 'wavelet_webapp/decrypt_image.html')


def compress_image_view(request, uploaded_image_id):
    uploaded_image = UploadedImage.objects.get(pk=uploaded_image_id)

    if request.method == 'POST':
        image_path = uploaded_image.image.path

        rgb_image = Image.open(image_path)
        grayscale_image = np.array(rgb_image)
        original_array = np.array(grayscale_image)

        encoded_coeffs, wavelet_coeffs, original_size, compressed_size = compress_image(original_array)

        decompressed_image = decompress_image(encoded_coeffs, wavelet_coeffs, original_array.shape)

        decompressed_image_path = os.path.join(settings.MEDIA_ROOT, 'decompressed', 'decompressed_image.png')
        os.makedirs(os.path.dirname(decompressed_image_path), exist_ok=True)
        decompressed_image.save(decompressed_image_path)

        compression_ratio = calculate_compression_ratio(original_size, compressed_size)
        psnr_value = calculate_psnr(original_array, np.array(decompressed_image))

        decompressed_image_url = os.path.join(settings.MEDIA_URL, 'decompressed', 'decompressed_image.png')

        return render(request, 'wavelet_webapp/compression_success.html', {
            'decompressed_image_path': decompressed_image_url,
            'compression_ratio': compression_ratio,
            'psnr_value': psnr_value,
        })

    return render(request, 'wavelet_webapp/compress_image.html', {'uploaded_image': uploaded_image})


def process_image(request, uploaded_image_id):
    uploaded_image = UploadedImage.objects.get(pk=uploaded_image_id)
    if request.method == 'POST':
        image_path = uploaded_image.image.path


        image = PIL.Image.open(image_path).convert('L')
        image_float = img_as_float(np.array(image))

        noisy_image = add_gaussian_noise(image_float, mean=0, var=0.01)

        wavelets = ['bior4.4', 'db4', 'sym4']
        levels = [1, 2]
        threshold_factors = [0.1, 0.2]
        threshold_modes = ['soft', 'hard']

        best_psnr = -np.inf
        best_ssim = -np.inf
        best_params_psnr = None
        best_params_ssim = None
        best_denoised_psnr = None
        best_denoised_ssim = None

        for wavelet in wavelets:
            for level in levels:
                for threshold_factor in threshold_factors:
                    for threshold_mode in threshold_modes:
                        denoised_image = wavelet_denoising(noisy_image, wavelet=wavelet, level=level,
                                                               threshold_factor=threshold_factor,
                                                               threshold_mode=threshold_mode)
                        psnr = compute_psnr(image_float, denoised_image)
                        ssim = compute_ssim(image_float, denoised_image)

                        if psnr > best_psnr:
                            best_psnr = psnr
                            best_params_psnr = (wavelet, level, threshold_factor, threshold_mode)
                            best_denoised_psnr = denoised_image

                        if ssim > best_ssim:
                            best_ssim = ssim
                            best_params_ssim = (wavelet, level, threshold_factor, threshold_mode)
                            best_denoised_ssim = denoised_image

        denoised_image_nl_means = nl_means_denoising(noisy_image)
        psnr_nl_means = compute_psnr(image_float, denoised_image_nl_means)
        ssim_nl_means = compute_ssim(image_float, denoised_image_nl_means)

        if psnr_nl_means > best_psnr:
            best_psnr = psnr_nl_means
            best_denoised_psnr = denoised_image_nl_means

        if ssim_nl_means > best_ssim:
            best_ssim = ssim_nl_means
            best_denoised_ssim = denoised_image_nl_means

        def image_to_base64(image):
            buf = BytesIO()
            plt.imsave(buf, image, format='png', cmap='gray')
            buf.seek(0)
            return base64.b64encode(buf.getvalue()).decode('utf-8')

        context = {
                'original_image': image_to_base64(image_float),
                'noisy_image': image_to_base64(noisy_image),
                'best_denoised_psnr': image_to_base64(best_denoised_psnr),
                'best_denoised_ssim': image_to_base64(best_denoised_ssim),
                'best_psnr': best_psnr,
                'best_ssim': best_ssim,
                'best_params_psnr': best_params_psnr,
                'best_params_ssim': best_params_ssim,
        }

        return render(request, 'wavelet_webapp/enhancement_success.html', context)

    return render(request, 'wavelet_webapp/enhance_image.html', {'uploaded_image': uploaded_image})

