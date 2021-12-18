import time

from pydicom import dcmread
import numpy as np
import pydicom as pyd
import os
from PIL import ImageOps, ImageEnhance
from PIL.ImageQt import *
import cv2
import matplotlib.pyplot as plt


_BENCHMARK = True
_FAST = True


factor_bright = 1
factor_contrast = 1
autocontrast_mode = 0
inversion_mode = 0
width_of = 450

def readFromDicomAndNormalize(filename):
    plan = pyd.read_file(filename)
    image_2d = plan.pixel_array.astype(float)
    image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0
    image_2d_scaled = np.uint8(image_2d_scaled)
    return image_2d_scaled

def readFromJpgAndNormalize(filename):
    return

def dicom_to_qt(dcm_file):
    image = readFromDicomAndNormalize(dcm_file)
    qim = np_to_qt(image)
    return qim

def np_to_qt(image):
    image = cv2.resize(image, (200,200), cv2.INTER_AREA)
    image = Image.fromarray(image)
    # enhancer = ImageEnhance.Contrast(image)
    # image = enhancer.enhance(factor_contrast)
    # enhancer = ImageEnhance.Brightness(image)
    # image = enhancer.enhance(factor_bright)
    qim_ = ImageQt(image)
    return (qim_)

def point(imraw,threshold):
    start = time.time()
    if _FAST:
        _, imnew = cv2.threshold(imraw, threshold, 255, cv2.THRESH_BINARY)
    else:
        imnew=np.zeros(imraw.shape)
        for i in range(imraw.shape[0]):
            for j in range(imraw.shape[1]):
                if imraw[i,j]>=threshold: imnew[i,j]=255
                else:imnew[i,j]=0
    if _BENCHMARK: print("Point image ", imraw.shape, ", in ", time.time()-start, "s")
    return imnew

def otsuThresh(img):
    start = time.time()
    size=np.shape(img)[0]*np.shape(img)[1]
    final_t=0
    max_g=0
    for t in range(255):
        n0 = img[np.where(img < t)]
        n1 = img[np.where(img >= t)]
        w0 = len(n0) / size
        w1 = len(n1) / size
        u0 = np.mean(n0) if len(n0) > 0 else 0.
        u1 = np.mean(n1) if len(n0) > 0 else 0.
        g = w0 * w1 * (u0 - u1) ** 2
        if g>max_g:
            max_g=g
            final_t=t
    if _BENCHMARK: print("calculate otsu image ", img.shape, ", in ", time.time() - start, "s")
    return final_t

def normalizeBinary(imgBin):
    start = time.time()
    img = imgBin.copy()
    img[np.where(img == img.min())] = 0
    img[np.where(img > 0)] = 255
    if _BENCHMARK: print("Normalize image ", img.shape, ", in ", time.time() - start, "s")
    return np.uint8(img)

def histControlImg(img):
    img = plt.hist(img.flatten(),bins=256)
    plt.savefig("histimg.png",format = "png")

    img = QImage()
    img.load("./histimg.png")
    return QPixmap.fromImage(img)

def emptyQtPixelMap(size):
    array = np.zeros((512, 512), dtype=np.uint8)
    qimg = np_to_qt(array)
    qpix = QPixmap.fromImage(qimg)
    return qpix.scaled(size)