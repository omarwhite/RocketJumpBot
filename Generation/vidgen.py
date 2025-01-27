from moviepy.editor import VideoFileClip, AudioFileClip
import yt_dlp
from datetime import datetime
import os
import subprocess
from Database.mongodbconn import getRandomVid

def downloadBackgroundVid(videoId, length, output_folder, timestamp):
    filename = f"video_{timestamp}"
    temp_files = []

    os.makedirs(output_folder, exist_ok=True)

    total_downloaded_time = 0
    remaining_length = length

    while remaining_length > 0:
        part_filename = os.path.join(output_folder, f'{filename}_part{len(temp_files)}.mp4')
        temp_files.append(part_filename)

        ydl_opts = {
            'format': 'bestvideo',
            'outtmpl': part_filename,
            'quiet': True
        }

        url = f"https://www.youtube.com/watch?v={videoId}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_duration = info.get('duration', 0)

            if video_duration >= remaining_length:
                download_section = f"00:00:00-{convert_seconds_to_time(remaining_length)}"
                ydl_opts['download_sections'] = f'*{download_section}'
                remaining_length = 0
            else:
                download_section = f"00:00:00-{convert_seconds_to_time(video_duration)}"
                ydl_opts['download_sections'] = f'*{download_section}'
                remaining_length -= video_duration

            ydl.download([url])
            total_downloaded_time += video_duration

            if remaining_length > 0:
                videoId = getRandomVid()["snippet"]["resourceId"]["videoId"]

    final_filename = os.path.join(output_folder, f'{filename}.mp4')
    combine_videos(temp_files, final_filename)

    # Clean up temporary files
    for temp_file in temp_files:
        os.remove(temp_file)

    # Trim the final video to the exact length
    trim_video(final_filename, length)

    return final_filename

def convert_seconds_to_time(seconds):
    hrs, remainder = divmod(seconds, 3600)
    mins, secs = divmod(remainder, 60)
    return f"{int(hrs):02}:{int(mins):02}:{int(secs):02}"

def combine_videos(input_files, output_file):
    list_file = "file_list.txt"
    with open(list_file, 'w') as f:
        for file in input_files:
            f.write(f"file '{file}'\n")

    command = [
        'ffmpeg', '-f', 'concat', '-safe', '0', '-i', list_file,
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '22',
        '-c:a', 'aac', '-b:a', '192k',
        output_file
    ]
    
    subprocess.run(command, check=True)

    os.remove(list_file)

def trim_video(filename, target_length):
    output_file = filename.replace('.mp4', '_trimmed.mp4')
    start_time = "00:00:00"
    end_time = convert_seconds_to_time(target_length)
    
    command = [
        'ffmpeg', '-i', filename, '-ss', start_time, '-to', end_time,
        '-c', 'copy',  # Copying without re-encoding
        output_file
    ]
    
    subprocess.run(command, check=True)

    # Replace original with trimmed video
    os.replace(output_file, filename)

def mergeVidAndTrack(vid, track, output_folder, timestamp):
    complete_filename = os.path.join(output_folder, f'audiovideo_{timestamp}.mp4')

    vid_file = VideoFileClip(vid)
    audio_file = AudioFileClip(track)

    complete_vid = vid_file.set_audio(audio_file)

    complete_vid.write_videofile(complete_filename, codec="libx264", audio_codec="aac")