# 📊 Wavelet Application – Project Report  

## 📌 1. Overview  
This project is a **web application** that allows users to process images using **wavelet transforms**.  

The system has **three main features**:  
- 🗜️ **Image Compression** → Make images smaller in size without losing too much quality.  
- ✨ **Image Denoising** → Remove unwanted noise (grainy dots) to make images clearer.  
- 🔒 **Image Encryption/Decryption** → Secure images by scrambling them into unreadable form and restoring them back.  

👉 In short: **Compress it. Clean it. Protect it.**  

---

## 🎯 2. Objectives  
- Build an **easy-to-use web app** where anyone can try wavelet image processing.  
- Show how **mathematics (wavelets)** can solve real problems.  
- Measure performance using:  
  - **Compression Ratio (CR)** → Storage savings  
  - **PSNR (Peak Signal-to-Noise Ratio)** → Image quality  
  - **SSIM (Structural Similarity Index)** → How similar processed image is to original  

---

## ⚙️ 3. How It Works  

**Step-by-Step Flow:**  
1. User **uploads an image**.  
2. Chooses an **operation** → Compress / Denoise / Encrypt.  
3. System applies **wavelet processing** in the backend.  
4. **Results** are shown with metrics.  
5. User can **download** the new image.  

**Architecture (Simplified):**  
- 🖥️ **Frontend**: HTML + CSS (user interface)  
- 🐍 **Backend**: Python (Django framework)  
- 🧮 **Libraries**: PyWavelets, NumPy, OpenCV  
- 🗄️ **Database**: SQLite (for image handling)  

---

## 🔬 4. Features Explained  

<details>
<summary>📉 Image Compression</summary>  

- Removes less-important details from the image.  
- Keeps the important structure (so it still looks good).  
- Saves storage space.  

**Metric:** Compression Ratio (CR) = Original Size ÷ Compressed Size  
</details>  

<details>
<summary>🧹 Image Denoising</summary>  

- Removes unwanted “grainy” or “snowy” dots (noise).  
- Wavelets separate noise from real image details.  
- Restores a cleaner, sharper image.  

**Metrics:**  
- PSNR (higher = better quality)  
- SSIM (closer to 1 = more similar to original)  
</details>  

<details>
<summary>🔐 Image Encryption & Decryption</summary>  

- Encryption scrambles the pixels → image looks like random patterns.  
- Decryption restores it back to the original.  
- Protects sensitive data (medical images, personal photos, etc.).  
</details>  

---

## 📈 5. Results  

| Feature          | Before Processing                | After Processing                 | Metrics / Outcome |
|------------------|----------------------------------|----------------------------------|------------------|
| **Compression**  | Size: 1.2 MB                     | Size: 0.35 MB                     | CR ≈ 3.4× smaller <br> SSIM: 0.92 |
| **Denoising**    | PSNR: 18.5 dB <br> SSIM: 0.71    | PSNR: 28.7 dB <br> SSIM: 0.90    | Much clearer image |
| **Encryption**   | Original visible                 | Encrypted: scrambled patterns     | Fully unreadable without key |

---

## 🖼️ 6. Screenshots  

### Upload Page  
![Upload Example](Screenshots/upload.png)  

### Compression Example  
| Original | Compressed |
|----------|------------|
| ![orig](Screenshots/original.png) | ![comp](Screenshots/compressed.png) |

### Denoising Example  
| Noisy Image | Denoised Image |
|-------------|----------------|
| ![noisy](Screenshots/noisy.png) | ![clean](Screenshots/denoised.png) |

### Encryption Example  
| Original | Encrypted | Decrypted |
|----------|-----------|-----------|
| ![orig](Screenshots/original.png) | ![enc](Screenshots/encrypted.png) | ![dec](Screenshots/decrypted.png) |

---

## ✅ 7. Conclusion  
- The project shows that **wavelet transforms** are powerful tools for image processing.  
- Users can **shrink, clean, and protect** images with a simple web interface.  
- The system combines **mathematical concepts + practical application** in an easy way.  

---

## 🚀 8. Future Improvements  
- Add more wavelet families (Haar, Daubechies, Symlets).  
- Let users pick compression level or denoising strength.  
- Support multiple images at once.  
- Deploy online for public access.  

---

## 📚 9. References  
- [PyWavelets Documentation](https://pywavelets.readthedocs.io/)  
- [OpenCV Image Processing](https://opencv.org/)  
- Mallat, S. *A Wavelet Tour of Signal Processing*  

---
