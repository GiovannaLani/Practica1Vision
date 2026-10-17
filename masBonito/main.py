import cv2
import numpy as np
import figures
import ui
import save
import config

def onMouse(event, x, y, flags, param):
    figures.onMouse(event, x, y, flags, currentFrame)

videoCapture = cv2.VideoCapture(config.VIDEO_NAME)

size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fps = videoCapture.get(cv2.CAP_PROP_FPS)
totalFrames = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))

cv2.namedWindow(config.WINDOW_NAME)
cv2.setMouseCallback(config.WINDOW_NAME, onMouse)

success, frame = videoCapture.read()
currentFrame = 0

while success:
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    
    elif key == ord('d'):
        currentFrame = ui.changeFrame(currentFrame, 1, totalFrames, videoCapture, frame)
    elif key == ord('f'):
        currentFrame = ui.changeFrame(currentFrame, int(fps), totalFrames, videoCapture, frame)
    elif key == ord('s'):
        currentFrame = ui.changeFrame(currentFrame, -1, totalFrames, videoCapture, frame)
    elif key == ord('a'):
        currentFrame = ui.changeFrame(currentFrame, -int(fps), totalFrames, videoCapture, frame)

    elif key == 26: #Ctrl + Z
        figures.undoLastPoint()

    elif key == ord('v'):
        figures.toggleVisibilityAtFrame(currentFrame)
    elif key == ord('k'):
        figures.saveDeleteKeyframeAtFrame(currentFrame)
    elif key == ord('t'):
        figures.selectNextFigure()

    elif key == ord('g'):
        print("Generando vídeo... Escoge una opción:")
        print("1. Guardar vídeo con regiones seleccionadas")
        print("2. Guardar vídeo ocultando las regiones seleccionadas")
        print("3. Guardar vídeo mostrando solo las regiones seleccionadas")
        print("4. Guardar un video por cada región seleccionada")
        option = input("Opción: ").strip()
        if option == "1":
            save.generateVideo(fps, size)
        elif option == "2":
            save.generateVideo(fps, size, hideFigures=True)
        elif option == "3":
            save.generateVideo(fps, size, hideBackground=True)
        elif option == "4":
            save.generateVideoByFigures(fps, size)


    frameUI = frame.copy()

    ui.drawPoints(frameUI, figures.getPoints())
    ui.drawFigures(frameUI, figures.getVisibleFigures())

    panel = ui.createPanel(frameUI, currentFrame, totalFrames)

    finalFrame = np.vstack((frameUI, panel))
    cv2.imshow(config.WINDOW_NAME, finalFrame)