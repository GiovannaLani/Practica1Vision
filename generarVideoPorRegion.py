import cv2
import math

drawing = False
points = []
figures =[]
regionSelections = {}
regionResetFrames = set()

selectedPoint = -1
selectedFigure = None

def saveCurrentFrameRegions():
    frameIndex = min(max(frame_num - 1, 0), total_frames - 1)
    regionSelections[frameIndex] = tuple(
        tuple((int(x), int(y)) for x, y in figure) for figure in figures
    )


def getFiguresForFrame(frameIndex):
    selectedFrames = sorted(regionSelections)
    if not selectedFrames:
        return ()

    previousFrame = max(
        (index for index in selectedFrames if index <= frameIndex),
        default=None
    )
    nextFrame = min(
        (index for index in selectedFrames if index >= frameIndex),
        default=None
    )

    if previousFrame is None:
        if nextFrame in regionResetFrames:
            return ()
        return regionSelections[nextFrame]
    if nextFrame is None or previousFrame == nextFrame:
        return regionSelections[previousFrame]

    previousFigures = regionSelections[previousFrame]
    nextFigures = regionSelections[nextFrame]
    if nextFrame in regionResetFrames:
        return previousFigures
    if (len(previousFigures) != len(nextFigures)
            or any(len(a) != len(b) for a, b in zip(previousFigures, nextFigures))):
        return previousFigures

    ratio = (frameIndex - previousFrame) / (nextFrame - previousFrame)
    return tuple(
        tuple(
            (round(x1 + (x2 - x1) * ratio), round(y1 + (y2 - y1) * ratio))
            for (x1, y1), (x2, y2) in zip(figure1, figure2)
        )
        for figure1, figure2 in zip(previousFigures, nextFigures)
    )


def onMouse(event, x, y, flags, param):
    global drawing, frame, figures, points, selectedFigure, selectedPoint
    


    if event == cv2.EVENT_LBUTTONUP:
        if len(points) == 0:
            points.append((x, y))
        else:
            if len(points) > 1 and math.sqrt((x - points[0][0]) ** 2 + (y - points[0][1]) ** 2) < 10:
                figures.append(points.copy())
                points.clear()
                saveCurrentFrameRegions()
            else:
                points.append((x, y))


        
        
    if event == cv2.EVENT_RBUTTONDOWN:
        for figure in figures:
            for i, point in enumerate(figure):
                if math.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2) < 10: #TODO
                    selectedFigure = figure
                    selectedPoint = i

    if event == cv2.EVENT_RBUTTONUP:
        if selectedPoint != -1:
            saveCurrentFrameRegions()
        selectedFigure = None
        selectedPoint = -1

    if event == cv2.EVENT_MOUSEMOVE:
        if selectedPoint != -1:
            selectedFigure[selectedPoint] = (x,y)


def changeFrame(step):
    global frame, frame_num, figures, selectedFigure, selectedPoint
    targetFrame = min(max(frame_num + step, 1), total_frames)
    if targetFrame == frame_num:
        return False

    videoCapture.set(cv2.CAP_PROP_POS_FRAMES, targetFrame - 1)
    success, nextFrame = videoCapture.read()
    if not success:
        raise RuntimeError(f"No se pudo leer el fotograma {targetFrame}.")

    frame_num = targetFrame
    frame = nextFrame
    figures = [list(map(tuple, figure)) for figure in getFiguresForFrame(frame_num - 1)]
    points.clear()
    selectedFigure = None
    selectedPoint = -1
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


def keepFigures(figures, frame):
    originalFrame = frame.copy()
    height, width = frame.shape[:2]
    frame[:] = (0, 0, 0)

    for figure in figures:
        if len(figure) < 3:
            continue

        for y in range(height):
            crossings = []
            for i in range(len(figure)):
                x1, y1 = figure[i]
                x2, y2 = figure[(i + 1) % len(figure)]
                if (y1 > y) != (y2 > y):
                    crossingX = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                    crossings.append(crossingX)

            crossings.sort()
            for i in range(0, len(crossings) - 1, 2):
                startX = max(0, math.ceil(crossings[i]))
                endX = min(width, math.ceil(crossings[i + 1]))
                frame[y, startX:endX] = originalFrame[y, startX:endX]


