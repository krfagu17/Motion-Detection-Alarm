import cv2
import imutils as mu
import threading
import winsound

cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
address="http://192.168.33.16:8080/video"
cap.open(address)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
_, start_frame=cap.read()
start_frame=mu.resize(start_frame, width=500)
start_frame=cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame=cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm=False
alarm_thread=False
alarm_Counter=0

def alarm_sound():
    global alarm
    for _ in range(5):
        if not alarm_thread:
            break
        print("Alarm")
        winsound.Beep(1000, 1000)
    alarm=False

while True:
    _, frame=cap.read()
    frame=mu.resize(frame, width=500)

    if alarm_thread:
        frame_bw=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw=cv2.GaussianBlur(frame_bw, (21, 21), 0)

        difference=cv2.absdiff(frame_bw, start_frame)
        threshold=cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame=frame_bw

        if threshold.sum()>=300:
            alarm_Counter +=1
        else:
            if alarm_Counter>0:
                alarm_Counter -=1
        cv2.imshow("Camera", threshold)
    else:
        cv2.imshow("Camera", frame)
    if alarm_Counter>20:
        if not alarm:
            alarm=True
            threading.Thread(target=alarm_sound).start()

    key=cv2.waitKey(30)
    if key==ord("t"):
        alarm_thread=not alarm_thread
        alarm_Counter=0
    if key==ord("q"):
        alarm_thread=False
        break

cap.release()
cv2.destroyAllWindows()

    
            

