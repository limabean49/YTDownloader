from pytubefix import YouTube
import gui

def requestVideo(input):
    try:
        yt = YouTube(input)
    except:
        return {
            "title": "Error: Invalid URL (likely) or YouTube's servers are not working",
            "thumbnail": None,
            "views": None,
            "length": None,
            "uploadDate": None
        }
    else:
        print(yt.streams.all())
        return {
            "title": yt.title + " - " + yt.author,
            "thumbnail": yt.thumbnail_url,
            "views": yt.views,
            "length": yt.length,
            "uploadDate": yt.publish_date
        }