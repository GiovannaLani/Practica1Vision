import cv2
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
    elif key in (ord('b'), ord('B')):
        figures.undoLastPoint()

    elif key in (ord('g'), ord('G')):
        save.generateVideo(fps, size)
    elif key in (ord('h'), ord('H')):
        save.generateVideo(fps, size, hideFigures=True)
    elif key in (ord('j'), ord('J')):
        save.generateVideo(fps, size, hideBackground=True)
    elif key in (ord('k'), ord('K')):
        save.generateVideoByFigures(fps, size)


    frame_ui = frame.copy()

    ui.drawPoints(frame_ui, figures.getPoints())
    ui.drawFigures(frame_ui, figures.getVisibleFigures())
    
    cv2.putText(frame_ui, f'{currentFrame + 1} / {totalFrames}', (size[0] - 140, 40), cv2.FONT_HERSHEY_SIMPLEX, config.FONT_SCALE, config.COLOR_TEXT, config.FONT_THICKNESS)

    cv2.imshow(config.WINDOW_NAME, frame_ui)