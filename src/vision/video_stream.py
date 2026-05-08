import cv2
import time
import threading
from ultralytics import YOLO

class VideoProcessor:
    def __init__(self, ip_url="http://10.177.52.9:8080"):
        self.ip_url = ip_url
        self.video_url = f"{self.ip_url}/video"
        self.model_name = "yolov10n.pt"
        self.model = YOLO(self.model_name)
        
        self.latest_frame = None
        self.latest_boxes = []
        self.lock = threading.Lock()
        
        # Metrics
        self.current_fps = 0.0
        self.current_inference_time = 0.0
        self.current_count = 0
        self.current_density = "LOW"
        
        self.is_running = False
        
    def start(self):
        if not self.is_running:
            self.is_running = True
            threading.Thread(target=self._capture_thread, daemon=True).start()
            threading.Thread(target=self._inference_thread, daemon=True).start()

    def set_model(self, model_name):
        # Load the new model FIRST without locking, so the video stream doesn't freeze
        new_model = YOLO(model_name)
        
        # Now quickly swap the reference
        with self.lock:
            self.model_name = model_name
            self.model = new_model
            
    def _capture_thread(self):
        # We use cv2.CAP_FFMPEG or just default, but buffer size 1 is crucial to drop old frames
        cap = cv2.VideoCapture(self.video_url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        while self.is_running:
            ret, frame = cap.read()
            if ret:
                self.latest_frame = frame
            else:
                time.sleep(0.01)
                cap.open(self.video_url)
                
    def _inference_thread(self):
        while self.is_running:
            if self.latest_frame is None:
                time.sleep(0.01)
                continue
                
            frame_to_infer = self.latest_frame.copy()
            
            # Get a local reference to the model so we don't lock while predicting
            with self.lock:
                current_model = self.model
            
            # Predict OUTSIDE the lock to prevent blocking the video stream!
            results = current_model.predict(frame_to_infer, classes=[0], verbose=False, imgsz=320)
            result = results[0]
            
            inference_time_ms = result.speed['inference'] if hasattr(result, 'speed') else 0.0
            person_count = len(result.boxes)
            
            if person_count > 20:
                density = "HIGH"
            elif person_count > 10:
                density = "MEDIUM"
            else:
                density = "LOW"
                
            # Extract boxes to draw later
            boxes = []
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                boxes.append((int(x1), int(y1), int(x2), int(y2)))
            
            # Update the shared variables INSIDE a tiny, fast lock
            with self.lock:
                self.latest_boxes = boxes
                self.current_inference_time = inference_time_ms
                self.current_count = person_count
                self.current_density = density
                
    def generate_frames(self):
        self.start()
        prev_time = time.time()
        
        while True:
            if self.latest_frame is None:
                time.sleep(0.01)
                continue
                
            frame = self.latest_frame.copy()
            
            # Draw latest boxes (they might be slightly behind the frame, but video remains 30fps)
            with self.lock:
                boxes_to_draw = self.latest_boxes.copy()
                density = self.current_density
                
            color = (0, 255, 0)
            if density == "HIGH": color = (0, 0, 255)
            elif density == "MEDIUM": color = (0, 255, 255)
                
            for x1, y1, x2, y2 in boxes_to_draw:
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time
            self.current_fps = fps
            
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # Target 30 FPS output (33ms delay)
            time.sleep(1/30)
            
    def get_metrics(self):
        return {
            "fps": round(self.current_fps, 1),
            "inference_time_ms": round(self.current_inference_time, 1),
            "person_count": self.current_count,
            "density": self.current_density,
            "model": self.model_name
        }

video_processor = VideoProcessor()
