"""
Returns N most prominant colors in image 

"""
import cv2
import numpy as np
import GetAlbums
from PIL import Image

# in OpenCV, Hue range is [0,179], saturation range is [0,255], and value range is [0,255]

# cv2 k-means clustering algorithm:
def domColor(img, n_colors): # https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
    
    pixels = np.float32(img.reshape(-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]
    return dominant, palette 


def insertSort(sortedImgs, entry):
    # insertion sort array of type [["banana", 10], ["currents", 30], ["inner", 5], ["meta", 7], ["orc", 1], ["poly", 67]]
    placed = False
    if sortedImgs == []:
        sortedImgs.append(entry)
    else:
        for i in range(0, len(sortedImgs)):
            if entry[1] <= sortedImgs[i][1]:
                sortedImgs.insert(i, entry)
                placed = True
                break
        if not placed:
            sortedImgs.append(entry)
        
    return sortedImgs

def sortImg(sortedImgs, dom_img, path, ext, name):
    # Get Hue of dom_img, make entry:
    dom_img = cv2.cvtColor(dom_img, cv2.COLOR_BGR2HSV)
    hue = dom_img[0,0,0]
    entry = [name, hue] 
    # Insert sort by hue:
    sortedImgs = insertSort(sortedImgs, entry)
    return sortedImgs

def get_average(image):
    img = Image.open("images/" + image + ".jpg")
    r,g,b = 0,0,0
    width, height = img.size
    size = width * height
    pixel_values = list(img.getdata())
    for x in range(width):
        for y in range(height):
            r += pixel_values[width * y + x][0]
            g += pixel_values[width * y + x][1]
            b += pixel_values[width * y + x][2]
    r //= size
    g //= size
    b //= size
    return r,g,b


def main():
    path = "images/"
    ext = ".jpg"
    imList = GetAlbums.get_albums()

    n_colors = 2 # Number of dominant colors to search for
    n_bins = 6 # Number of colors to sort dominant into

    sortedImgs = [] # [[name, hue], [name, hue], ...]
    sortedImgsB = []
    for name in imList:
        print(path + name + ext)
        img = cv2.imread(path + name + ext)
        
        # Get "n_colors" most dominant RGB values 
        dominant, palette = domColor(img, n_colors)
        #dominant = get_average(name)
        # Get pure dominant color image:
        dom_img = img 
        dom_img[0:dom_img.shape[0],0:dom_img.shape[1]] = dominant

        # Insert image name and hue into sortedImgs
        sortedImgs = sortImg(sortedImgs, dom_img, path, ext, name)

    # Fill sorted folder:
    for i in range(0, len(sortedImgs)):
        entry = sortedImgs[i]
        img = cv2.imread(path + entry[0] + ext)
        cv2.imwrite("sorted/" + str(i) + "_" + entry[0] + ext, img)
        
    return 0

main()
