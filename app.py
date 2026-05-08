from flask import Flask, render_template, Response, jsonify, request
from flask_cors import CORS
from src.vision.video_stream import video_processor
from src.audio.audio_stream import audio_processor
import os

# Set template and static folder explicitly if needed
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

@app.before_request
def start_background_threads():
    # Only start once
    if not hasattr(app, 'background_started'):
        audio_processor.start()
        app.background_started = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_processor.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/metrics')
def get_metrics():
    v_metrics = video_processor.get_metrics()
    a_metrics = audio_processor.get_data()
    
    # Calculate combined risk
    risk = "LOW"
    if v_metrics["density"] == "HIGH" and a_metrics["state"] == "PANIC":
        risk = "CRITICAL"
    elif v_metrics["density"] == "HIGH" or a_metrics["state"] == "PANIC":
        risk = "HIGH"
    elif v_metrics["density"] == "MEDIUM":
        risk = "MEDIUM"
        
    return jsonify({
        "vision": v_metrics,
        "audio": a_metrics,
        "risk": risk
    })

@app.route('/api/set_model', methods=['POST'])
def set_model():
    data = request.json
    model_name = data.get('model', 'yolov10n.pt')
    video_processor.set_model(model_name)
    return jsonify({"status": "success", "model": model_name})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
