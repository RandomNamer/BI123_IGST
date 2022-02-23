from util import *
import cv2
import pydicom

raw = readFromDicomAndNormalize("/Users/zzy/Desktop/Image Processing CourseWorks/lab1/1091.dcm")
# thresh = point(raw, 64)
# cv2.imwrite("/Users/zzy/Desktop/Image Processing CourseWorks/lab1/1168-bin.png", thresh)
noised = addsalt_pepper(raw, 0.9)
noised = point(noised, 64)
cv2.imwrite("/Users/zzy/Desktop/Image Processing CourseWorks/lab1/1091-noised.png", noised)