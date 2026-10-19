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

def generateVideoByFigures(fps, size):
    inputVideo = cv2.VideoCapture(config.VIDEO_NAME)

    bounds = {}
    writers = {}

    for figureId, keyframes in figures.getFiguresKeyframes().items():
        pointsKeyframes = {}

        for frameId, data in keyframes.items():
            points = data[1]
            pointsKeyframes[frameId] = points

        figureBounds = getFigureBounds(pointsKeyframes)
        
        if figureBounds is None:
            continue
        
        bounds[figureId] = figureBounds

        writers[figureId] = cv2.VideoWriter(config.REGION_VIDEO_PATTERN.format(figureId), cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, figureBounds)

    frameIndex = 0
    success, originalFrame = inputVideo.read()

    while success:
        figuresAtFrame = figures.getFiguresAtFrame(frameIndex)

        for figureId, writer in writers.items():
            points = figuresAtFrame.get(figureId)

            if points is None:
                continue

            frameWithFigure = originalFrame.copy()
            figuresToKeep = [points]

            keepFigures(figuresToKeep, frameWithFigure)
 
            writer.write(centerFigure(frameWithFigure, points, bounds[figureId]))

        frameIndex += 1
        success, originalFrame = inputVideo.read()

    inputVideo.release()

    for writer in writers.values():
        writer.release()

    print("VIDEOS DE FIGURAS GUARDADOS" + ", ".join([config.REGION_VIDEO_PATTERN.format(figureId) for figureId in writers.keys()]))

def getFigureBounds(keyframes):
    maxWidth = 0
    maxHeight = 0
    found = False
 
    for points in keyframes.values():
        if len(points) < 3:
            continue
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        maxWidth = max(maxWidth, max(xs) - min(xs) + 1)
        maxHeight = max(maxHeight, max(ys) - min(ys) + 1)
        found = True
 
    if not found:
        return None
 
    return maxWidth, maxHeight

def centerFigure(frame, points, outputSize):
    minX = min(point[0] for point in points)
    maxX = max(point[0] for point in points)
    minY = min(point[1] for point in points)
    maxY = max(point[1] for point in points)
    center = (
        (minX + maxX) / 2,
        (minY + maxY) / 2,
    )

    return cv2.getRectSubPix(frame, outputSize, center)