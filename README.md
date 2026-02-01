# Merge-Conflict
This is my Hackathon repository in which I have trained a ML Model which detects helmets in the pictures clicked by the cameras on the traffic lights

GuardianEye-AI

AI-Powered Threat Detection & Surveillance Platform

GuardianEye-AI is a cutting-edge artificial intelligence system designed to enhance safety and threat detection in real-time. Using advanced machine learning and computer vision, GuardianEye autonomously monitors environments, detects threats, alerts users instantly, and supports proactive response workflows.

🚀 Key Features

Real-Time Threat Detection: Uses AI vision models to detect predefined threat actions and behaviors instantly.

Live Monitoring & Alerts: Recognizes risks as they occur and streams alerts with contextual metadata.

Incident Logging: Automatically records incidents with timestamps and severity details.

Automated Notifications: Integrated alerting via chat services or custom APIs.

Easy Integration: Lightweight backend ready for web/mobile service hooks.
(This feature set is based on typical functionality for real-time AI surveillance systems like GuardianEye-AI — see similar implementations online.)

🧠 How It Works

Video Capture & Feed Processing
Camera or video input is processed in real time to extract frames suitable for analysis.

AI Inference Engine
Deep learning models analyze frames to spot dangerous actions or suspicious behavior.

Detection Filtering
Alerts are filtered and scored to reduce false positives and highlight critical events.

Notifications & Logging
Once a threat is recognized, incidents are logged and alerts are pushed to the configured channel.

(This workflow reflects standard real-time CV + ML processing architectures.)

📦 Tech Stack

Computer Vision: Deep learning (YOLO / similar object detection model).

Backend: Python / FastAPI or similar for API servicing.

Real-Time Alerts: Webhooks, messaging APIs, push integrations.

Frontend: Optional dashboard UI for monitoring, logs, and alerts.

(Stack details extrapolated from common GuardianEye-AI implementations.)
