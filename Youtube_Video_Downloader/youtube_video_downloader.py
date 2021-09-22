# For http requests
import requests
# Scraping Video url from Youtube
from pytube import YouTube
# For Merging two audio and video files
import moviepy.editor as mpe
# For Downloading Video
from urllib.request import urlretrieve
# for argument parsing
import sys
import os

# Exception Handling
if len(sys.argv) >1:
    url = sys.argv[1]
    resolution = sys.argv[2]
else:
    sys.exit("Please Enter the Youtube Video URL and required resolution")

# Function to Merge Audio and Video Files
def merge_audio_video(video_download_path, audio_download_path, output_file_path):
	clip = mpe.VideoFileClip(video_download_path)
	audio_bg = mpe.AudioFileClip(audio_download_path)
	final_clip =clip.set_audio(audio_bg)
	return final_clip.write_videofile(output_file_path)

# Checking the Video Availability
video = YouTube(url)
video.check_availability()
resolutions = {}

# Getting all video resolutions
for stream in video.streams.filter(adaptive=True):
    resolutions[stream.resolution] = stream.resolution

print(resolutions)
if resolution in resolutions.keys():
    print("Downloading Video ...")
    video_download_path = YouTube(url).streams.filter(res=resolution).first().download('./video')
    vid_name = video_download_path.split("\\")[-1]
    print("Downloading Audio ...")
    audio_download_path = YouTube(url).streams.filter(only_audio=True).first().download('./audio')
    out = './downloads' + vid_name
    merge_audio_video(video_download_path, audio_download_path, out)
else:
    raise ValueError("Provided Resolution is not available")
os.remove(audio_download_path)
os.remove(video_download_path)
print("Download Done.")