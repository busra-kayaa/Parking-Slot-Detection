# Otopark Boş Alan Tespiti

import cv2
import pickle
import numpy as np

cap = cv2.VideoCapture("video.mp4")

def check(frame1):

    spaceCounter = 0
    for pos in liste:
        x, y = pos

        crop = frame1[y: y+15, x: x+26]
        count = cv2.countNonZero(crop)
        # print("count", count)

        if count < 150:
            color = (0, 255, 0)
            spaceCounter = spaceCounter+1
        else:
            color = (0, 0, 255)

        cv2.rectangle(frame, pos, (pos[0]+26, pos[1]+15), color, 2)
    cv2.putText(frame, f"bos: {spaceCounter}/{len(liste)}", (15, 350), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 4)


with open("carparkpos", "rb") as f:
    liste = pickle.load(f)

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1) # gürültü azaltmak ve yumuşatmak
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    median = cv2.medianBlur(thresh, 5) # tuz biber gürültüyü azaltır
    dilates = cv2.dilate(median, np.ones((3, 3)), iterations=1)

    check(dilates)

    cv2.imshow("orj", frame)
    #cv2.imshow("gri", gray)
    #cv2.imshow("blur", blur)
    #cv2.imshow("thresh", thresh)
    #cv2.imshow("median", median)
    #cv2.imshow("dilates", dilates)

    if cv2.waitKey(200) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()