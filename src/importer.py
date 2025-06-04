from pytubefix import YouTube
import gui

def requestVideo(input):
    input = input.strip().split('&')[0]
    try:
        yt = YouTube(input)
    except Exception as e:
        return "Error: " + e
    else:
        print(yt.streams.all())
        return {
            "title": yt.title + " - " + yt.author,
            "thumbnail": yt.thumbnail_url
        }
        
