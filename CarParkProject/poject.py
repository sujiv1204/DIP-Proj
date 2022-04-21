import cv2
import pickle
import cvzone
import numpy as np

# Video feed
cap = cv2.VideoCapture("car_test.mp4")

# with open("CarParkPos", "rb") as f:
#     posList = pickle.load(f)

# width, height = 107, 48

try:
    with open('CarParkPos', 'rb') as f:
        top_left = pickle.load(f)
        bottom_right = pickle.load(f)
except:
    top_left = []
    bottom_right = []

# print(top_left, bottom_right)
def checkParkingSpace(imgPro):
    spaceCounter = 0

    for i in range(len(top_left)):

        imgCrop = imgPro[top_left[i][1]: bottom_right[i][1], top_left[i][0]: bottom_right[i][0]]
        # cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, top_left[i], bottom_right[i], color, thickness)
        cvzone.putTextRect(
            img,
            str(count),
            (top_left[i][0], bottom_right[i][1] - 3),
            scale=1,
            thickness=2,
            offset=0,
            colorR=color,
        )

    cvzone.putTextRect(
        img,
        f"Free: {spaceCounter}/{len(top_left)}",
        (100, 50),
        scale=3,
        thickness=5,
        offset=20,
        colorR=(0, 200, 0),
    )

# def display(img):
#     cv2.imshow(img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    # display(imgBlur)

    imgThreshold = cv2.adaptiveThreshold(
        imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16
    )
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    # display(imgMedian)


    kernel = np.ones((3, 3), np.uint8)
    # display(imgMedian)

    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    # display(imgDilate)

    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    cv2.waitKey(500)
