from youtube_dl import YoutubeDL
import vlc

# Create an instance of the VLC media player and a media player object for the audio URL
vlc_instance = vlc.Instance()
media_player = vlc_instance.media_player_new()

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
g = input('YouTube URL: ')
with YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(g, download=False)
#URL = info['url']

audio_url = info['url']

# Load the audio from the URL and start playing it
media = vlc_instance.media_new(audio_url)
media_player.set_media(media)
media_player.play()

# Continuously check for user input and control the playback accordingly
while True:
    command = input("Enter a command (play, pause, stop): ")
    if command == "play":
        media_player.play()
    elif command == "pause":
        media_player.pause()
    elif command == "stop":
        media_player.stop()
        break

