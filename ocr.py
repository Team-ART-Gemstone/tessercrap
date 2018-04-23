# COMMANDS TO RUN:
# python ocr.py --image images/example_01.png 
# python ocr.py --image images/example_02.png  --preprocess blur
# python ocr.py --image images/example_03.png

from PIL import Image # allows us to load out image input in PIL format (required for pytesseract)
import pytesseract
import argparse
import cv2
import os





# GETTING INPUT AND SHIT

# parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing to be done")
args = vars(ap.parse_args())

# load image and convert to grayscale (preprocessing)
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow("Image", gray)





# PREPROCESSING SHIT

# check to see if we should apply thresholding (preprocess)
# thresholding will try to separate the foreground from the background
# THRESH_BINARY will threshold into 
if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# check to see if median blurring should be done to remove noise (preprocessing)
# median blur will help differentiate foreground text from "salt and peppery" backgrounds (ex. image2)
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)




# APPLYING OCR SHIT

# save grayscale image as a temporary file to apply OCR later
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# load image as a PIL/Pillow image, apply OCR, and then delete temporary file
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(text) # wtites text output from pytesseract to terminal

# show the output images
# cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)