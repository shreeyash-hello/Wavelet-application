import numpy as np
import pywt
import matplotlib.pyplot as plt

def logistic_map(x, r, size):
    seq = np.zeros(size)
    seq[0] = x
    for i in range(1, size):
        seq[i] = r * seq[i - 1] * (1 - seq[i - 1])
    return seq

def chaotic_wavelet_encrypt(image, wavelet='haar', level=1, r=3.9):
    # Perform wavelet decomposition
    coeffs = pywt.wavedec2(image, wavelet, level=level)
    coeff_arr, coeff_slices = pywt.coeffs_to_array(coeffs)

    x = 0.5
    chaotic_sequence = logistic_map(x, r, coeff_arr.size)

    permuted_indices = np.argsort(chaotic_sequence)
    encrypted_coeff_arr = coeff_arr.flatten()
    encrypted_coeff_arr = encrypted_coeff_arr[permuted_indices]

    encrypted_coeff_arr = encrypted_coeff_arr.reshape(coeff_arr.shape)

    encrypted_coeffs = pywt.array_to_coeffs(encrypted_coeff_arr, coeff_slices, output_format='wavedec2')

    encrypted_image = pywt.waverec2(encrypted_coeffs, wavelet)

    return encrypted_image, permuted_indices

def chaotic_wavelet_decrypt(encrypted_image, permuted_indices, wavelet='haar', level=1, r=3.9):
    encrypted_coeffs = pywt.wavedec2(encrypted_image, wavelet, level=level)
    encrypted_coeff_arr, coeff_slices = pywt.coeffs_to_array(encrypted_coeffs)

    decrypted_coeff_arr = np.zeros_like(encrypted_coeff_arr.flatten())
    decrypted_coeff_arr[permuted_indices] = encrypted_coeff_arr.flatten()

    decrypted_coeff_arr = decrypted_coeff_arr.reshape(encrypted_coeff_arr.shape)

    decrypted_coeffs = pywt.array_to_coeffs(decrypted_coeff_arr, coeff_slices, output_format='wavedec2')

    decrypted_image = pywt.waverec2(decrypted_coeffs, wavelet)

    return decrypted_image
