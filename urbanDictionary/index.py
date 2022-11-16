from api import getData
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, ImageClip, AudioFileClip, CompositeAudioClip
import os
import random
import requests
import json
import base64
import asyncio


word = getData()['list'][0]['word']
definition = getData()['list'][0]['definition']
# turn word to text to speech using tiktok api

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# post to https://tiktok-tts.weilnet.workers.dev/api/generation width payload word as text and voice as en_uk_001 and get the mp3 file


async def textToSpeech(word, type):
    r = requests.post("https://tiktok-tts.weilnet.workers.dev/api/generation",
                      json={'text': word, 'voice': 'en_uk_001'})
    r = r.json()
    with open(f"{dir_path}/urbanDictionary/audio/{type}.mp3", "wb") as f:
        f.write(base64.b64decode(r['data']))


# function that creates a vide width word as text for 5 seconds and saves it as video.mp4 in the same directory
def createVideo():
    # create video width a image and the word as text that fades in after 1 second and fades out after 4 seconds and then the definition as text that fades in after 1 second and fades out after 4 seconds
    clip = (ImageClip(f"{dir_path}/urbanDictionary/videos/bg.jpg")
            .set_duration(12)
            .set_position('center')
            .crossfadein(1)
            .set_start(1))
    wordd = (TextClip(word, fontsize=100, color='white', font='Arial-Bold')
             .set_duration(5)
             .set_position('center')
             .crossfadein(1)
             .set_start(1))
    definitionn = (TextClip(definition, fontsize=50, color='white', font='Arial-Bold')
                   .set_duration(5)
                   .set_position('center')
                   .crossfadein(1)
                   .set_start(7))
    wordAudio = AudioFileClip(
        f"{dir_path}/urbanDictionary/audio/word.mp3").set_start(1)
    definitionAudio = AudioFileClip(
        f"{dir_path}/urbanDictionary/audio/definition.mp3").set_start(7)

    # add text to the video
    clip = CompositeVideoClip([clip, wordd, definitionn])
    # add audio to the video
    clip = clip.set_audio(CompositeAudioClip([wordAudio, definitionAudio]))

    clip.write_videofile(f"{dir_path}/urbanDictionary/video.mp4",
                         fps=24, codec='libx264', audio_codec='aac')


# specify the path to imageMAgick in your computer


def main():
    asyncio.run(textToSpeech(word, 'word'))
    asyncio.run(textToSpeech(definition, 'definition'))
    createVideo()


if __name__ == '__main__':
    main()
