import cv2
import math
import figures
import ui
import config

def generateVideo(fps, size, hideFigures=False, hideBackground=False):
    inputVideo = cv2.VideoCapture(config.VIDEO_NAME)
    outputVideoName = config.OUTPUT_VIDEO
    if hideFigures:
        outputVideoName = outputVideoName + "_HideFigures.avi"
    elif hideBackground:
        outputVideoName = outputVideoName + "_HideBackground.avi"
    else:
        outputVideoName = outputVideoName + ".avi"

    outputWriter = cv2.VideoWriter(outputVideoName, cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)

    frameIndex = 0
    success, outputFrame = inputVideo.read()
    while success:
        figuresAtFrame = figures.getFiguresAtFrame(frameIndex)
        figuresList = list(figuresAtFrame.values())
        
        if hideBackground:
            keepFigures(figuresList, outputFrame)
        elif hideFigures:
            for figure in figuresList:
                hideFigure(figure, outputFrame)
        else:
            ui.drawFigures(outputFrame, figuresAtFrame)
        
        outputWriter.write(outputFrame)
        frameIndex += 1
        success, outputFrame = inputVideo.read()
    
    inputVideo.release()
    outputWriter.release()
    print(f"VÍDEO GUARDADO: {outputVideoName}")

def hideFigure(figure, frame, color=config.COLOR_HIDDEN):
    height, width = frame.shape[:2]
    for y, startX, endX in getPolygonSpans(figure, width, height):
        frame[y, startX:endX] = color

def keepFigures(figuresList, frame):
    originalFrame = frame.copy()
    height, width = frame.shape[:2]
    frame[:] = config.COLOR_HIDDEN
 
    for figure in figuresList:
        for y, startX, endX in getPolygonSpans(figure, width, height):
            frame[y, startX:endX] = originalFrame[y, startX:endX]

def getPolygonSpans(figure, width, height):
    spans = []
    if len(figure) < 3:
        return spans
    
    ys =[]
    for point in figure:
        ys = ys + [point[1]]

    firstY = max(0, min(ys))
    lastY = min(height - 1, max(ys))
 
    for y in range(firstY, lastY + 1):
        crossings = []
        for i in range(len(figure)):
            x1, y1 = figure[i]
            x2, y2 = figure[(i + 1) % len(figure)]
            if (y1 > y) != (y2 > y):
                crossings.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
 
        crossings.sort()
        for i in range(0, len(crossings) - 1, 2):
            startX = max(0, math.ceil(crossings[i]))
            endX = min(width, math.ceil(crossings[i + 1]))
            spans.append((y, startX, endX))
 
    return spans

#TODO Si la figura el tamaño del frame es del recorrido en vez de la figura
#TODO si la figura se oculta no añadir frame
def generateVideoByFigures(fps, size):
    inputVideo = cv2.VideoCapture(config.VIDEO_NAME)

    bounds = {}
    writers = {}

    for figureId, keyframes in figures.getFiguresKeyframes().items():
        pointsKeyframes = {}

        for frameId, data in keyframes.items():
            points = data[1]
            pointsKeyframes[frameId] = points

        figureBounds = getFigureBounds(pointsKeyframes, size)
        
        if figureBounds is None:
            continue
        
        minX, maxX, minY, maxY = figureBounds
        bounds[figureId] = figureBounds

        writers[figureId] = cv2.VideoWriter(config.REGION_VIDEO_PATTERN.format(figureId), cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, (maxX - minX + 1, maxY - minY + 1))

    frameIndex = 0
    success, originalFrame = inputVideo.read()

    while success:
        figuresAtFrame = figures.getFiguresAtFrame(frameIndex)

        for figureId, writer in writers.items():
            minX, maxX, minY, maxY = bounds[figureId]
            frameWithFigure = originalFrame.copy()

            points = figuresAtFrame.get(figureId)

            if points is None:
                continue

            figuresToKeep = [points]

            keepFigures(figuresToKeep, frameWithFigure)
 
            writer.write(frameWithFigure[minY:maxY + 1, minX:maxX + 1])

        frameIndex += 1
        success, originalFrame = inputVideo.read()

    inputVideo.release()

    for writer in writers.values():
        writer.release()

    print("VIDEOS DE FIGURAS GUARDADOS" + ", ".join([config.REGION_VIDEO_PATTERN.format(figureId) for figureId in writers.keys()]))

def getFigureBounds(keyframes, frameSize):
    minX, maxX = frameSize[0] - 1, 0
    minY, maxY = frameSize[1] - 1, 0
    found = False
 
    for points in keyframes.values():
        if len(points) < 3:
            continue
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        minX = min(minX, min(xs))
        maxX = max(maxX, max(xs))
        minY = min(minY, min(ys))
        maxY = max(maxY, max(ys))
        found = True
 
    if not found:
        return None
 
    return (max(minX, 0), min(maxX, frameSize[0] - 1), max(minY, 0), min(maxY, frameSize[1] - 1))