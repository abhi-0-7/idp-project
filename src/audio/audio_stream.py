import requests
import struct
import numpy as np
import threading
import time

class AudioProcessor:
    def __init__(self, ip_url="http://10.177.52.9:8080"):
        self.ip_url = ip_url
        self.audio_url = f"{self.ip_url}/audio.wav"
        self.current_volume = 0.0
        self.current_state = "NORMAL"
        self.is_running = False
        self.thread = None

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._process_stream, daemon=True)
            self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join()

    def _process_stream(self):
        print(f"Connecting to IP Webcam audio stream at {self.audio_url}...")
        while self.is_running:
            try:
                # Start streaming the request
                response = requests.get(self.audio_url, stream=True, timeout=5)
                response.raise_for_status()
                
                # Skip header
                _ = response.raw.read(44)
                chunk_size = 1024  # Smaller chunk for faster real-time processing
                
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if not self.is_running:
                        break
                        
                    if len(chunk) < chunk_size:
                        continue
                        
                    try:
                        audio_data = struct.unpack(f"<{len(chunk)//2}h", chunk)
                        audio_array = np.array(audio_data, dtype=np.float64)
                        volume = np.sqrt(np.mean(audio_array**2)) if len(audio_array) > 0 else 0
                        
                        # Scale volume: Multiply by 5 for sensitivity, cap at 100
                        raw_vol = (volume / 32768.0) * 100 * 5
                        self.current_volume = min(100.0, raw_vol)
                        
                        self.current_state = "PANIC" if self.current_volume > 30 else "NORMAL"
                    except struct.error:
                        pass

            except requests.exceptions.RequestException:
                print("Error connecting to audio stream. Retrying in 2 seconds...")
                time.sleep(2)

    def get_data(self):
        return {
            "volume": round(self.current_volume, 2),
            "state": self.current_state
        }

audio_processor = AudioProcessor()
