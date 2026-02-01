# Merge-Conflict
This is our Hackathon repository in which we have trained a ML Model which detects helmets in the pictures clicked by the cameras on the traffic lights

GuardianEye-AI

AI-Powered Threat Detection & Surveillance Platform

GuardianEye-AI is a cutting-edge artificial intelligence system designed to enhance safety and threat detection in real-time. Using advanced machine learning and computer vision, GuardianEye autonomously monitors environments, detects threats, alerts users instantly, and supports proactive response workflows.

Key Features

Real-Time Threat Detection: Uses AI vision models to detect predefined threat actions and behaviors instantly.

Live Monitoring & Alerts: Recognizes risks as they occur and streams alerts with contextual metadata.

Incident Logging: Automatically records incidents with timestamps and severity details.

Automated Notifications: Integrated alerting via chat services or custom APIs.

Easy Integration: Lightweight backend ready for web/mobile service hooks.
(This feature set is based on typical functionality for real-time AI surveillance systems like GuardianEye-AI)

How It Works

Video Capture & Feed Processing
Camera or video input is processed in real time to extract frames suitable for analysis.

AI Inference Engine
Deep learning models analyze frames to spot traffic violation especially.

Detection Filtering
Alerts are filtered and scored to reduce false positives and highlight critical events.

Notifications & Logging
Once a rule violation is recognized, incidents are logged and alerts are pushed to the configured channel.

(This workflow reflects standard real-time CV + ML processing architectures.)

Tech Stack

Computer Vision: Deep learning (YOLO / similar object detection model).

Backend: Python / FastAPI .

GuardianEye-AI 

Real-Time Helmet Detection & Traffic Rule Violation System
Hackathon Project — Computer Vision + Deep Learning

Overview

GuardianEye-AI is a real-time helmet compliance detection system built to identify motorcyclists violating helmet laws using live video feeds. The model processes frames from CCTV/road cameras, detects riders without helmets, and flags violations for downstream action such as logging, alerting, or challan generation.

This project uses a state-of-the-art object detector tuned for helmet/no-helmet classification, optimized for speed and accuracy in traffic scenarios.

---

Features-

Detects motorcycles and riders in video streams  
Classifies helmet vs. no-helmet status  
Marks and logs violations with timestamps  
Outputs cropped violator images for review  
Real-time performance (~28 FPS on GPU / optimized CPU)  

Real-Time Alerts: messaging APIs, push integrations.

Frontend: Optional dashboard UI for monitoring, logs, and alerts.


