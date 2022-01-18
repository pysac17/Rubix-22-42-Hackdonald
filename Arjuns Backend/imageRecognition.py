from operator import truediv
import cv2
import pytesseract
import numpy as np
from pytesseract import Output
import re
import datetime

current_time = datetime.datetime.now()

image = cv2.imread('Letest.jpg')

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 

gray = get_grayscale(image)
thresh = thresholding(gray)
opening1 = opening(gray)
canny1 = canny(gray)

custom_config = r'--oem 3 --psm 6'
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


d = pytesseract.image_to_data(canny1, output_type=Output.DICT)

date_pattern = '^([0-9]|0[1-9]|[12][0-9]|3[01])/([0-9]|0[1-9]|1[012])/(2019|202[0-9]|19|2[0-9])\d\d$'

dates=["", ""]
j=0
single_date=False

n_boxes = len(d['text'])

for i in range(n_boxes):
    if float(d['conf'][i]) > 60.0:
        if re.match(date_pattern, d['text'][i]):
           dates[j]=d['text'][i]
           j=j+1

if j==1:
    dates[1]=str(current_time.day)+'/'+str(current_time.month)+'/'+str(current_time.year)
    single_date = True


dates_split=[dates[0].split('/'), dates[1].split('/')]

first_exp = False

if int(dates_split[0][2])>int(dates_split[1][2]):
    first_exp = True
elif int(dates_split[0][1])>int(dates_split[1][1]) and int(dates_split[0][2])==int(dates_split[1][2]):
    first_exp = True
else:
    first_exp = False

expiry=""


def bestbefore(mdate):
    premonths = int(mdate[2])*12 + int(mdate[1])
    b = ""
    for a in range(n_boxes):
        if float(d['conf'][a]) > 60.0:
            if d['text'][a].isnumeric() and d['text'][a-2].lower() == "best" and d['text'][a-1] == "before":
                b = d['text'][a]
                break
    totalmonths = premonths + int(b)
    year = int(totalmonths/12)
    mont = totalmonths%12
    day = int(mdate[0])
    expd = str(day)+'/'+str(mont)+'/'+str(year)
    return expd

if first_exp == False and single_date == True:
    expiry=bestbefore(dates_split[0])
elif first_exp:
    expiry=dates[0]
else:
    expiry=dates[1]

print(expiry)