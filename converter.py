import os
import re
import subprocess
import json
from yt_dlp import YoutubeDL

# Define the temporary folder where downloaded files will be stored
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Helper function to sanitize titles for safe filenames
def sanitize_title(title):
    # Remove special characters and replace spaces with hyphens
    s = re.sub(r'[^\w\s-]', '', title).strip()
    return re.sub(r'[-\s]+', '-', s)

def download_video(url, output_format='mp4'):
    """
    Downloads the YouTube video stream using yt-dlp, converts it, and saves it.
    
    Args:
        url (str): The full YouTube URL.
        output_format (str): 'mp4' or 'mp3'.
        
    Returns:
        tuple: (filename, filepath) if successful, (None, error_message) otherwise.
    """
    try:
        # Step 1: Extract Video Metadata to get the title
        # DEBUG: quiet is set to False to display verbose errors
        ydl_opts_meta = {'quiet': True, 'skip_download': True, 'force_generic_extractor': True}
        with YoutubeDL(ydl_opts_meta) as ydl:
            info = ydl.extract_info(url, download=False)
            title = sanitize_title(info.get('title', 'video'))

        # Determine output paths
        output_template = os.path.join(DOWNLOAD_FOLDER, f'{title}.%(ext)s')

        # Step 2: Configure the download options based on format
        if output_format == 'mp4':
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': output_template,
                'merge_output_format': 'mp4',
                'quiet': False, # DEBUG: quiet is set to False
                # yt-dlp automatically handles remuxing video and audio streams
            }
            final_filename = f"{title}.mp4"
            
        elif output_format == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192', # High quality audio
                }],
                'quiet': False, # DEBUG: quiet is set to False
                # NOTE: This requires the external FFmpeg tool for conversion!
            }
            final_filename = f"{title}.mp3"
        
        else:
            return None, "Unsupported output format."

        # Step 3: Execute the download
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        final_filepath = os.path.join(DOWNLOAD_FOLDER, final_filename)
        
        # A quick check to see if the file exists (yt-dlp is usually reliable)
        if os.path.exists(final_filepath):
            return final_filename, final_filepath
        else:
            # Fallback for when the file is saved with a different extension
            for f in os.listdir(DOWNLOAD_FOLDER):
                if f.startswith(title) and (f.endswith('.mp4') or f.endswith('.mp3')):
                     return f, os.path.join(DOWNLOAD_FOLDER, f)
            return None, "Download appeared successful, but final file could not be located."


    except Exception as e:
        # Check if the error is due to missing FFmpeg
        if "No ffmpeg" in str(e):
             return None, "Missing dependency: FFmpeg is required for MP3 conversion. Please install FFmpeg."
        return None, f"An unexpected error occurred during download: {e}"

# --- For Unit Testing Only ---
if __name__ == '__main__':
    # Using a known stable YouTube URL for testing
    TEST_URL = "https://youtu.be/lttH8yO5pdE?si=vpRmbpZUy4U1nFeE" # Stable test URL 
    # If the user's provided URL is known to be stable, you can use that one too:
    # TEST_URL = "https://youtu.be/lttH8yO5pdE?si=vpRmbpZUy4U1nFeE"
    
    print(f"--- Running Dependency Check & Testing MP4 Download ---")
    mp4_filename, mp4_result = download_video(TEST_URL, 'mp4')
    if mp4_filename:
        print(f"✅ MP4 Download SUCCESS: File saved as {mp4_filename}")
        os.remove(mp4_result) # Clean up the test file
    else:
        print(f"❌ MP4 Download FAILED: {mp4_result}")

    print(f"\n--- Running Dependency Check & Testing MP3 Download ---")
    mp3_filename, mp3_result = download_video(TEST_URL, 'mp3')
    if mp3_filename:
        print(f"✅ MP3 Download SUCCESS: File saved as {mp3_filename}")
        os.remove(mp3_result) # Clean up the test file
    else:
        print(f"❌ MP3 Download FAILED: {mp3_result}")