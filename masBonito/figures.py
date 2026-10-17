import cv2
import math
import config

visibleFigures = {}
drawingFigurePoints = []
figuresKeyframes = {}
figureNames = {}
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
            saveFigureAtFrame(nextFigureId, currentFrame, created=True)

            name = input(f"Nombre de la figura {nextFigureId} (Enter = Figura {nextFigureId}): ").strip()
            if name == "":
                name = f"Figura {nextFigureId}"
            figureNames[nextFigureId] = name
            
            activeFigureId = nextFigureId
            nextFigureId += 1
            drawingFigurePoints.clear()
        else:
            drawingFigurePoints.append((x, y))
        
    elif event == cv2.EVENT_RBUTTONDOWN:
        selectedFigureId, selectedPoint = findPointAt(x, y)
        if selectedFigureId is not None:
            activeFigureId = selectedFigureId

    elif event == cv2.EVENT_RBUTTONUP:
        if selectedFigureId is not None:
            saveFigureAtFrame(selectedFigureId, currentFrame)
        selectedFigureId = None
        selectedPoint = None

    elif event == cv2.EVENT_MOUSEMOVE:
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

def saveFigureAtFrame(figureId, frameIndex, created=False):
    if figureId not in figuresKeyframes:
        figuresKeyframes[figureId] = {}
    if created and frameIndex != 0:
        figuresKeyframes[figureId][0] = (False, visibleFigures[figureId].copy())

    figuresKeyframes[figureId][frameIndex] = (True, visibleFigures[figureId].copy())
    print(f"Figures keyframes updated for figure {figureId} at frame {frameIndex}: {figuresKeyframes[figureId]}")

def getFigureStateAtFrame(figureId, frameIndex):
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

    previousVisible, previousPoints = figureKeyframes[previousFrame]

    if nextFrame is None or previousFrame == nextFrame:
        return previousVisible, list(previousPoints)

    nextPoints = figureKeyframes[nextFrame][1]
    ratio = (frameIndex - previousFrame) / (nextFrame - previousFrame)

    interpolatedPoints = []
    for i in range(len(previousPoints)):
        x1, y1 = previousPoints[i]
        x2, y2 = nextPoints[i]

        x = round(x1 + (x2 - x1) * ratio)
        y = round(y1 + (y2 - y1) * ratio)

        interpolatedPoints.append((x, y))

    return previousVisible, interpolatedPoints

def getFigureAtFrame(figureId, frameIndex):
    state = getFigureStateAtFrame(figureId, frameIndex)
    if state is None or not state[0]:
        return None
    return state[1]

def getFiguresAtFrame(frameIndex):
    result = {}

    for figureId in figuresKeyframes.keys():
        vertices = getFigureAtFrame(figureId, frameIndex)

        if vertices is not None:
            result[figureId] = vertices

    return result

def deleteFigure(figureId):
    global activeFigureId
    visibleFigures.pop(figureId, None)
    figuresKeyframes.pop(figureId, None)
    figureNames.pop(figureId, None)
    if activeFigureId == figureId:
        activeFigureId = None

def undoLastPoint():
    if len(drawingFigurePoints) > 0:
        drawingFigurePoints.pop()

def selectNextFigure():
    global activeFigureId
    ids = sorted(figuresKeyframes.keys())
    if len(ids) == 0:
        return
    if activeFigureId in ids:
        activeFigureId = ids[(ids.index(activeFigureId) + 1) % len(ids)]
    else:
        activeFigureId = ids[0]

def toggleVisibilityAtFrame(frameIndex):
    if activeFigureId is None or activeFigureId not in figuresKeyframes:
        return

    state = getFigureStateAtFrame(activeFigureId, frameIndex)
    if state is None:
        return

    visible, vertices = state
    figuresKeyframes[activeFigureId][frameIndex] = (not visible, vertices)
    refreshVisibleFigures(frameIndex)

def saveDeleteKeyframeAtFrame(frameIndex):
    if activeFigureId is None or activeFigureId not in figuresKeyframes:
        return

    keyframes = figuresKeyframes[activeFigureId]

    if frameIndex not in keyframes:
        saveFigureAtFrame(activeFigureId, frameIndex)
        return

    if len(keyframes) == 1:
        return

    keyframes.pop(frameIndex, None)
    refreshVisibleFigures(frameIndex)

def getVisibleFigures():
    return visibleFigures

def getPendingPoints():
    return drawingFigurePoints

def getFiguresKeyframes():
    return figuresKeyframes

def getFigureKeyframes(figureId):
    return figuresKeyframes.get(figureId, {})

def getActiveFigureId():
    return activeFigureId

def refreshVisibleFigures(frameIndex):
    global visibleFigures
    visibleFigures = getFiguresAtFrame(frameIndex)

def getPoints():
    return drawingFigurePoints

def getFigureName(figureId):
    return figureNames.get(figureId, f"Figura {figureId}")

def updateFiguresForFrame(frameIndex):
    global selectedFigureId, selectedPoint
    refreshVisibleFigures(frameIndex)
    drawingFigurePoints.clear()
    selectedFigureId = None
    selectedPoint = None