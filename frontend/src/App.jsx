import { useState, useRef } from "react";
import "./index.css";

export default function App() {
  const [mode, setMode] = useState("image"); // image | video
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const canvasRef = useRef(null);
  const imageRef = useRef(null);

  /* ================= RESET ================= */
  const clearAll = () => {
    setFile(null);
    setPreview(null);
    setResult(null);

    if (canvasRef.current) {
      const ctx = canvasRef.current.getContext("2d");
      ctx.clearRect(
        0,
        0,
        canvasRef.current.width,
        canvasRef.current.height
      );
    }
  };

  /* ================= FILE HANDLER ================= */
  const handleFile = (file) => {
    if (!file) return;

    setFile(file);
    setResult(null);

    if (mode === "image") {
      const url = URL.createObjectURL(file);
      setPreview(url);

      const img = new Image();
      img.src = url;

      img.onload = () => {
        imageRef.current = img;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");

        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
      };
    } else {
      setPreview(file.name);
    }
  };

  /* ================= DRAW BOXES (IMAGE) ================= */
  const drawBoxes = (detections) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const img = imageRef.current;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0);

    detections.forEach((d) => {
      ctx.strokeStyle = "#00fff0";
      ctx.lineWidth = 3;
      ctx.shadowColor = "#00fff0";
      ctx.shadowBlur = 10;

      ctx.strokeRect(
        d.x1,
        d.y1,
        d.x2 - d.x1,
        d.y2 - d.y1
      );

      ctx.fillStyle = "#00fff0";
      ctx.font = "16px Poppins";
      ctx.fillText(
        `Helmet ${(d.confidence * 100).toFixed(1)}%`,
        d.x1,
        d.y1 - 6
      );
    });
  };

  /* ================= NORMALIZE RESULT ================= */
  const normalizeResult = (data) => {
    if (mode === "image") {
      const confs = data.detections?.map((d) => d.confidence) || [];
      const avg =
        confs.length > 0
          ? confs.reduce((a, b) => a + b, 0) / confs.length
          : 0;

      return {
        verdict: confs.length > 0 ? "HELMET WORN" : "NOT WORN",
        avg_confidence: avg.toFixed(3),
      };
    }

    return {
      verdict: data.verdict,
      avg_confidence: data.avg_confidence,
      helmet_presence_ratio: data.helmet_presence_ratio,
      video_url: data.video_url,
    };
  };

  /* ================= UPLOAD ================= */
  const runDetection = async () => {
    if (!file) return alert("Upload a file first");

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setResult(null);

    const endpoint =
      mode === "image"
        ? "http://127.0.0.1:8000/predict"
        : "http://127.0.0.1:8000/predict-video";

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Backend error");

      const data = await res.json();
      const normalized = normalizeResult(data);

      setResult(normalized);

      if (mode === "image") {
        drawBoxes(data.detections);
      }
    } catch (err) {
      alert("Backend not running");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  /* ================= UI ================= */
  return (
    <div className="page">
      <div className="container">
        {/* MODE TOGGLE */}
        <div className="mode-toggle">
          <button
            className={mode === "image" ? "active" : ""}
            onClick={() => {
              setMode("image");
              clearAll();
            }}
          >
            Image
          </button>
          <button
            className={mode === "video" ? "active" : ""}
            onClick={() => {
              setMode("video");
              clearAll();
            }}
          >
            Video
          </button>
        </div>

        <h1>Helmet Detection</h1>
        <p className="subtitle">YOLO-powered AI Vision System</p>

        {/* UPLOAD CARD */}
        <div
          className="upload-card"
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            handleFile(e.dataTransfer.files[0]);
          }}
        >
          {!file ? (
            <>
              <p className="drop-text">
                Drag & Drop {mode === "image" ? "Image" : "Video"}
              </p>
              <div className="or-divider"><span>OR</span></div>

              <label className="upload-btn">
                Browse File
                <input
                  hidden
                  type="file"
                  accept={mode === "image" ? "image/*" : "video/*"}
                  onChange={(e) => handleFile(e.target.files[0])}
                />
              </label>
            </>
          ) : (
            <>
              {mode === "image" ? (
                <canvas ref={canvasRef} className="preview-canvas" />
              ) : (
                <div className="image-frame">{file.name}</div>
              )}

              <button className="remove-btn" onClick={clearAll}>✕</button>
            </>
          )}
        </div>

        {/* RUN BUTTON */}
        <button className="detect-btn" onClick={runDetection}>
          {loading ? "Detecting..." : "Run Detection"}
        </button>

        {/* RESULT */}
        {result && (
          <div className="result">
            <h3>Detection Result</h3>
            <p><b>Verdict:</b> {result.verdict}</p>
            <p><b>Avg Confidence:</b> {result.avg_confidence}</p>

            {mode === "video" && (
              <>
                <p><b>Helmet Ratio:</b> {result.helmet_presence_ratio}</p>
                <video
                  src={`http://127.0.0.1:8000${result.video_url}`}
                  controls
                />
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
