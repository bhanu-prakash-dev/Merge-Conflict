import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from PIL import Image
from ultralytics import YOLO

from app.video import process_video
from app.stream import generate_frames

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "helmet_detector_best.pt")
VIDEO_DIR = os.path.join(BASE_DIR, "outputs", "videos")

os.makedirs(VIDEO_DIR, exist_ok=True)

# ---------------- APP ----------------
app = FastAPI(title="Helmet Detection API")

app.mount("/videos", StaticFiles(directory=VIDEO_DIR), name="videos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- LOAD MODEL ONCE ----------------
model = YOLO(MODEL_PATH)

# ---------------- ROUTES ----------------
@app.get("/")
def root():
    return {"status": "API running"}

# ======================================================
# IMAGE PREDICTION  (USED BY EXISTING App.jsx)
# ======================================================
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 🔒 Guard: image only
    if not file.content_type.startswith("image/"):
        return {"error": "Please upload an image file"}

    image = Image.open(file.file).convert("RGB")
    file.file.close()

    results = model(image)

    detections = []
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            detections.append({
                "x1": float(x1),
                "y1": float(y1),
                "x2": float(x2),
                "y2": float(y2),
                "confidence": float(box.conf[0])
            })

    return {
        "helmets_detected": len(detections),
        "detections": detections
    }

# ======================================================
# VIDEO PREDICTION (AGGREGATED ANALYSIS)
# ======================================================
@app.post("/predict-video")
async def predict_video(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".mp4", ".avi", ".mov")):
        return {"error": "Unsupported video format"}

    return process_video(file)

# ======================================================
# LIVE STREAMING (OPTIONAL — USED LATER)
# ======================================================
@app.get("/stream-video")
def stream_video(filename: str):
    video_path = os.path.join(VIDEO_DIR, filename)

    if not os.path.exists(video_path):
        return {"error": "Video not found"}

    return StreamingResponse(
        generate_frames(video_path),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
