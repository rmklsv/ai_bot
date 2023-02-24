import cv2
import pytesseract

def text_recognition(image) -> str:
    try:
        image = cv2.imread('image.png')
        text = pytesseract.image_to_string(image)
        return text
    except:
        return 'Failed to recognize, please send another image.'