def generateHiddenVideo():
    saveCurrentFrameRegions()
    outputCapture = cv2.VideoCapture("Video Práctica.mp4")
    if not outputCapture.isOpened():
        raise RuntimeError("No se pudo abrir el vídeo: Video Práctica.mp4")

    outputWriter = cv2.VideoWriter(
        "MyOutputVid.avi",
        cv2.VideoWriter_fourcc('I', '4', '2', '0'),
        fps,
        size
    )
    if not outputWriter.isOpened():
        outputCapture.release()
        raise RuntimeError("No se pudo crear el vídeo: MyOutputVid.avi")

    processedFrames = 0
    try:
        while True:
            success, outputFrame = outputCapture.read()
            if not success:
                break

            keepFigures(getFiguresForFrame(processedFrames), outputFrame)
            outputWriter.write(outputFrame)
            processedFrames += 1
    finally:
        outputCapture.release()
        outputWriter.release()

    if processedFrames == 0:
        raise RuntimeError("El vídeo no contiene fotogramas: Video Práctica.mp4")

    print(f"Vídeo completo guardado en MyOutputVid.avi ({processedFrames} fotogramas).")


def generateVideosByRegion():
    saveCurrentFrameRegions()
    numberOfRegions = max(
        (len(selectedFigures) for selectedFigures in regionSelections.values()),
        default=0
    )
    if numberOfRegions == 0:
        raise RuntimeError("No hay figuras definidas para generar vídeos.")

    outputCapture = cv2.VideoCapture("Video Práctica.mp4")
    if not outputCapture.isOpened():
        raise RuntimeError("No se pudo abrir el vídeo: Video Práctica.mp4")

    outputWriters = []
    outputPaths = []
    processedFrames = 0
    try:
        contador = 1
        while contador <= numberOfRegions:
            outputPath = f"VideoFigura{contador}.avi"
            outputWriter = cv2.VideoWriter(
                outputPath,
                cv2.VideoWriter_fourcc('I', '4', '2', '0'),
                fps,
                size
            )
            outputWriters.append(outputWriter)
            if not outputWriter.isOpened():
                raise RuntimeError(f"No se pudo crear el vídeo: {outputPath}")
            outputPaths.append(outputPath)
            contador += 1

        while True:
            success, outputFrame = outputCapture.read()
            if not success:
                break

            figuresForFrame = getFiguresForFrame(processedFrames)
            for regionIndex, outputWriter in enumerate(outputWriters):
                regionFrame = outputFrame.copy()
                regionFigures = (
                    (figuresForFrame[regionIndex],)
                    if regionIndex < len(figuresForFrame)
                    else ()
                )
                keepFigures(regionFigures, regionFrame)
                outputWriter.write(regionFrame)
            processedFrames += 1
    finally:
        outputCapture.release()
        for outputWriter in outputWriters:
            outputWriter.release()

    if processedFrames == 0:
        raise RuntimeError("El vídeo no contiene fotogramas: Video Práctica.mp4")

    for regionIndex, outputPath in enumerate(outputPaths, start=1):
        print(
            f"Vídeo de la región {regionIndex} guardado en {outputPath} "
            f"({processedFrames} fotogramas)."
        )


videoCapture = cv2.VideoCapture("Video Práctica.mp4")
if not videoCapture.isOpened():
    raise RuntimeError("No se pudo abrir el vídeo: Video Práctica.mp4")

size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fps = videoCapture.get(cv2.CAP_PROP_FPS)

cv2.namedWindow('MyWindow')
cv2.setMouseCallback('MyWindow', onMouse)

success, frame = videoCapture.read()
frame_num = 1
total_frames = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))

while success:

    key = cv2.waitKey(1) & 0xFF

    if key == 32: #Tecla espacio
        changeFrame(1)
    elif key == ord('d'):
        changeFrame(1)
    elif key == ord('f'):
        changeFrame(int(fps))
    elif key == ord('s'):
        changeFrame(-1)
    elif key == ord('a'):
        changeFrame(-int(fps))
    elif key == ord('q'):
        break

    elif key in (98, 66): #Tecla B
        figures.clear()
        points.clear()
        selectedFigure = None
        selectedPoint = -1
        resetFrame = min(max(frame_num - 1, 0), total_frames - 1)
        regionSelections[resetFrame] = ()
        regionResetFrames.add(resetFrame)
    elif key in (ord('g'), ord('G')):
        generateHiddenVideo()
    elif key in (ord('m'), ord('M')):
        generateVideosByRegion()

    frame_ui = frame.copy()

    drawPoints(points, frame_ui)
    for figure in figures:
        drawFigure(figure, frame_ui)

    cv2.putText(frame_ui, f'{frame_num} / {total_frames}', (size[0] - 140, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    

    cv2.imshow('MyWindow', frame_ui)
    if cv2.getWindowProperty('MyWindow', cv2.WND_PROP_VISIBLE) < 1:
        break
cv2.destroyWindow('MyWindow')
videoCapture.release()