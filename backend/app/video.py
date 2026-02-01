import cv2
import uuid
import numpy as np
from pathlib import Path
from fastapi import UploadFile
from ultralytics import YOLO

# ---------------- PATH SETUP ----------------
BASE_DIR = Path(__file__).resolve().parent.parent
VIDEO_DIR = BASE_DIR / "outputs" / "videos"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = BASE_DIR / "helmet_detector_best.pt"

# ---------------- LOAD MODEL ONCE ----------------
model = YOLO(str(MODEL_PATH))

# ---------------- VIDEO PROCESSING ----------------
def process_video(file: UploadFile):
    input_path = VIDEO_DIR / f"input_{uuid.uuid4()}.mp4"
    output_path = VIDEO_DIR / f"output_{uuid.uuid4()}.mp4"

    # Save uploaded video
    with open(input_path, "wb") as f:
        f.write(file.file.read())
    file.file.close()

    cap = cv2.VideoCapture(str(input_path))

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = cap.get(cv2.CAP_PROP_FPS)
    fps = fps if fps and fps > 1 else 25

    out = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    per_frame_confidence = []
    frames_with_helmet = 0
    total_frames = 0

    # ---------------- FRAME LOOP ----------------
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1
        results = model(frame, conf=0.4)[0]

        frame_conf = 0.0

        # Helmet present in this frame
        if results.boxes is not None and len(results.boxes) > 0:
            frames_with_helmet += 1
            frame_conf = float(max(box.conf[0] for box in results.boxes))

        per_frame_confidence.append(frame_conf)

        # Draw bounding boxes
        for box in results.boxes or []:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(
                frame,
                f"Helmet {conf:.2f}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )

        out.write(frame)

    # ---------------- CLEANUP ----------------
    cap.release()
    out.release()
    input_path.unlink(missing_ok=True)

    # ---------------- AGGREGATION ----------------
    avg_confidence = float(np.mean(per_frame_confidence)) if per_frame_confidence else 0.0
    presence_ratio = frames_with_helmet / total_frames if total_frames > 0 else 0.0

    # Helmet considered worn if:
    # - present in >= 40% frames
    # - average confidence >= 60%
    verdict = (
        "HELMET WORN"
        if presence_ratio >= 0.4 and avg_confidence >= 0.6
        else "NOT WORN"
    )

    # ---------------- RESPONSE ----------------
    return {
        "video_url": f"/videos/{output_path.name}",
        "total_frames": total_frames,
        "frames_with_helmet": frames_with_helmet,
        "helmet_presence_ratio": round(presence_ratio, 3),
        "avg_confidence": round(avg_confidence, 3),
        "verdict": verdict,
        "confidence_timeline": per_frame_confidence  # 📊 frontend graph
    }
