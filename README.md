# 🌊 Wavelet Application

A Django web application that demonstrates **image encryption, compression, and denoising** using **Wavelet transforms**.  
This project combines **signal/image processing** with a **web interface**, showing how wavelet-based methods can be applied in practice.

---

## 🔍 Overview
This project explores the use of the **Discrete Wavelet Transform (DWT)** in image processing.  
The system allows users to upload images, which are decomposed into wavelet coefficients and then processed for:  
- 🔐 **Encryption & Decryption**  
- 📦 **Compression**  
- 🎨 **Denoising**

The processed image is reconstructed using the **Inverse Discrete Wavelet Transform (IDWT)**.

---

## 🏗️ System Architecture

The diagram below shows the flow of the application:

![System Architecture](SYS.png)

1. User uploads an image via the **browser interface**.  
2. The server applies **DWT** to decompose the image.  
3. Depending on the selected operation:  
   - **Encryption:** chaotic sequence + wavelet coefficients  
   - **Compression:** quantisation & encoding of coefficients  
   - **Denoising:** thresholding coefficients to remove noise  
4. The modified coefficients are passed through **IDWT** to reconstruct the final image.  

---

## ✨ Features
- Upload and process images via the browser.  
- Apply wavelet-based encryption, compression, or denoising.  
- Reconstruct images using inverse transforms.  
- Store uploaded and processed images in a database.  

---

## 🛠 Tech Stack
- **Backend:** Python, Django  
- **Image Processing:** PyWavelets, NumPy, OpenCV  
- **Frontend:** HTML, CSS, Django Templates  
