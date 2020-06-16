import cv2
import numpy as np
import matplotlib.pyplot as plt

def mostra_fig(img, title=None, ticks=False):
    if len(img.shape) < 3:
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    else:
        plt.imshow(img[:,:,::-1])
    
    if not ticks:
        plt.yticks([])
        plt.xticks([])
    
    if title is not None: plt.title(title)
    plt.show()

#imagem para scan
img = cv2.imread("imgCovid.png")
img = img[5:270, 10:400]

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (0, 0, 70), (179, 255, 224))
elem = np.ones([5,5])

mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, elem)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, elem)

contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

maior_area = 300
contorno_maior_area = []

for contorno in contours:
    area = cv2.contourArea(contorno)
    if area > maior_area:
        contorno_maior_area.append(contorno)

for contorno in contorno_maior_area:
    areaPixel = cv2.contourArea(contorno)
    print("Área da doença: ", areaPixel, " pixels")
    cv2.drawContours(img, [contorno], contourIdx=0, color=(0,255,0))
    centro_x = contorno[:,:,0].mean()
    centro_y = contorno[:,:,1].mean() 

plt.figure(figsize=(10,10))
mostra_fig(img)
