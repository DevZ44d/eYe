import cv2

class CameraCapture:
    def __init__(self):
        self.filename = "screenshot.jpg"

    def capture(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return False, "No camera"

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            ret, frame = cap.read()
            cap.release()
            cv2.destroyAllWindows()

            if ret:
                cv2.imwrite(self.filename, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                return True, self.filename
            return False, "Capture failed"
        except:
            try:
                cv2.destroyAllWindows()
            except:
                pass
            return False, "Camera error"