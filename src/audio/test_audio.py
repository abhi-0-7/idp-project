import numpy as np
import requests
import time
import struct

def test_audio_ipwebcam(ip_url="http://192.168.1.10:8080", duration=10):
    """
    Test the microphone by streaming audio from the Mobile IP Webcam.
    Args:
        ip_url (str): The base URL of the IP Webcam.
        duration (int): Duration in seconds to test.
    """
    audio_url = f"{ip_url}/audio.wav"
    print(f"Connecting to IP Webcam audio stream at {audio_url}...")
    print(f"Testing audio for {duration} seconds. Please make noise near the mobile...")
    
    try:
        # Start streaming the request
        response = requests.get(audio_url, stream=True, timeout=5)
        response.raise_for_status()
        
        start_time = time.time()
        
        # IP Webcam audio.wav is typically 16-bit PCM, mono, 8000Hz or 44100Hz
        # The first 44 bytes are the WAV header, we skip them roughly by just reading stream
        
        # Skip header
        header = response.raw.read(44)
        
        chunk_size = 2048 # Number of bytes to read at a time
        
        for chunk in response.iter_content(chunk_size=chunk_size):
            if time.time() - start_time > duration:
                break
                
            if len(chunk) < chunk_size:
                continue
                
            # Convert bytes to 16-bit integers
            # 'h' is 2 bytes (16-bit), so 2048 bytes = 1024 integers
            try:
                audio_data = struct.unpack(f"<{len(chunk)//2}h", chunk)
                
                # Calculate RMS volume
                audio_array = np.array(audio_data, dtype=np.float64)
                volume = np.sqrt(np.mean(audio_array**2)) if len(audio_array) > 0 else 0
                
                # Normalize or scale volume for display
                # A 16-bit integer ranges from -32768 to 32767
                volume_scaled = (volume / 32768.0) * 100
                
                # Determine a simple state
                state = "PANIC" if volume_scaled > 30 else "NORMAL"
                
                print(f"Volume: {volume_scaled:5.2f}% | State: {state}")
                
            except struct.error:
                pass
                
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to audio stream: {e}")
        print("Please check the IP address and make sure the IP Webcam server is running.")
        
    print("Audio test finished.")

if __name__ == "__main__":
    # You can change the IP here
    IP_WEBCAM_URL = "http://192.168.1.10:8080"
    test_audio_ipwebcam(IP_WEBCAM_URL, duration=20)
