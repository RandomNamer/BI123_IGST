import time

from PyQt5.QtCore import Qt
from pydicom import dcmread
import numpy as np
import pydicom as pyd
import os
from PIL import ImageOps, ImageEnhance
from PIL.ImageQt import *
import cv2
import matplotlib.pyplot as plt
from skimage.filters.rank import entropy
from skimage.morphology import disk
from scipy import signal
from numpy.fft import fft2,fftshift,ifft2,ifftshift



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
    print("Reading non-dcm...")
    raw = np.array(cv2.imread(filename))
    if(len(np.shape(raw)) == 3): raw = raw[:, :, 0];
    scaled = (raw / raw.max()) * 255
    return np.uint8(scaled)

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


def entropyLevelSeg(imraw, level):
    start = time.time()
    k = disk(6)
    e = entropy(imraw, k)
    normalized = e / e.max()
    res = np.zeros_like(imraw, dtype=np.uint8)
    resIdx = np.where(normalized > level)
    res[resIdx] = 255
    if _BENCHMARK: print("Entropy in ", time.time()-start, "s.")
    return res
    # return np.uint8(normalized * 255)

def conv2D(array, kernel):
    ks = np.shape(kernel)[0]
    stride = int(ks/2)
    assert(np.shape(kernel)[0] == np.shape(kernel)[1])
    kernel = np.transpose(kernel)
    assert(ks%2 == 1)
    res = np.zeros_like(array)
    for x in range(1, np.shape(array)[0] - stride):
        for y in range(1, np.shape(array)[1] - stride):
            roi = np.array(array[(x-stride): (x+stride+1), (y-stride): (y+stride+1)])
            assert(np.shape(roi) == np.shape(kernel))
            res[x][y] = np.sum(roi * kernel)
    return res



def sobel(imgArray):
    k = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    if _FAST:
        return abs(signal.convolve2d(imgArray, k, boundary='symm',mode='same'))
    else:
        return abs(conv2D(imgArray, k))

def prewitt(imgArray):
    k = np.array([[-1, 0, -1], [-1, 0, -1], [-1, 0, -1]])
    if _FAST:
        return abs(signal.convolve2d(imgArray, k, boundary='symm',mode='same'))
    else:
        return abs(conv2D(imgArray, k))

def roberts(imgArray):
    k = np.array([[0,1,0],[1,-4,1],[0,1,0]])
    if _FAST:
        return abs(signal.convolve2d(imgArray, k, boundary='symm',mode='same'))
    else:
        return abs(conv2D(imgArray, k))

def setImageArrayForWidget(arr, widget):
    arr = np.uint8(arr)
    qimg = np_to_qt(arr)
    pix = QPixmap.fromImage(qimg)
    pix_resized = pix.scaled(widget.size(), Qt.KeepAspectRatio)
    widget.setPixmap(pix_resized)

def gaussianLPF(imraw,CutOffFreq=0,CutOffFreqPercentage=0.1,order=2):
    f=fftshift(fft2(imraw))
    f_out=np.empty_like(f)
    f_show=np.zeros_like(f,dtype=np.float32)
    #print(f_out.shape)
    orgx,orgy=np.int16(f.shape[0]/2),np.int16(f.shape[1]/2)
    if CutOffFreq==0 and CutOffFreqPercentage==0:
        print('Lack of cutoff freq args.')
        return 0
    if  CutOffFreqPercentage: d0=np.int16((min(f.shape)*CutOffFreqPercentage)/2)
    else: d0=CutOffFreq
    for x in range(f.shape[0]):
        for y in range(f.shape[1]):
            d=np.sqrt((x-orgx)**2+(y-orgy)**2)
            h=np.exp(-0.5*(d**2/d0**2))
            #print(h)
            f_out[x][y]=h*f[x][y]
            f_show[x][y]=h
    # return f_out,f_show
    return np.uint8(ifft2(ifftshift(f_out)))

def median(imraw,ksize=3):
    h,w=np.shape(imraw)
    length=int((ksize-1)/2)
    im=np.zeros((h,w))
    for x in range(h):
        for y in range(w):
            if x <= length - 1 or x >= h - 1 - length or y <= length - 1 or y >= h - length - 1:
                im[x,y]=imraw[x,y]
            else:
                im[x,y]=np.median(imraw[x-length:x+length+1,y-length:y+length+1])
    return im

def dilation(img, ksize = 5):
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
    if _FAST:
        return cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel=k, iterations=1)

def erosion(img, ksize = 5):
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
    if _FAST:
        return cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel=k, iterations=1)

def opening(img, ksize = 5):
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
    if _FAST:
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel=k, iterations=1)

def closing(img, ksize = 5):
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
    if _FAST:
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel=k, iterations=1)

def morphologicalGradient(img, mode="full", ksize = 5):
    if mode == "full":
        return dilation(img, ksize) - erosion(img, ksize)
    if mode == "inter":
        return img - erosion(img, ksize)
    if mode == "extern":
        return dilation(img, ksize) - img

def morphologicalReconstruct(original, marker):
    m = marker
    runCount = 0
    while True:
        # if runCount%100==0:
        #     print("checkpoint")
        t = m
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        m = cv2.morphologyEx(m, cv2.MORPH_DILATE, kernel=k,iterations=1)
        m = cv2.bitwise_and(m, original)
        if (t==m).all(): return m
        else: runCount+=1

#Add pepper noise:
def addsalt_pepper(img, SNR):
    img_ = img.copy()
    h, w = img_.shape
    mask = np.random.choice((0,1, 2), size=(h, w), p=[SNR,(1-SNR)/2,(1 - SNR)/2 ])
    mask = np.repeat(mask, 1, axis=0)
    img_[mask==1]=255
    img_[mask == 2] = 0
    return img_

def automaticMorphologicalReconstruction(img, ksize = 11):
    mask = opening(img, ksize)
    return morphologicalReconstruct(img, mask)