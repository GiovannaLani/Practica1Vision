import cv2
import math
import config

visibleFigures = {}
drawingFigurePoints = []
figuresKeyframes = {}
nextFigureId = 1

selectedFigureId = None
selectedPoint = None
activeFigureId = None

def onMouse(event, x, y, flags, currentFrame):
    global selectedFigureId, selectedPoint, nextFigureId, activeFigureId

    if event == cv2.EVENT_LBUTTONUP:
        if flags & cv2.EVENT_FLAG_SHIFTKEY:
            figureId, pointIndex = findPointAt(x, y)
            if figureId is not None:
                deleteFigure(figureId)
            return

        closesFigure = len(drawingFigurePoints) > 2 and isNear(x, y, drawingFigurePoints[0])
        if closesFigure:
            visibleFigures[nextFigureId] = drawingFigurePoints.copy()
            saveFigureAtFrame(nextFigureId, currentFrame)

            activeFigureId = nextFigureId
            nextFigureId += 1
            drawingFigurePoints.clear()
        else:
            drawingFigurePoints.append((x, y))

    if event == cv2.EVENT_RBUTTONDOWN:
        selectedFigureId, selectedPoint = findPointAt(x, y)
        if selectedFigureId is not None:
            activeFigureId = selectedFigureId

    if event == cv2.EVENT_RBUTTONUP:
        if selectedFigureId is not None:
            saveFigureAtFrame(selectedFigureId, currentFrame)

        selectedFigureId = None
        selectedPoint = None
    
    if event == cv2.EVENT_MOUSEMOVE:
        if selectedFigureId is not None:
            visibleFigures[selectedFigureId][selectedPoint] = (x, y)

def isNear(x, y, point):
    return math.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2) < config.CLICK_RADIUS

def findPointAt(x, y):
    for figureId, vertices in visibleFigures.items():
        for pointIndex, point in enumerate(vertices):
            if isNear(x, y, point):
                return figureId, pointIndex
    return None, None

def saveFigureAtFrame(figureId, frameIndex):
    if figureId not in figuresKeyframes:
        figuresKeyframes[figureId] = {}
    figuresKeyframes[figureId][frameIndex] = visibleFigures[figureId].copy()

def getFigureAtFrame(figureId, frameIndex):
    if figureId not in figuresKeyframes:
        return None

    figureKeyframes = figuresKeyframes[figureId]

    previousFrame = None
    nextFrame = None

    for frame in figureKeyframes:
        if frame <= frameIndex and (previousFrame is None or frame > previousFrame):
                previousFrame = frame

        if frame >= frameIndex and (nextFrame is None or frame < nextFrame):
                nextFrame = frame

    if previousFrame is None:
        return None

    previousPoints = figureKeyframes[previousFrame]

    if nextFrame is None or previousFrame == nextFrame:
        return list(previousPoints)

    nextPoints = figureKeyframes[nextFrame]

    ratio = ((frameIndex - previousFrame) / (nextFrame - previousFrame))
    interpolatedPoints = []

    for i in range(len(previousPoints)):
        x1, y1 = previousPoints[i]
        x2, y2 = nextPoints[i]

        x = round(x1 + (x2 - x1) * ratio)
        y = round(y1 + (y2 - y1) * ratio)

        interpolatedPoints.append((x, y))

    return interpolatedPoints

def getFiguresAtFrame(frameIndex):
    result = {}

    for figureId in figuresKeyframes.keys():
        vertices = getFigureAtFrame(figureId, frameIndex)

        if vertices is not None:
            result[figureId] = vertices

    return result

def updateFiguresForFrame(frameIndex):
    global visibleFigures
    visibleFigures = getFiguresAtFrame(frameIndex)
    drawingFigurePoints.clear()
    selectedFigureId = None
    selectedPoint = None

def undoLastPoint():
    if len(drawingFigurePoints) > 0:
        drawingFigurePoints.pop()

def deleteFigure(figureId):
    global activeFigureId
    visibleFigures.pop(figureId, None)
    figuresKeyframes.pop(figureId, None)
    if activeFigureId == figureId:
        activeFigureId = None

def getVisibleFigures():
    return visibleFigures

def getPoints():
    return drawingFigurePoints

def getFiguresKeyframes():
    return figuresKeyframes

def getFigureKeyframes(figureId):
    return figuresKeyframes.get(figureId, {})

def getActiveFigureId():
    return activeFigureId