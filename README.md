# 🎥 EliteTube Downloader

A modern, highly interactive web application built with Python (Flask) that allows users to download and convert YouTube videos to either **MP4 (Video)** or **MP3 (Audio)** format.

The core downloading functionality is powered by the robust `yt-dlp` library.

## ✨ Features

* **Interactive UI:** Elegant and responsive interface using Bootstrap 5 with custom hover effects and a clean design.
* **Format Selection:** Download videos as MP4 or convert them to MP3 audio.
* **Robust Core:** Utilizes `yt-dlp` for reliable, high-quality media extraction.
* **Temporary Cleanup:** Automatically cleans up temporary files after each successful download.

## 🛠️ Setup and Installation

### 1. Prerequisites

You must have **Python 3** and **FFmpeg** installed on your system.

* **Python:** Ensure Python is installed and available in your command line.
* **FFmpeg:** This is **required** for MP3 conversion. Download and install it, ensuring the `ffmpeg` executable is added to your system's PATH.

### 2. Project Setup

1.  **Clone or Download** the project files.
2.  **Navigate** to the project directory in your terminal.
3.  **Install** the required Python libraries:
    ```bash
    pip install Flask yt-dlp
    ```

### 3. Running the Application

Start the Flask development server:
```bash
python app.py
