import cv2
import math

drawing = False
points = []
figures =[]

selectedPoint = -1
selectedFigure = None

def onMouse(event, x, y, flags, param):
    global drawing, frame, figures, points, selectedFigure, selectedPoint
    


    if event == cv2.EVENT_LBUTTONUP:
        if len(points) == 0:
            points.append((x, y))
        else:
            if len(points) > 1 and math.sqrt((x - points[0][0]) ** 2 + (y - points[0][1]) ** 2) < 10:
                figures.append(points.copy())
                points.clear()
            else:
                points.append((x, y))


        
        
    if event == cv2.EVENT_RBUTTONDOWN:
        for figure in figures:
            for i, point in enumerate(figure):
                if math.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2) < 10: #TODO
                    selectedFigure = figure
                    selectedPoint = i

    if event == cv2.EVENT_RBUTTONUP:
        selectedFigure = None
        selectedPoint = -1

    if event == cv2.EVENT_MOUSEMOVE:
        if selectedPoint != -1:
            selectedFigure[selectedPoint] = (x,y)


def changeFrame():
    global frame, frame_num
    outputFrame = frame.copy()
    for figure in figures:
        drawFigure(figure, outputFrame)
    videoWriter.write(outputFrame)
    frame_num += 1
    if (frame_num > total_frames): 
        return False
    success, frame = videoCapture.read()
    points.clear()
    return True

        
def drawFigure(points, frame):
    for i in range(len(points)):
        cv2.circle(frame, points[i], 1, (255, 0, 0), 20)
        cv2.line(frame, points[i], points[(i+1)%len(points)], (255, 0, 0), 3)

def drawPoints(points, frame):
    for i in range(len(points)):
        cv2.circle(frame, points[i], 1, (255, 0, 0), 20)
        if i != len(points)-1:
            cv2.line(frame, points[i], points[(i+1)], (255, 0, 0), 3)


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
        if not changeFrame():
            break

    if key == 100: #Tecla D
        for i in range(20):
            if not changeFrame():
                break
        
        if frame_num > total_frames: 
            break      

    elif key == 113: #Tecla Q
        break
    
    frame_ui = frame.copy()

    drawPoints(points, frame_ui)
    for figure in figures:
        drawFigure(figure, frame_ui)

    cv2.putText(frame_ui, f'{frame_num} / {total_frames}', (size[0] - 140, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    

    cv2.imshow('MyWindow', frame_ui)

cv2.destroyWindow('MyWindow')
videoCapture.release()