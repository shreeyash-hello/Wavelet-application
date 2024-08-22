import numpy as np
import pywt
from PIL import Image

def calculate_std_threshold(coeffs):
    thresholds = {}
    for i, (cH, cV, cD) in enumerate(coeffs[1:]):
        thresholds[f'cH{i+1}'] = np.std(cH)
        thresholds[f'cV{i+1}'] = np.std(cV)
        thresholds[f'cD{i+1}'] = np.std(cD)
    return thresholds

def std_thresholding(coeffs, thresholds):
    thresholded_coeffs = [coeffs[0]]
    for i, (cH, cV, cD) in enumerate(coeffs[1:]):
        cH = np.where(np.abs(cH) > thresholds[f'cH{i+1}'], cH, 0)
        cV = np.where(np.abs(cV) > thresholds[f'cV{i+1}'], cV, 0)
        cD = np.where(np.abs(cD) > thresholds[f'cD{i+1}'], cD, 0)
        thresholded_coeffs.append((cH, cV, cD))
    return thresholded_coeffs

def quantize(coefficients, quantization_factor):
    if isinstance(coefficients, tuple):
        return tuple(quantize(subband, quantization_factor) for subband in coefficients)
    else:
        return np.round(coefficients / quantization_factor)

def dequantize(quantized_coefficients, quantization_factor):
    if isinstance(quantized_coefficients, tuple):
        return tuple(dequantize(subband, quantization_factor) for subband in quantized_coefficients)
    else:
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

def compress_image(image_array, wavelet='haar', quantization_factor=10):
    coeffs = pywt.wavedec2(image_array, wavelet, level=1)

    thresholds = calculate_std_threshold(coeffs)

    thresholded_coeffs = std_thresholding(coeffs, thresholds)

    quantized_coeffs = [quantize(coeff, quantization_factor) for coeff in thresholded_coeffs]

    encoded_coeffs = {}
    for i, coeff in enumerate(quantized_coeffs):
        if isinstance(coeff, tuple):
            for j, subband in enumerate(coeff):
                encoded_coeffs[f'coeff_{i}_{j}'] = entropy_encode(subband.flatten())
        else:
            encoded_coeffs[f'coeff_{i}_0'] = entropy_encode(coeff.flatten())

    original_size = image_array.size
    compressed_size = sum(len(encoded) for encoded in encoded_coeffs.values())

    return encoded_coeffs, coeffs, original_size, compressed_size

def decompress_image(encoded_coeffs, wavelet_coeffs, shape_image, wavelet='haar', quantization_factor=10):
    decoded_coeffs = []
    for i, coeff in enumerate(wavelet_coeffs):
        if isinstance(coeff, tuple):
            subbands = []
            for j in range(len(coeff)):
                encoded_key = f'coeff_{i}_{j}'
                decoded_subband = entropy_decode(encoded_coeffs[encoded_key])
                subbands.append(decoded_subband.reshape(coeff[j].shape))
            decoded_coeffs.append(tuple(dequantize(subband, quantization_factor) for subband in subbands))
        else:
            encoded_key = f'coeff_{i}_0'
            decoded_subband = entropy_decode(encoded_coeffs[encoded_key])
            decoded_coeffs.append(dequantize(decoded_subband.reshape(coeff.shape), quantization_factor))

    reconstructed_image = pywt.waverec2(decoded_coeffs, wavelet)

    reconstructed_image = np.clip(reconstructed_image, 0, 255).astype(np.uint8)

    if reconstructed_image.shape != shape_image:
        reconstructed_image = reconstructed_image[:shape_image[0], :shape_image[1]]

    decompressed_image = Image.fromarray(reconstructed_image)

    return decompressed_image
