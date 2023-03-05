import cv2
import pytesseract

#Path to the tesseract OCR app
pytesseract.pytesseract.tesseract_cmd = "tesseract\\tesseract.exe"

#Define the text recognition function
def text_recognition(img) -> str:
    pre_img = cv2.imread(img)
    pre_img = cv2.cvtColor(pre_img, cv2.COLOR_BGR2RGB) #Conversion to the necessary format
    
    text = pytesseract.image_to_string(pre_img, lang = "eng+rus")
    
    #Processing List(str) into str
    resultString = ''
    for item in text:
        resultString += item
        
    return resultString

def show_text_on_img(img):
    pre_img = cv2.imread(img)
    pre_img = cv2.cvtColor(pre_img, cv2.COLOR_BGR2RGB) #Conversion to the necessary format
    
    data = pytesseract.image_to_data(pre_img, lang = "eng+rus")
    
    for i, el, in enumerate(data.splitlines()):
        if i == 0:
            continue
        
        el = el.split()
        try:
            x, y= int(el[6]), int(el[7])
            cv2.putText(pre_img, el[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0), 1)
        except IndexError:
            print ('Skiped')
        
    cv2.imshow('Result', pre_img)
    cv2.waitKey(0)

if __name__ == "__main__":
    print (show_text_on_img('img2.jpg'))
