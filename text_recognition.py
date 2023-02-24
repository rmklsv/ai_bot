import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "tesseract\\tesseract.exe"

def text_recognition(image) -> str:
    try:
        image = cv2.imread('image.png')
        tempImage = cv2.cvtColor(tempImage, cv2.COLOR_BGR2RGB)
        tempResult = pytesseract.image_to_string(image, lang = "rus+eng")
        result = ""
        for x in tempResult:
            if x == "": continue
            result += x
        return result
    except:
        return 'Failed to recognize, please send another image.'
