import boto3
from botocore.exceptions import BotoCoreError, ClientError
from pydub import *
from Reddit.getcomments import *

def genVoiceover(redditPost, comments, location, timestamp):
    filename = f"{location}voiceover_{timestamp}.mp3"
    
    # Initialize Polly client
    polly_client = boto3.client('polly', region_name='us-west-2')  # Replace with your desired AWS region

    # Create a list to store the combined audio streams
    audio_streams = []

    try:
        # Convert the Reddit post title to speech
        response = polly_client.synthesize_speech(
            Text=redditPost["title"],
            OutputFormat='mp3',
            VoiceId='Joanna'  # You can change the voice ID here
        )
        audio_streams.append(response['AudioStream'].read())

        # Convert each comment to speech
        for i, comment in enumerate(comments, start=1):
            comment_text = f"{i} {comment.body}"  # Assuming comments are objects with a body attribute
            response = polly_client.synthesize_speech(
                Text=comment_text,
                OutputFormat='mp3',
                VoiceId='Joanna'  # You can change the voice ID here
            )
            audio_streams.append(response['AudioStream'].read())

    except (BotoCoreError, ClientError) as error:
        print(f"An error occurred: {error}")
        return

    # Write the combined audio streams to a single file
    with open(filename, 'wb') as f:
        for stream in audio_streams:
            f.write(stream)

def combineVoiceAndMusic(voiceover, music, dest, timestamp):
    filename = f"{dest}track_{timestamp}.mp3"

    voiceoverTrack = AudioSegment.from_file(voiceover)
    musicTrack = AudioSegment.from_file(music)

    musicTrack -= 15

    if (len(voiceoverTrack) > len(musicTrack)):
        musicTrack = musicTrack * (len(voiceoverTrack) // len(musicTrack) + 1)  # Loop background to match the length of voiceover
        musicTrack = musicTrack[:len(voiceoverTrack)]  # Trim the background to the exact length of the voiceover
    else:
        musicTrack = musicTrack[:len(voiceoverTrack)]  # Truncate the background to the length of the voiceover
    
    combinedTrack = musicTrack.overlay(voiceoverTrack)

    combinedTrack.export(filename, format="mp3")
    return filename