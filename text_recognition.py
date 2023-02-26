import cv2
import pytesseract

#Path to the tesseract OCR app
pytesseract.pytesseract.tesseract_cmd = "tesseract\\tesseract.exe"

#Define the text recognition function
def text_recognition(img) -> str:
    pre_img = cv2.imread(img)
    pre_img = cv2.cvtColor(pre_img, cv2.COLOR_BGR2RGB) #Conversion to the necessary format
    
    recognitionConfig = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(pre_img, lang = "eng+rus", config = recognitionConfig)
    
    #Processing List(str) into str
    resultString = ''
    for item in text:
        resultString += item
        
    return resultString
