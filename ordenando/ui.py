import cv2
import figures
import config

def drawPoints(frame, points):
    for i in range(len(points)):
        cv2.circle(frame, points[i], config.POINT_RADIUS, config.COLOR_PENDING, -1)
        if i != len(points)-1:
            cv2.line(frame, points[i], points[i + 1], config.COLOR_PENDING, config.LINE_THICKNESS)

def drawFigure(points, frame):
    for i in range(len(points)):
        cv2.circle(frame, points[i], config.POINT_RADIUS, config.COLOR_FIGURE, -1)
        cv2.line(frame, points[i], points[(i + 1) % len(points)], config.COLOR_FIGURE, config.LINE_THICKNESS)

def drawFigures(frame, figuresDict):
    for figureId, points in figuresDict.items():
        drawFigure(points, frame)

def changeFrame(currentFrame, step, total_frames, videoCapture, frame):
    targetFrame = min(max(currentFrame + step, 0), total_frames - 1)
    videoCapture.set(cv2.CAP_PROP_POS_FRAMES, targetFrame - 1)
    success, nextFrame = videoCapture.read()
    
    if success:
        frame[:] = nextFrame
        figures.updateFiguresForFrame(targetFrame)
        return targetFrame