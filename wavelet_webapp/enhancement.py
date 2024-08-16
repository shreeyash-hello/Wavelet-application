import numpy as np
import pywt
from skimage import metrics
from skimage.restoration import denoise_nl_means

def add_gaussian_noise(image, mean=0, var=0.01):
    sigma = np.sqrt(var)
    noise = np.random.normal(mean, sigma, image.shape)
    noisy_image = image + noise
    return noisy_image

def wavelet_denoising(image, wavelet='db1', level=2, threshold_factor=0.2, threshold_mode='soft'):
    coeffs = pywt.wavedec2(image, wavelet, level=level)
    approximation_coeffs = coeffs[0]
    sigma = np.median(np.abs(approximation_coeffs - np.median(approximation_coeffs))) / 0.6745
    threshold = threshold_factor * sigma
    coeffs_thresh = list(coeffs)
    coeffs_thresh[1:] = [tuple(pywt.threshold(c, threshold, mode=threshold_mode) for c in subcoeffs) for subcoeffs in coeffs_thresh[1:]]
    denoised_image = pywt.waverec2(coeffs_thresh, wavelet)
    return denoised_image

def nl_means_denoising(image, patch_size=5, patch_distance=6, h=0.1):
    return denoise_nl_means(image, patch_size=patch_size, patch_distance=patch_distance, h=h)

def compute_psnr(original, denoised):
    return metrics.peak_signal_noise_ratio(original, denoised)

def compute_ssim(original, denoised):
    return metrics.structural_similarity(original, denoised, data_range=denoised.max() - denoised.min())