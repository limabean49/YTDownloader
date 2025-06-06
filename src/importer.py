from pytubefix import YouTube

class YouTubeVideo:
    def __init__(self, url) -> None:
        try:
            self.yt = YouTube(url)
        except:
            self.yt = None

    def getValues(self) -> dict:
        if not self.yt:
            return {
                "title": "Error: Invalid URL (likely) or YouTube's servers are not working",
                "thumbnail": None,
                "views": None,
                "length": None,
                "uploadDate": None
            }
        return {
            "title": f"{self.yt.title} - {self.yt.author}",
            "thumbnail": self.yt.thumbnail_url,
            "views": f"{self.yt.views:,}",
            "length": f"{self.yt.length // 3600:02}:{(self.yt.length % 3600) // 60:02}:{self.yt.length % 60:02}",
            "uploadDate": self.yt.publish_date
        }
    
    def getStreams(self) -> list:
        return self.yt.streams