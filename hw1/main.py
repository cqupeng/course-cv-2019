# -*- coding: utf-8 -*-

import numpy as np
import cv2
import datetime
from PIL import Image

if __name__ == "__main__":

    cameraCapture = cv2.VideoCapture(0)
    cv2.namedWindow('MyWindow')
    print("Show camera feed.Click window or press ans key to stop")
    success, frame = cameraCapture.read()
    timeFormat = '%Y-%m-%d %H:%M:%S'
    myImg = Image.open("img.png").resize((200, 200), Image.ANTIALIAS)

    fps = 30
    size = (int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    videoWriter = cv2.VideoWriter('testVideros.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)

    pauseFlag = True
    pauseImage = Image.open("pause.png")
    startImage = Image.open("start.png")

    drawing = False
    ix, iy = -1, -1

    lineXY = []
    tempLineXY = []


    def draw_circle(event, x, y, flags, param):
        global ix, iy, drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y
            tempLineXY.append((x, y))
        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            tempLineXY.append((x, y))
        elif event == cv2.EVENT_LBUTTONUP:
            lineXY.append(tempLineXY.copy())
            tempLineXY.clear()
            drawing = False


    while success and cv2.waitKey(1) & 0xFF != ord('q'):
        cv2.setMouseCallback('MyWindow', draw_circle)

        cv2.imshow('MyWindow', frame)
        success, frame = cameraCapture.read()
        for i in range(len(tempLineXY)):
            if i != 0:
                cv2.line(frame, tempLineXY[i - 1], tempLineXY[i], (0, 0, 255), 5)
        for xyList in lineXY:
            for i in range(len(xyList)):
                if i != 0:
                    cv2.line(frame, xyList[i - 1], xyList[i], (0, 0, 255), 5)
        tempTime = datetime.datetime.now().strftime(timeFormat)
        cv2.putText(frame, tempTime, (400, 50), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)
        cv2.putText(frame, "name: Shiyuan Peng", (400, 100), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)
        cv2.putText(frame, "StudentID: 21921216", (400, 150), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        layer.paste(myImg, (image.size[0] - 200, image.size[1] - 700))
        if cv2.waitKey(1) & 0xFF == ord(' '):
            if pauseFlag:
                pauseFlag = False
            else:
                pauseFlag = True
        if pauseFlag:
            layer.paste(pauseImage, (int(image.size[0] / 2), int(image.size[1] * 2 / 3)))
            out = Image.composite(layer, image, layer)
            frame = cv2.cvtColor(np.asarray(out), cv2.COLOR_RGB2BGR)
        else:
            layer.paste(startImage, (int(image.size[0] / 2), int(image.size[1] * 2 / 3)))
            out = Image.composite(layer, image, layer)
            frame = cv2.cvtColor(np.asarray(out), cv2.COLOR_RGB2BGR)
            videoWriter.write(frame)
    cv2.destroyAllWindows()
    cameraCapture.release()
