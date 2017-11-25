"""
Performs CT scan attenuation rescale on a folder of images. 
Primarily aimed at converting 16bit tiff images from the Talisman Test Suite to RGB jpgs.
"""

import cv2
import os
import numpy as np


def map_HU_to_RGB(value, minHU, maxHU):
    ''' Rescales Hounsfield unit to the range [0,255] using linear transformation. 

    Inputs:
        value: Hounsfield unit (integer)
        minHU: Hounsfield unit value to map to 0 (integer)
        maxHU: Hounsfield unit value to map to 255 (integer)
    Output: Integer in range [0,255]
    '''

    if value < minHU:
        newValue = 0
    elif value > maxHU:
        newValue = 255
    else:
        spanHU = maxHU - minHU
        valueScaled = float(value - minHU) / float(spanHU)
        newValue = int((valueScaled * 255))
    
    return newValue


v_map_HU_to_RGB = np.vectorize(map_HU_to_RGB) # allow map_HU_to_RGB to be used pointwise on numpy array


def convert_image(inputFilePath, outputFilePath, minR, maxR, minG, maxG, minB, maxB):
    ''' Converts 16bit grayscale tiff image to 8bit rgb jpg.

    Input:
        inputFilePath: path to image to be converted 
        outputFilePath: location to save converted image, with new filename
        min*: Hounsfield unit value to map to 0 (integer), * refers to color channel (RGB)
        max*: Hounsfield unit value to map to 255 (integer), * refers to color channel (RGB)
    '''

    HUImage = cv2.imread(inputFilePath, -1)
    HUImage = HUImage.astype(np.int16)

    red = v_map_HU_to_RGB(HUImage, minR, maxR)
    green = v_map_HU_to_RGB(HUImage, minG, maxG)
    blue = v_map_HU_to_RGB(HUImage, minB, maxB)

    RGBImage = np.stack((blue, green, red), axis=-1) # opencv expects blue first

    # print(RGBImage.shape)
    # print(RGBImage.dtype)
    # print(type(RGBImage))

    cv2.imwrite(outputFilePath, RGBImage, [int(cv2.IMWRITE_JPEG_QUALITY), 100]) 


# set HU color ranges
#minR, maxR, minG, maxG, minB, maxB = -1400, -950, -1400, -200, -160, 240
#minR, maxR, minG, maxG, minB, maxB = -1400, -853, -852, -306, -305, 240
#minR, maxR, minG, maxG, minB, maxB = -1000, -600, -601, -200, -201, 200
minR, maxR, minG, maxG, minB, maxB = -1000, 200, -1000, 200, -1000, 200 

# convert a single image
#inputFilePath = '../ILD_medgift/ILD_DB_talismanTestSuite/emphysema_patch1000_patient-1_7.tif'
#outputFilePath = './even-split_-1000to200.jpg'
#convert_image(inputFilePath, outputFilePath, minR, maxR, minG, maxG, minB, maxB)

# convert a directory
inputDir = './ILD_DB_talismanTestSuite/'
outputDir = './converted/'
if not os.path.exists(outputDir):
    os.makedirs(outputDir)
fileNames = os.listdir(inputDir)
print("R: [", minR, ", ", maxR, "] HU -> [0, 255]", sep='')
print("G: [", minG, ", ", maxG, "] HU -> [0, 255]", sep='')
print("B: [", minB, ", ", maxB, "] HU -> [0, 255]", sep='')
print("Converting images to RGB...")
for fileName in fileNames:
    if fileName.endswith(".tif"):
        inputFilePath = inputDir + fileName
        outputFilePath = outputDir + os.path.splitext(fileName)[0] + ".jpg"
        convert_image(inputFilePath, outputFilePath, minR, maxR, minG, maxG, minB, maxB)
print("Done! Converted images saved to", outputDir)
