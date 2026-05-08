# AI-Based Predictive Crowd Congestion and Panic Alert System

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-Flask-lightgrey.svg" alt="Flask Framework">
  <img src="https://img.shields.io/badge/ML-YOLOv10%2Fv11-red.svg" alt="YOLO ML">
  <img src="https://img.shields.io/badge/Hardware-FPGA%20Integrated-orange.svg" alt="FPGA Integrated">
  <img src="https://img.shields.io/badge/Status-Active-green.svg" alt="Project Status">
</div>

## 📌 Project Overview
This repository contains the source code for the IDP project: **AI-Based Predictive Crowd Congestion and Panic Alert System Using Multi-Sensor Fusion with FPGA**. 

The system leverages state-of-the-art computer vision (YOLOv10/v11) and real-time audio analysis to monitor crowd density and detect panic situations. By fusing multi-sensor data, the system provides a robust predictive alert mechanism designed for deployment on FPGA for low-latency edge computing.

## 🚀 Key Features
- **Real-time Crowd Density Estimation**: Utilizing YOLOv10 and YOLOv11 for high-accuracy person detection.
- **Audio-Based Panic Detection**: Monitoring sound intensity and frequency patterns to identify abnormal crowd behavior.
- **Multi-Sensor Fusion**: Combining vision and audio metrics for a comprehensive risk assessment.
- **FPGA Integration**: Optimized for low-latency processing at the edge.
- **Live Dashboard**: A Flask-based web interface for real-time monitoring and model switching.

## 🛠️ Tech Stack
- **Backend**: Flask, Python
- **Computer Vision**: OpenCV, Ultralytics (YOLOv10/v11)
- **Audio Processing**: NumPy, SoundDevice, Requests
- **Hardware Integration**: FPGA (Verilog/HLS)

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/abhi-0-7/idp-project.git
cd idp-project
```

### 2. Environment Setup
It is recommended to use a virtual environment:
```bash
# Create venv
python -m venv venv

# Activate venv (Windows)
.\venv\Scripts\activate

# Activate venv (Linux/Mac)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Model Weights
Place the YOLO weights (`yolov10n.pt`, `yolo11n.pt`, etc.) in the root directory. (Note: These are gitignored due to size).

## 🚦 Usage

### Running the Dashboard
Start the Flask application to access the web-based monitoring interface:
```bash
python app.py
```
Access the dashboard at `http://localhost:5000`.

### Standalone Module Testing

**Vision Module Test**
To test the video feed and detection logic:
```bash
python src/vision/test_camera.py
```

**Audio Module Test**
To test the microphone and sound intensity calculation:
```bash
python src/audio/test_audio.py
```

## 📊 Project Structure
```text
├── src/
│   ├── vision/        # Video processing and crowd detection
│   ├── audio/         # Audio stream analysis and panic detection
│   └── ml/            # Model management and optimization
├── templates/         # HTML Dashboard files
├── static/            # CSS, JS, and Assets
├── app.py             # Main Flask Application
├── requirements.txt   # Project Dependencies
└── README.md          # Project Documentation
```

---
<div align="center">
  Developed by <b>Abhishek</b>
</div>
