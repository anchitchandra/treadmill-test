import cv2

count = 0
cap = cv2.VideoCapture('D:/downloads new/treadmill.mp4')  # file location

ret, frame1 = cap.read()
ret, frame2 = cap.read()

writer = cv2.VideoWriter("output2.mp4",
                         cv2.VideoWriter_fourcc(*"XVID"), 30, (640, 480))
while cap.isOpened():
    try:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thres = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thres, None, iterations=1)
        cv2.line(frame1, (0, 300), (700, 300), (0, 0, 255), 1)
        counturs, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(frame1, counturs, -1, (255, 0, 0), 2)
        for countur in counturs:
            (x, y, w, h) = cv2.boundingRect(countur)
            if cv2.contourArea(countur) < 3000:
                continue
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            xmid = (x + (x + w)) // 2
            ymid = (y + (y + h)) // 2
            cv2.circle(frame1, (xmid, ymid), 4, (255, 0, 0), 4)

            if 300 < ymid < 306:
                count += 1

        writer.write(cv2.resize(frame1, (640, 480)))
        # cv2.imshow("Treadmill exp", frame1)
        frame1 = frame2

        ret, frame2 = cap.read()
        cv2.putText(frame1, f"Objects: {count}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 3)
    except:break

cv2.destroyAllWindows()
cap.release()
