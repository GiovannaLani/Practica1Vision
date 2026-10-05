import cv2

drawing = False
points = []

def onMouse(event, x, y, flags, param):
    global drawing, start_point, end_point, frame
    if event == cv2.EVENT_LBUTTONUP:
        
        points.append((x,y))
        
        if len(points) > 1:
            cv2.line(frame, points[len(points) - 2], points[len(points) - 1], (255, 0, 0), 3)
            if len(points) == 4:
                cv2.line(frame, points[len(points) - 1], points[0], (255, 0, 0), 3)
                points.clear()
        

videoCapture = cv2.VideoCapture("Video Práctica.mp4")
size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fps = videoCapture.get(cv2.CAP_PROP_FPS)

videoWriter = cv2.VideoWriter( 'MyOutputVid.avi', cv2.VideoWriter_fourcc('I','4','2','0'), fps, size)

cv2.namedWindow('MyWindow')
cv2.setMouseCallback('MyWindow', onMouse)

success, frame = videoCapture.read()
frame_num = 1
total_frames = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))

while success:
    key = cv2.waitKey(1) & 0xFF
    cv2.putText(frame, f'{frame_num} / {total_frames}', (size[0] - 140, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    if key == 32: #Tecla espacio
        frame_num += 1
        if (frame_num > total_frames): 
            break
        videoWriter.write(frame)
        success, frame = videoCapture.read()
        points.clear()
    if key == 100: #Tecla D
        frame_num += 20
        if (frame_num > total_frames): 
            break
        videoCapture.set(cv2.CAP_PROP_POS_FRAMES, frame_num - 1)
        videoWriter.write(frame)
        success, frame = videoCapture.read()
        points.clear()
        
    elif key == 113: #Tecla Q
        break
    
    
    cv2.imshow('MyWindow', frame)

cv2.destroyWindow('MyWindow')
videoCapture.release()