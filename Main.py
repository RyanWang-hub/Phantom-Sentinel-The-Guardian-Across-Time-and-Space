import RPi.GPIO as GPIO
import time
from ThiefOutMonitor import ThiefOut
from LineVideoMessenger import process_videos  # Import the method from LineService

trigger_pin = 23
echo_pin = 24

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# Function to calculate distance
def send_trigger_pulse():
    GPIO.output(trigger_pin, True)
    time.sleep(0.01)
    GPIO.output(trigger_pin, False)

def wait_for_echo(value, timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count > 0:
        count -= 1

def get_distance():
    send_trigger_pulse()
    wait_for_echo(True, 5000)
    start = time.time()
    wait_for_echo(False, 5000)
    finish = time.time()
    pulse_len = finish - start
    distance_cm = pulse_len * 340 * 100 / 2
    return distance_cm

# Set initial distance value
previous_distance = None
threshold = 3  # Set distance change threshold (in cm)

# Initialize ThiefOutMonitor
thief_out = ThiefOut()

# Flag to prevent multiple entries into recording logic
processing_flag = False

while True:
    dist = get_distance()
    if previous_distance is not None:
        # If the current distance differs from the previous one by more than the threshold, print change
        if dist - previous_distance > threshold and not processing_flag:
            print(f"Distance changed! previous_distance: {previous_distance:.2f} cm, New distance: {dist:.2f} cm")
            
            # Set flag to indicate that recording is in progress
            processing_flag = True
            
            # Trigger ThiefOutMonitor functionality
            saved_folder = thief_out.start_and_stop_recording()
            if saved_folder:
                print(f"ThiefOutMonitor videos saved in: {saved_folder}")
                
                process_videos(saved_folder)
                # Process and clear folder after recording
                thief_out.clear_folder("/home/user/project/videos")
            else:
                print("Recording failed. No folder returned.")
            
            # Reset flag after processing
            processing_flag = False

        if dist - previous_distance < threshold * -1:
            print(f"Distance changed! previous_distance: {previous_distance:.2f} cm, New distance: {dist:.2f} cm")
            
    else:
        print(f"Initial distance: {dist:.2f} cm")

    # Update previous distance
    previous_distance = dist
    
    time.sleep(1)
