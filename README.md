# Talisman Test Suite Image Processing
Convert and categorize Talisman Test Suite images.
Requires Python3, OpenCV, and Numpy.

The Talisman Test Suite consists of CT scan patches of Interstitial Lung Disease(ILD).
The patches are saved as 16 bit tiffs and use Hounsfield Units(HU).

### Convert HU to RGB
In HUtoRGB.py set the following variables to the HU values you want to correspond to each RGB color channel:
```
minR, maxR, minG, maxG, minB, maxB
```

The converted images are saved as jpgs in a new directory. The input and output directory paths can be changed from their defaults:
```
inputDir = './ILD_DB_talismanTestSuite/'
outputDir = './converted/'
```

### Categorize by Disease
After running HUtoRGB.py, place and run catagorize.sh in the new 'converted' directory. 
The images will be moved to subdirectories with disease names.

