import cv2
import time
from ultralytics import YOLO

def start_vision_module(ip_url="http://192.168.1.10:8080"):
    print("========================================")
    print(" Crowd Detection & Analysis Module ")
    print("========================================")
    print("Select YOLO Model:")
    print("1. YOLOv10 (yolov10n.pt)")
    print("2. YOLOv11 (yolo11n.pt)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    model_name = "yolov10n.pt" if choice == "1" else "yolo11n.pt"
    print(f"\nLoading {model_name}...")
    
    # Load the chosen model
    model = YOLO(model_name)
    print("Model loaded successfully!")
    
    video_url = f"{ip_url}/video"
    print(f"\nConnecting to IP Webcam video stream at {video_url}...")
    cap = cv2.VideoCapture(video_url)
    
    if not cap.isOpened():
        print("Error: Could not open video stream. Please check the IP address and make sure the IP Webcam server is running.")
        return

    # Variables for FPS calculation
    prev_frame_time = 0
    new_frame_time = 0

    print("Starting real-time detection. Press 'ESC' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
            
        # FPS calculation start
        new_frame_time = time.time()
        
        # Inference (predict only 'person' class which is class 0)
        results = model.predict(frame, classes=[0], verbose=False)
        result = results[0]
        
        # Calculate inference time in ms
        # result.speed is a dict: {'preprocess': ..., 'inference': ..., 'postprocess': ...}
        inference_time_ms = result.speed['inference'] if hasattr(result, 'speed') else 0.0
        
        person_count = len(result.boxes)
        
        # Density estimation logic
        if person_count > 20:
            density = "HIGH"
            color = (0, 0, 255) # Red
        elif person_count > 10:
            density = "MEDIUM"
            color = (0, 255, 255) # Yellow
        else:
            density = "LOW"
            color = (0, 255, 0) # Green
            
        # Draw bounding boxes
        annotated_frame = result.plot()
        
        # Calculate FPS
        fps = 1 / (new_frame_time - prev_frame_time) if (new_frame_time - prev_frame_time) > 0 else 0
        prev_frame_time = new_frame_time
        
        # Overlay Metrics on Frame
        cv2.putText(annotated_frame, f"Model: {model_name.replace('.pt', '')}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(annotated_frame, f"Inf Time: {inference_time_ms:.1f}ms", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)
        
        cv2.putText(annotated_frame, f"Count: {person_count}", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        cv2.putText(annotated_frame, f"Density: {density}", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        # Display the resulting frame
        cv2.imshow("Crowd Detection & Analysis", annotated_frame)
        
        # Press ESC to exit
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # You can change the IP here
    IP_WEBCAM_URL = "http://192.168.1.10:8080"
    start_vision_module(IP_WEBCAM_URL)
