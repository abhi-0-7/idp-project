import cv2

def test_camera(url=None):
    """
    Test the IP Webcam or default camera.
    Args:
        url (str): The IP Webcam URL (e.g., 'http://192.168.1.5:8080/video').
                   If None, it uses the default webcam (0).
    """
    source = url if url else 0
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Error: Could not open video stream from {source}")
        return

    print(f"Successfully connected to {source}. Press 'ESC' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        cv2.imshow("Camera Test - Press ESC to close", frame)

        # Press ESC to exit
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # To test IP Webcam, uncomment the line below and put your IP
    # ip_webcam_url = "http://192.168.1.X:8080/video"
    # test_camera(ip_webcam_url)
    
    # By default, tests the connected local webcam
    test_camera()
