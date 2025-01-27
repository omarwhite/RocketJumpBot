from Generation.audiogen import *
from dbtests import *
from Reddit.getcomments import *
from datetime import datetime

testPost = grabTestPost()
comments = getTop10Comments(testPost["url"])
output_folder_voiceover = "Input\\Test Input\\Voiceovers\\"
output_folder_track = "Input\\Test Input\\Completed Tracks\\"
time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
test_music_file = "Input\\Music\\touch_and_go.mp3"
test_voiceover_file = f"{output_folder_voiceover}voiceover_{time}.mp3"

genVoiceover(testPost, comments, output_folder_voiceover, time)
combineVoiceAndMusic(test_voiceover_file, test_music_file, output_folder_track, time)