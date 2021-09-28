import cv2
# import Open CV library
from cvzone.HandTrackingModule import HandDetector
from time import sleep
# from pynput.keyboard import Controller

# Create Video Object
cap = cv2.VideoCapture(0)
# Set parameter 3 -> 'width' to 1280 and 4 -> 'height' to 720
# For HD resolution (not vga) and accommodating keyboard on screen
cap.set(3, 1280)
cap.set(4, 720)
# instantiate detector, set detection confidence high
detector = HandDetector(detectionCon=0.8, maxHands=2)

# List with set of keys.
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
    [" "]
]

finalText = ""

# keyboard = Controller()


# Function to draw the keys over captured image.
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        if button.text != " ":
            button_start = button.pos
            button_end = (x + w, y + h)
            text = button.text
            text_pos = (x + 20, y + 65)
            img = draw(img, button_start, button_end, text, text_pos)

        if button.text == " ":
            button_start = button.pos
            button_end = (x + 5 * w, y + h)
            text = "SPACE"
            text_pos = (x + 80, y + 65)
            img = draw(img, button_start, button_end, text, text_pos)

    return img


def draw(img, button_start, button_end, text, text_pos):
    cv2.rectangle(img, button_start, button_end, (255, 0, 255), cv2.FILLED)
    cv2.putText(img, text, text_pos, cv2.FONT_HERSHEY_PLAIN,
                4, (255, 255, 255), 4)
    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 100, 100 * i + 50], key))

# Capture image from camera
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    img = drawAll(img, buttonList)

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        centrePoint1 = hand1["center"]
        handType1 = hand1["type"]

        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if button.text != " ":
                if x < lmList1[8][0] < x+w and y < lmList1[8][1] < y+h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                                4, (255, 255, 255), 4)
                    length, _ = detector.findDistance(lmList1[8], lmList1[12])

                    if length < 30:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                                    4, (255, 255, 255), 4)
                        finalText += button.text
                        # keyboard.press(button.text)
                        sleep(0.20)

            if button.text == " ":
                if x < lmList1[8][0] < x+5*w and y < lmList1[8][1] < y+h:
                    cv2.rectangle(img, button.pos, (x + 5 * w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, "SPACE", (x + 80, y + 65), cv2.FONT_HERSHEY_PLAIN,
                                4, (255, 255, 255), 4)
                    length, _ = detector.findDistance(lmList1[8], lmList1[12])

                    if length < 30:
                        cv2.rectangle(img, button.pos, (x + 5 * w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, "SPACE", (x + 80, y + 65), cv2.FONT_HERSHEY_PLAIN,
                                    4, (255, 255, 255), 4)
                        finalText += button.text
                        # keyboard.press(button.text)
                        sleep(0.20)

    if len(finalText) == 12:
        finalText = ""

    cv2.rectangle(img, (100, 550), (750, 650), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (110, 630), cv2.FONT_HERSHEY_PLAIN,
                5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
