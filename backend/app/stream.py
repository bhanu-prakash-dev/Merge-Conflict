import cv2

def generate_frames(video_path: str):
    """
    MJPEG video streaming generator.
    Used by /stream-video endpoint.
    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Encode frame as JPEG
        success, buffer = cv2.imencode(".jpg", frame)
        if not success:
            continue

        frame_bytes = buffer.tobytes()

        # MJPEG frame format
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes +
            b"\r\n"
        )

    cap.release()
