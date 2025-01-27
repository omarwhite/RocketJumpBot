from Generation.vidgen import *
from dbtests import grabTestPost, grabTestVid
from audiogentest import *
from moviepy.editor import AudioFileClip 
import os

# Setting a path to the intended folder for the Youtube Video download
output_folder = "Input\\Test Input\\Videos\\"

# Grabbing video data
test_vid_data = grabTestVid()

# Getting time for filename
time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Testing the function that downloads the background video
'''
vid_file = downloadBackgroundVid(test_vid_data["snippet"]["resourceId"]["videoId"], 
                                 300, 
                                 output_folder, 
                                 time)
'''

# Testing the function that merges audio and video
testPost = grabTestPost()
comments = getTop10Comments(testPost["url"])
output_folder_voiceover = "Input\\Test Input\\Voiceovers\\"
output_folder_track = "Input\\Test Input\\Completed Tracks\\"
time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
test_music_file = "Input\\Music\\touch_and_go.mp3"
test_voiceover_file = f"{output_folder_voiceover}voiceover_{time}.mp3"

genVoiceover(testPost, comments, output_folder_voiceover, time)
finished_track = combineVoiceAndMusic(test_voiceover_file, 
                                      test_music_file, 
                                      output_folder_track, 
                                      time)

audio_track = AudioFileClip(finished_track)

vid_file = downloadBackgroundVid(test_vid_data["snippet"]["resourceId"]["videoId"], 
                                 audio_track.duration, 
                                 output_folder, 
                                 time)

output_folder_completed_vid = "Input\\Test Input\\Videos\\"

mergeVidAndTrack(vid_file, finished_track, output_folder_completed_vid, time)