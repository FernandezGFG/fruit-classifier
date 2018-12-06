import numpy as np
from skimage import color, filters
from skimage.feature import hog

import cv2
import mahotas


# Conversión de imagen a escala de grises
def img2grey(image, mode='sk'):
    if (mode == 'sk'):
        gray = color.rgb2gray(image)
    elif (mode == 'cv'):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


# Normalización del tamaño de la imagen
def normSize(image, size=(tuple((100, 100)))):
    image = cv2.resize(image, size)
    return image


# Filtrado de imagen con filtro gaussiano
def imgClean(image, sigma=1, mode='cv'):
    if (mode == 'cv'):
        clean = cv2.GaussianBlur(image, (3, 3), 0)
    else:
        clean = filters.gaussian(image, sigma)
    return clean


# Detección de bordes con filtro sobel
def imgEdge(image, sigma=1):
    aux = imgClean(image, sigma)
    edge = filters.sobel(aux)
    return edge


# Extracción de características Hu Moments
def hu_moments(image):
    feature = cv2.HuMoments(cv2.moments(image)).flatten()
    return feature


# Extracción de características Haralick Textures
def haralick(image):
    feature = mahotas.features.haralick(image).mean(axis=0)
    return feature


def color_histogram(image, mask=None, bins=8):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([image], [0, 1, 2], None, [bins, bins, bins],
                        [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    feature = hist.flatten()
    return feature


def m_hog(image):
    feature = hog(image).ravel()
    return feature


def ft_extract(image):
    image = normSize(image)
    aux = img2grey(image, mode='cv')
    aux = imgClean(aux, mode='cv')

    # image_fht = haralick(aux)
    # image_fhm = hu_moments(aux)
    image_fch = color_histogram(image)
    # image_fhog = m_hog(aux)

    # feature = np.hstack([image_fht, image_fhm, image_fhog])
    feature = image_fch
    feature = feature.reshape(1, -1)

    # COLOR HISTOGRAM
    sum = 0
    for m in feature[0]:
        sum += m
    med = sum / len(feature[0])
    sum = 0
    for m in feature[0]:
        sum += np.power((m - med), 2)
    dstd = np.sqrt(sum / (len(feature[0]) - 1))
    feature = [med, dstd]

    return aux, feature


# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='',
                     decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of
    decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = (
        "{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


class Elemento():
    def __init__(self):
        self.label = None
        self.image = None
        self.feature = []
        self.distance = 0
