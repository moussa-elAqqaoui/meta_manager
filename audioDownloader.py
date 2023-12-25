from pytube import YouTube
import datetime
import os
import gspread
from google.auth import exceptions
from google.oauth2 import service_account
import requests
from PIL import Image
from io import BytesIO
from pydub import AudioSegment
from moviepy.editor import AudioFileClip, ImageClip

def rename_mp4_files(directory_path, new_filename="audio.mp4"):
    """
    Rename all files with ".mp4" extension in the specified directory
    to have the given new filename.

    Parameters:
    - directory_path (str): The path to the directory containing the files.
    - new_filename (str): The new filename (default is "audio.mp4").
    """
    for filename in os.listdir(directory_path):
        if filename.endswith(".mp4"):
            old_filepath = os.path.join(directory_path, filename)
            new_filepath = os.path.join(directory_path, new_filename)

            try:
                os.rename(old_filepath, new_filepath)
                print(f"File renamed from {filename} to {new_filename}")
            except Exception as e:
                print(f"Error renaming file {filename}: {e}")


def download_audio(youtube_url, start_time, end_time, output_path=""):
    try:
        yt = YouTube(youtube_url)
        
        # Set the video stream to download audio only
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download the audio
        output_file = "audio.mp4"
        if output_path:
            output_file = os.path.join(output_path, output_file)

        print(f"Downloading audio from {youtube_url}...")
        audio_stream.download(output_path=output_path)

        rename_mp4_files("./")

        # Convert webm to mp3
        mp3_output_file = output_file.replace(".mp4", ".mp3")
        AudioSegment.from_file(output_file).export(mp3_output_file, format="mp3")

        # Trim the audio to the specified range
        audio = AudioSegment.from_file(mp3_output_file, format="mp3")
        trimmed_audio = audio[start_time * 1000:end_time * 1000]

        # Save the trimmed audio
        trimmed_audio.export(mp3_output_file, format="mp3")

        # Remove the original downloaded file (untrimmed)
        os.remove(output_file)

        print("Download and trim completed successfully.")

    except Exception as e:
        print(f"Error: {e}")


def download_image(image_url, output_path=""):
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        # Save the image locally
        image_file = "photo.png"
        if output_path:
            image_file = os.path.join(output_path, image_file)

        image.save(image_file)
        print(f"Image saved at: {image_file}")

        return image_file
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def create_video(audio_file, image_path, output_path="output_video.mp4", fps=24):
    audio_clip = AudioFileClip(audio_file)
    image_clip = ImageClip(image_path, duration=audio_clip.duration)

    # Set the resolution of the video to match the image
    video_clip = image_clip.set_audio(audio_clip)
    video_clip = video_clip.set_duration(audio_clip.duration)
    video_clip = video_clip.set_fps(fps)

    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile="temp.m4a", remove_temp=True)

def get_credentials(credentials_file):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"],
        )
        return gspread.Client(auth=credentials)
    except exceptions.GoogleAuthError as e:
        print(f"Error getting credentials: {e}")
        return None


def read_google_sheet(credentials_file, spreadsheet_name, worksheet_name):
    gc = get_credentials(credentials_file)
    spreadsheet = gc.open(spreadsheet_name)
    worksheet = spreadsheet.worksheet(worksheet_name)
    data = worksheet.get_all_records()
    return data

def get_todays_date():
    return datetime.datetime.now().strftime("%m/%d/%Y")

if __name__ == "__main__":

    credentials_file = "./glass-episode-363010-b4ea53d51b67.json"
    spreadsheet_name = "insta_content"
    worksheet_name = "data"

    sheet_data = read_google_sheet(credentials_file, spreadsheet_name, worksheet_name)

    for row in sheet_data:
        video_url = row["video_url"]
        start_time = int(row["start_time"])
        end_time = int(row["end_time"])
        image_url = row["image_url"]
        row_date = row["the_date"]

        if row_date == get_todays_date():
            download_audio(video_url, start_time, end_time)
            download_image(image_url)
            create_video("audio.mp3", "./photo.png")