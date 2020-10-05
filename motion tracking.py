from directkey import PressKey, UP, DOWN, LEFT, RIGHT, ReleaseKey
import cv2

# Lets make initital conditions:
ARROW_LEFT = False
ARROW_RIGHT = False
ARROW_UP = False
ARROW_DOWN = False

cap = cv2.VideoCapture(0)
for i in range(60):
    status, img = cap.read()
    img = cv2.flip(img, 1)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
res = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5)
for (x, y, w, h) in res:
    x_init = x
    y_init = y
    w_init = w
    h_init = h
# res has the initial positions of the head in the format (x,y,w,h)
# pt1 ==> (x,y)   pt2 ==> (x+w,y)   pt3 ==> (x,y+h)   pt4 ==> (x+w,y+h)

# Lets make a threshold for the y-axis:
threshold = 40
threshold_y = 40

while cap.isOpened():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    dim = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=5)
    # dim has the current positions of head in the format (x,y,w,h)
    for (x, y, w, h) in dim:
        x_current = x
        y_current = y
        w_current = w
        h_current = h
    cv2.line(frame, (x_init, (2 * y_init + h_init) // 2), (x_init + w_init, (2 * y_init + h_init) // 2), (0, 0, 255),
             thickness=1)
    cv2.line(frame, ((2 * x_init + w_init) // 2, y_init), ((2 * x_init + w_init) // 2, y_init + h_init), (0, 0, 255),
             thickness=1)
    cv2.rectangle(frame, (x_current, y_current), (x_current + w_current, y_current + h_current), (0, 255, 0),
                  thickness=1)
    if (y_current - y_init > threshold_y) and (ARROW_DOWN == False):
        PressKey(DOWN)
        ReleaseKey(DOWN)
        ARROW_DOWN = True
        print("DOWN")

    if (y_init - y_current > threshold_y) and (ARROW_UP == False):
        PressKey(UP)
        ReleaseKey(UP)
        ARROW_UP = True
        print("UP")

    if (x_current - x_init > threshold) and (ARROW_RIGHT == False):
        PressKey(RIGHT)
        ReleaseKey(RIGHT)
        ARROW_RIGHT = True
        print("Right")

    if (x_init - x_current > threshold) and (ARROW_LEFT == False):
        PressKey(LEFT)
        ReleaseKey(LEFT)
        ARROW_LEFT = True
        print("Left")

    if ARROW_UP == True or ARROW_DOWN == True or ARROW_LEFT == True or ARROW_RIGHT == True:
        x_init = x_current
        if ARROW_UP:
            ARROW_UP = False
        if ARROW_RIGHT:
            ARROW_RIGHT = False
        if ARROW_LEFT:
            ARROW_LEFT = False
        if ARROW_DOWN:
            ARROW_DOWN = False

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()
