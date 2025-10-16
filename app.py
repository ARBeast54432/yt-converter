from flask import Flask, render_template, request, send_file
import os
import shutil # Used for directory cleanup

# Import the core logic module
from converter import download_video, DOWNLOAD_FOLDER

# 1. Initialize the Flask application
app = Flask(__name__)

# A simple list to hold messages (success or error)
MESSAGES = []

# 2. Define the main route (Handles GET for showing form, and POST for processing)
@app.route('/', methods=['GET', 'POST'])
def index():
    global MESSAGES
    
    if request.method == 'POST':
        # --- A. Process the Form Submission ---
        
        # 1. Get user input from the form
        url = request.form.get('url')
        output_format = request.form.get('format')
        
        # **DEBUGGED URL VALIDATION:** Check for common YouTube domains (youtube.com OR youtu.be)
        if not url or ('youtube.com' not in url and 'youtu.be' not in url):
            MESSAGES.append(('error', "Invalid URL. Please enter a proper YouTube link."))
            # Render the template with the error message
            return render_template('index.html', messages=MESSAGES)

        # 2. Call the core download logic
        filename, result_path = download_video(url, output_format)
        
        if filename:
            # 3. SUCCESS: Prepare the file for download (Final functionality)
            # The download function is called, which initiates the file download to the user's browser
            
            # Immediately send the file for download
            try:
                # Determine correct MIME type
                mime_type = 'video/mp4' if output_format == 'mp4' else 'audio/mpeg'
                
                # We use as_attachment=True to force the browser to download the file
                response = send_file(
                    result_path, 
                    as_attachment=True,
                    download_name=filename,
                    mimetype=mime_type
                )
                
                # After the file is sent, we must ensure it is cleaned up. 
                # This is tricky in Flask, but the tear-down hook covers most cases.
                
                # To show a message after the download completes (which is often missed 
                # because send_file is a return), we redirect back to the home page 
                # with a success message appended, but this is an advanced pattern 
                # that requires session/flash messages. For simplicity, we just return the file.
                
                return response

            except Exception as e:
                # If file serving fails (e.g., file disappeared during transfer), report it
                MESSAGES.append(('error', f"Error serving file: {e}. Please try again."))
                
        else:
            # 4. FAILURE: The converter returned an error message (result_path contains the error string)
            MESSAGES.append(('error', f"Download failed: {result_path}"))


    # --- B. Handle the GET request or Re-render after POST failure ---
    
    # We clear the messages after rendering to prevent them from persisting on refresh
    current_messages = MESSAGES[:]
    MESSAGES = [] 
    
    # Render the index page, passing any collected messages
    return render_template('index.html', messages=current_messages)

# --- CLEANUP HOOK ---
# Recommended cleanup function that runs when the app is shut down or occasionally
@app.teardown_appcontext
def cleanup_temp_folder(exception=None):
    """Clean up the contents of the temporary download folder when the application context ends."""
    if os.path.exists(DOWNLOAD_FOLDER):
        try:
            # Safely delete all files and subdirectories within the temporary folder
            for item in os.listdir(DOWNLOAD_FOLDER):
                item_path = os.path.join(DOWNLOAD_FOLDER, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
        except Exception as e:
            # Log the error, but don't crash the application
            print(f"Error during cleanup of {DOWNLOAD_FOLDER}: {e}")


# 3. Entry point to run the application
if __name__ == '__main__':
    # Cleanup on startup for safety
    cleanup_temp_folder() 
    app.run(debug=True)