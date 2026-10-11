import cv2
import math

drawing = False
points = []
figures =[]

selectedPoint = -1
selectedFigure = None

keyFrames = {}

def onMouse(event, x, y, flags, param):
    global drawing, frame, figures, points, selectedFigure, selectedPoint

    if event == cv2.EVENT_LBUTTONUP:
        if len(points) == 0:
            points.append((x, y))
        else:
            if len(points) > 1 and math.sqrt((x - points[0][0]) ** 2 + (y - points[0][1]) ** 2) < 10:
                figures.append(points.copy())
                saveKeyFrame(1)
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
        saveKeyFrame(frame_num)
        selectedFigure = None
        selectedPoint = -1

    if event == cv2.EVENT_MOUSEMOVE:
        if selectedPoint != -1:
            selectedFigure[selectedPoint] = (x,y)

def changeFrame(step):
    global frame, frame_num, figures, success

    frame_num += step
    videoCapture.set(cv2.CAP_PROP_POS_FRAMES, frame_num - 1)

    if frame_num > total_frames: 
        frame_num = total_frames
        return
    elif frame_num < 1:
        frame_num = 1
        return

    success, frame = videoCapture.read()
    points.clear()
    
    interpolated = getFiguresAtFrame(frame_num)
    figures = [figure.copy() for figure in interpolated]
    return True

        
def drawFigure(points, frame):
    for i in range(len(points)):
        cv2.circle(frame, points[i], 1, (255, 0, 0), 20)
        cv2.line(frame, points[i], points[(i+1)%len(points)], (255, 0, 0), 3)

def drawPoints(points, frame):
    for i in range(len(points)):
        cv2.circle(frame, points[i], 1, (0, 255, 0), 20)
        if i != len(points)-1:
            cv2.line(frame, points[i], points[(i+1)], (0, 255, 0), 3)

def saveKeyFrame(frame_num):
    global keyFrames, figures
    keyFrames[frame_num] = [figure.copy() for figure in figures]

def getFiguresAtFrame(frame_num):
    if not keyFrames:
        return []
    
    sortedFrames = sorted(keyFrames.keys())
    if frame_num in keyFrames:
        return keyFrames[frame_num]
    elif frame_num < sortedFrames[0]:
        return keyFrames[sortedFrames[0]]
    elif frame_num > sortedFrames[len(sortedFrames) - 1]:
        return keyFrames[sortedFrames[len(sortedFrames) - 1]]
    else:
        for i in range(len(sortedFrames) - 1):
            if sortedFrames[i] < frame_num < sortedFrames[i + 1]:
                prevFrame = sortedFrames[i]
                nextFrame = sortedFrames[i + 1]
                break

        prevFigures = keyFrames[prevFrame]
        nextFigures = keyFrames[nextFrame]

        interpolatedFigures = []
        for j in range(len(prevFigures)):
            prevFigure = prevFigures[j]
            nextFigure = nextFigures[j]
            interpolatedFigure = []
            for k in range(len(prevFigure)):
                x1, y1 = prevFigure[k]
                x2, y2 = nextFigure[k]
                t = (frame_num - prevFrame) / (nextFrame - prevFrame)
                x_interp = int(x1 + (x2 - x1) * t)
                y_interp = int(y1 + (y2 - y1) * t)
                interpolatedFigure.append((x_interp, y_interp))
            interpolatedFigures.append(interpolatedFigure)

        return interpolatedFigures

def generateVideo():
    videoCapture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    videoWriter = cv2.VideoWriter( 'MyOutputVid.avi', cv2.VideoWriter_fourcc('I','4','2','0'), fps, size)

    frame_num = 1
    success, frame = videoCapture.read()

    while success:

        interpolated = getFiguresAtFrame(frame_num)
        for figure in interpolated:
            drawFigure(figure, frame)
        
        videoWriter.write(frame)
        frame_num += 1
        success, frame = videoCapture.read()


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

    frame_ui = frame.copy()

    drawPoints(points, frame_ui)
    for figure in figures:
        drawFigure(figure, frame_ui)

    cv2.putText(frame_ui, f'{frame_num} / {total_frames}', (size[0] - 140, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    cv2.imshow('MyWindow', frame_ui)


    key = cv2.waitKey(1) & 0xFF  

    if key == ord('d'):
        changeFrame(1)

    if key == ord('f'):
        changeFrame(int(fps))
           
    if key == ord('s'):
        changeFrame(-1)

    if key == ord('a'):
        changeFrame(int(-fps))

    elif key == ord('q'):
        break

    elif key == ord('g'):
        generateVideo()

cv2.destroyWindow('MyWindow')
videoCapture.release()

