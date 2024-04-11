import cv2
import easyocr

class TextRecognizer:
    def __init__(self, search_words):
        self.search_words = search_words
        self.found_word = None

    def recognize_text(self, image):
        reader = easyocr.Reader(['en'], gpu=True)
        result = reader.readtext(image)
        return result

    def find_word(self, frame):
        for detection in self.recognize_text(frame):
            text = detection[1]
            if text in self.search_words:
                self.found_word = text
                return True
        return False

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if self.find_word(frame):
                print("Found word:", self.found_word)
                break

            cv2.imshow('Camera Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
