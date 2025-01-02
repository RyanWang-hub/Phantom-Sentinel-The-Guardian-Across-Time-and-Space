import time
from CameraRecorder import VideoRecorder  # Assume VideoRecorder is in the same directory or proper module path
from LineVideoMessenger import process_videos  # Import the method from LineService
import shutil
import os

class ThiefOut:
    def __init__(self):
        self.recorder = VideoRecorder()
        
        # Ensure cameras are initialized before starting recording
        self.recorder.initialize_cameras()

    def start_and_stop_recording(self):
        ## Ensure cameras are initialized before starting recording
        #self.recorder.initialize_cameras()

        # Start recording
        self.recorder.start_recording()

        # Wait for 12 seconds to ensure recording has started and then stop recording
        time.sleep(12)

        # Stop recording and get the saved folder and filenames
        saved_folder = self.recorder.stop_recording()
        return saved_folder

    def clear_folder(self, path):  # Use self to refer to the method within the class
        # Ensure the folder exists
        if os.path.exists(path) and os.path.isdir(path):
            # Get all subfolders and files in the directory
            all_folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            
            # Sort the folders by modification time (newest first)
            all_folders.sort(key=lambda f: os.path.getmtime(os.path.join(path, f)), reverse=True)
            
            # Keep the most recent 5 folders
            folders_to_delete = all_folders[5:]  # Folders to delete, keep the first 5
            
            # Delete old folders and their contents
            for folder in folders_to_delete:
                folder_path = os.path.join(path, folder)
                shutil.rmtree(folder_path)  # Delete the folder and its contents
                print(f"Deleted folder: {folder_path}")
            
            print(f"Kept the most recent 5 folders in '{path}'.")
        else:
            print(f"The path '{path}' does not exist or is not a directory.")

# Example usage
if __name__ == "__main__":
    thief_out = ThiefOut()

    # Start and stop recording
    saved_folder = thief_out.start_and_stop_recording()
    print(f"Videos saved in: {saved_folder}")
    
    
    # Start and stop recording
    saved_folder = thief_out.start_and_stop_recording()
    print(f"Videos saved in: {saved_folder}")

    # Call the process_videos method to process videos in the folder
    #process_videos(saved_folder)
    
    # Delete all files and subfolders inside the folder
    thief_out.clear_folder("/home/user/project/videos")
