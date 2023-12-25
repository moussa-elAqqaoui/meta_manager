# YouTube Video Processing Script

## Overview

This Python script is designed to process YouTube video information stored in a Google Sheet. It downloads audio, an associated image, and creates a video with optional text overlay based on the provided data.

## Prerequisites

- Python 3.x
- Dependencies (install using 'pip install -r requirements.txt'):
  - pytube
  - pydub
  - gspread
  - google-auth
  - requests
  - Pillow
  - moviepy

## Setup

1. Clone the repository:
   git clone https://github.com/yourusername/your-repo.git

2. Install dependencies:
   pip install -r requirements.txt

3. Obtain Google Sheets API credentials:
   - Follow the instructions in the gspread documentation to create a service account and download the credentials JSON file.
   - Save the credentials file as 'credentials.json' in the project directory.

4. Customize the Google Sheet:
   - Create a Google Sheet with the necessary columns (YouTube Video URL, Start Time, End Time, Image URL, Text for Video, etc.).
   - Share the Google Sheet with the email address specified in the service account's credentials.

## Usage

1. Populate your Google Sheet with video information.
2. Run the script:
   python process_videos.py
3. The script will download audio, images, and create videos based on the provided information.

## Configuration

- Customize the script by modifying constants in 'process_videos.py', such as output directory, font size, etc.
- Adjust the Google Sheet column names as needed.

## Notes

- Ensure that the Google Drive API is enabled for your project. Follow the error messages if API issues arise.
- Be mindful of YouTube's usage policies when downloading videos.

## Acknowledgments

- This script uses the following libraries:
  - pytube for YouTube video downloading.
  - gspread for Google Sheets interaction.
  - google-auth for authentication.
  - pydub, Pillow, moviepy for audio and video processing.
