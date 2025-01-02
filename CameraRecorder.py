import os
import threading
import time
import pytz
from datetime import datetime
from picamera2 import Picamera2, Preview
import cv2

class VideoRecorder:
    def __init__(self):
        self.cameras = []  # Store Picamera2 instances
        self.fps = 30
        self.recording_threads = []
        self.is_recording = False
        self.output_dir = None
        self.recording_start_time = None
        self.stop_flag = False  # Flag to control stop recording

    def initialize_cameras(self):
        """Initialize CSI cameras."""
        self.cameras = []  # Reset cameras list each time
        for i in range(2):  # Assume there are two cameras (0 and 1)
            try:
                camera = Picamera2(camera_num=i)
                camera.configure(camera.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"}))
                self.cameras.append(camera)
            except Exception as e:
                print(f"Failed to initialize camera {i}: {e}")
                return False  # Indicate failure to initialize cameras
        return True  # Cameras initialized successfully

    def start_recording(self):
        if self.is_recording:
            print("Recording is already in progress.")
            return

        if len(self.cameras) < 2:
            print("Not enough cameras available.")
            return

        # Create timestamped folder for saving videos
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.output_dir = os.path.join("videos", timestamp)
        os.makedirs(self.output_dir, exist_ok=True)

        self.is_recording = True
        self.recording_start_time = time.time()  # Record the start time
        self.stop_flag = False  # Reset the stop flag

        # Start recording threads for each camera
        for i, camera in enumerate(self.cameras):
            thread = threading.Thread(target=self._record, args=(i, camera))
            self.recording_threads.append(thread)
            camera.start()
            thread.start()

        print(f"Recording started. Videos will be saved to: {self.output_dir}")

    def _record(self, index, camera):
        # Configure video writer
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_in.mp4" if index == 0 else f"{timestamp}_out.mp4"
        output_path = os.path.join(self.output_dir, filename)

        frame_size = (1280, 720)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, frame_size)

        while self.is_recording and not self.stop_flag:
            frame = camera.capture_array()
            time.sleep(0.01)

            # Add timestamp to the frame
            taipei_timezone = pytz.timezone('Asia/Taipei')
            taipei_time = datetime.now(taipei_timezone)
            timestamp_text = taipei_time.strftime("%Y/%m/%d %H:%M:%S")
            cv2.putText(frame, timestamp_text, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))  # Convert RGB to BGR for OpenCV

            # Check if 10 seconds have passed
            if time.time() - self.recording_start_time >= 10:
                self.stop_flag = True  # Stop the recording

        camera.stop()
        out.release()

    def stop_recording(self):
        if not self.is_recording:
            print("No recording in progress.")
            return

        # Set the stop flag to stop all recording threads
        self.stop_flag = True
        self.is_recording = False

        for thread in self.recording_threads:
            if thread.is_alive():
                thread.join()  # Ensure all threads finish

        print("Recording stopped.")
        
        # Re-initialize cameras for the next round
        #self.initialize_cameras()

        # Return the folder and filenames of the saved videos
        return self.output_dir
    
if __name__ == "__main__":
    # Create VideoRecorder instance
    recorder = VideoRecorder()

    # Ensure cameras are initialized
    recorder.initialize_cameras()

    # Start recording
    recorder.start_recording()

    # Wait for 12 seconds to ensure recording has started and then stop recording
    time.sleep(5)

    # Stop recording and get the saved folder and filenames
    saved_folder = recorder.stop_recording()
    
    
    # Start recording
    recorder.start_recording()
    # Wait for 12 seconds to ensure recording has started and then stop recording
    time.sleep(5)

    # Stop recording and get the saved folder and filenames
    saved_folder = recorder.stop_recording()
    print(saved_folder)
