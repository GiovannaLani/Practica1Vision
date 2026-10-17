import cv2
import figures
import config

def drawPoints(frame, points):
    for i in range(len(points)):
        cv2.circle(frame, points[i], config.POINT_RADIUS, config.COLOR_PENDING, -1)
        if i != len(points)-1:
            cv2.line(frame, points[i], points[i + 1], config.COLOR_PENDING, config.LINE_THICKNESS)

def drawFigure(points, frame, name=""):
    for i in range(len(points)):
        cv2.circle(frame, points[i], config.POINT_RADIUS, config.COLOR_FIGURE, -1)
        cv2.line(frame, points[i], points[(i + 1) % len(points)], config.COLOR_FIGURE, config.LINE_THICKNESS)
 
        x, y = points[0]
        cv2.putText(frame, name, (x, y - 12), cv2.FONT_HERSHEY_SIMPLEX, config.FONT_SCALE_FIGURE, config.COLOR_TEXT_FIGURE, config.FONT_THICKNESS_FIGURE)
 
def drawFigures(frame, figuresDict):
    for figureId, points in figuresDict.items():
        drawFigure(points, frame, figures.getFigureName(figureId))

def changeFrame(currentFrame, step, total_frames, videoCapture, frame):
    targetFrame = min(max(currentFrame + step, 0), total_frames - 1)
    videoCapture.set(cv2.CAP_PROP_POS_FRAMES, targetFrame - 1)
    success, nextFrame = videoCapture.read()
    
    if success:
        frame[:] = nextFrame
        figures.updateFiguresForFrame(targetFrame)
        return targetFrame

def drawActiveFigureInfo(frame, currentFrame):
    figureId = figures.getActiveFigureId()
    if figureId is None:
        return

    state = figures.getFigureStateAtFrame(figureId, currentFrame)
    if state is None:
        status = "No existe"
    elif state[0]:
        status = "visible"
    else:
        status = "oculta"

    if currentFrame in figures.getFigureKeyframes(figureId):
        status += " (KEYFRAME)"

    cv2.putText(frame, f"{figures.getFigureName(figureId)} - {status}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, config.FONT_SCALE, config.COLOR_ACTIVE_FIGURE_TEXT, 2)

def drawFrameCounter(frame, frameIndex, totalFrames):
    text = f"{frameIndex + 1} / {totalFrames}"
    cv2.putText(frame, text, (frame.shape[1] - 90, 20), cv2.FONT_HERSHEY_SIMPLEX, config.FONT_SCALE, config.COLOR_TEXT, 2)

def frameToX(frameIndex, totalFrames, width):
    margin = 20
    return margin + int((width - 2 * margin) * frameIndex / max(totalFrames - 1, 1))

def drawTimeline(frame, currentFrame, totalFrames):
    height, width = frame.shape[:2]
    y = height - 20
    margin = 20

    cv2.line(frame, (0 + margin, y), (width - margin, y), (255,255,255), 6)

    figureId = figures.getActiveFigureId()
    if figureId:
        keyframes = figures.getFigureKeyframes(figureId)
        frameIds = sorted(keyframes.keys())

        for i in range(len(frameIds)):
            startX = frameToX(frameIds[i], totalFrames, width)
            if i + 1 < len(frameIds):
                endX = frameToX(frameIds[i + 1], totalFrames, width)
            else:
                endX = frameToX(totalFrames - 1, totalFrames, width)

            visible = keyframes[frameIds[i]][0]
            color = config.COLOR_TL_VISIBLE if visible else config.COLOR_TL_HIDDEN
            cv2.line(frame, (startX, y), (endX, y), color, 4)

        for frameId in frameIds:
            x = frameToX(frameId, totalFrames, width)
            visible = keyframes[frameId][0]
            color = config.COLOR_TL_VISIBLE if visible else config.COLOR_TL_HIDDEN
            cv2.circle(frame, (x, y), 6, (255, 255, 255), -1)
            cv2.circle(frame, (x, y), 4, color, -1)

    x = frameToX(currentFrame, totalFrames, width)
    cv2.line(frame, (x, y - 10), (x, y + 10), (255, 255, 255), 2)

def createPanel(frame, currentFrame, totalFrames):
    panel = frame[0:config.PANEL_HEIGHT].copy()
    panel[:] = config.COLOR_PANEL

    drawActiveFigureInfo(panel, currentFrame)
    drawFrameCounter(panel, currentFrame, totalFrames)
    drawTimeline(panel, currentFrame, totalFrames)
    return panel