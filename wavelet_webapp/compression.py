from PIL import Image
import numpy as np
import pywt

def quantize(coefficients, quantization_factor):
    return np.round(coefficients / quantization_factor)

def dequantize(quantized_coefficients, quantization_factor):
    return quantized_coefficients * quantization_factor

def entropy_encode(data):
    encoded = []
    previous_value = data[0]
    count = 1
    for value in data[1:]:
        if value == previous_value:
            count += 1
        else:
            encoded.append((previous_value, count))
            previous_value = value
            count = 1
    encoded.append((previous_value, count))
    return encoded

def entropy_decode(encoded):
    decoded = []
    for value, count in encoded:
        decoded.extend([value] * count)
    return np.array(decoded)

def calculate_compression_ratio(original_size, compressed_size):
    return original_size / compressed_size

def calculate_psnr(original_image, decompressed_image):
    mse = np.mean((original_image.astype(float) - decompressed_image.astype(float)) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr

def compress_image(image_array, wavelet='bior2.2', quantization_factor=10):
    coeffs = pywt.dwtn(image_array, wavelet)

    quantized_coeffs = {}
    for key in coeffs.keys():
        quantized_coeffs[key] = quantize(coeffs[key], quantization_factor)

    encoded_coeffs = {}
    for key in quantized_coeffs.keys():
        encoded_coeffs[key] = entropy_encode(quantized_coeffs[key].flatten())

    original_size = image_array.size
    compressed_size = sum(len(encoded) for encoded in encoded_coeffs.values())

    return encoded_coeffs, coeffs, original_size, compressed_size

def decompress_image(encoded_coeffs, wavelet_coeffs, shape_image, wavelet='bior2.2', quantization_factor=10):
    quantized_coeffs = {}
    for key in encoded_coeffs.keys():
        quantized_coeffs[key] = entropy_decode(encoded_coeffs[key]).reshape(wavelet_coeffs[key].shape)

    coeffs = {}
    for key in quantized_coeffs.keys():
        coeffs[key] = dequantize(quantized_coeffs[key], quantization_factor)

    reconstructed_image = pywt.idwtn(coeffs, wavelet)

    reconstructed_image = np.clip(reconstructed_image, 0, 255).astype(np.uint8)

    decompressed_image = Image.fromarray(reconstructed_image)

    return decompressed_image
