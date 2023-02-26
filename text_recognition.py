import cv2
import pytesseract

#Path to the tesseract OCR app
pytesseract.pytesseract.tesseract_cmd = "tesseract\\tesseract.exe"

# Define the text recognition function
def text_recognition(img) -> str:
    pre_img = cv2.imread(img)
    text = pytesseract.image_to_string(pre_img)
    return text






