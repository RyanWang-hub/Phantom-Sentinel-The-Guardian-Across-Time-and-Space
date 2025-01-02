import os
import requests
from linebot import LineBotApi
from linebot.models import VideoSendMessage
from io import BytesIO

# LINE Bot credentials
CHANNEL_ACCESS_TOKEN = '***************************************************'
USER_ID = '************************'  # Replace with the target user's LINE User ID

# Imgur credentials
IMGUR_CLIENT_ID = '********************'  # Replace with your actual Imgur Client ID

# Initialize LineBotApi
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

# Function to upload video to Imgur and return the URL
def upload_video_to_imgur(file_path):
    headers = {
        'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'
    }
    
    # Open the video file
    with open(file_path, 'rb') as video_file:
        files = {'video': video_file}
        url = 'https://api.imgur.com/3/upload'
        response = requests.post(url, headers=headers, files=files)

        # Check for successful upload
        if response.status_code == 200:
            data = response.json()
            # Get the video URL from the response
            video_url = data['data']['link']
            return video_url
        else:
            raise Exception(f"Failed to upload video to Imgur: {response.status_code} - {response.text}")

# Function to send video to LINE
def send_video_to_line(file_path):
    try:
        # Upload video to Imgur and get the URL
        video_url = upload_video_to_imgur(file_path)
        
        # Generate a preview image URL (optional)
        preview_image_url = "https://example.com/path/to/preview_image.jpg"  # Replace with your preview image URL
        
        # Send video message to the user
        message = VideoSendMessage(
            original_content_url=video_url,
            preview_image_url=preview_image_url
        )
        line_bot_api.push_message(USER_ID, message)

        print(f"Video sent to LINE: {file_path}")

    except Exception as e:
        print(f"Failed to send video via LINE: {e}")

# Function to process all videos in a folder
def process_videos(folder_path):
    if not os.path.isdir(folder_path):
        print(f"The provided path '{folder_path}' is not a valid directory.")
        return

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_path = os.path.join(folder_path, filename)
            print(f"Processing video: {video_path}")
            try:
                send_video_to_line(video_path)
            except Exception as e:
                print(f"Error processing video '{filename}': {e}")

# Example usage
if __name__ == "__main__":
    # Specify the folder containing videos
    video_folder = "/path/to/your/video/folder"
    process_videos(video_folder)

