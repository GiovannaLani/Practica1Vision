import cv2

drawing = False
points = []
figures =[]

def onMouse(event, x, y, flags, param):
    global drawing, start_point, end_point, frame, figures, points
    if event == cv2.EVENT_LBUTTONUP:
        
        points.append((x,y))
        
        if len(points) > 1:
            cv2.line(frame, points[len(points) - 2], points[len(points) - 1], (255, 0, 0), 3)
            if len(points) == 4:
                cv2.line(frame, points[len(points) - 1], points[0], (255, 0, 0), 3)
                figures.append(points.copy())
                print(figures)
                points.clear()
        
def draw_figure(points, frame):
    for i in range(len(points)):
        cv2.line(frame, points[i], points[(i+1)%len(points)], (255, 0, 0), 3)


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

    if key == 32: #Tecla espacio
        frame_num += 1
        if (frame_num > total_frames): 
            break
        videoWriter.write(frame)
        success, frame = videoCapture.read()
        points.clear()
        figures.clear()
    if key == 100: #Tecla D
        for i in range(20):
            frame_num += 1
            if (frame_num > total_frames): 
                break
            for figure in figures:
                draw_figure(figure, frame)
            videoWriter.write(frame)
            success, frame = videoCapture.read()

        
        if (frame_num > total_frames): 
            break      
        points.clear()
        figures.clear()
    elif key == 113: #Tecla Q
        break
    
    frame_ui = frame.copy()
    cv2.putText(frame_ui, f'{frame_num} / {total_frames}', (size[0] - 140, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.imshow('MyWindow', frame_ui)

cv2.destroyWindow('MyWindow')
videoCapture.release()