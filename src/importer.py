from pytubefix import YouTube
import threading
import re

class YouTubeVideo:
    def __init__(self, url: str, onProgress = None, onComplete = None, failCallback = None, finishCallback = None) -> None:
        try:
            self.yt = YouTube(url)
            if onProgress:
                self.yt.register_on_progress_callback(onProgress)
            if onComplete:
                self.yt.register_on_complete_callback(onComplete)
            self.failCallback = failCallback
            self.finishCallback = finishCallback
        except Exception as e:
            print(f"Error initializing YouTube object: {e}")
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
    
    def downloadVideo(self, videoInput: int, audioInput: int) -> None:
        thread = threading.Thread(target=self.startDownload, args=(videoInput, audioInput), daemon=True)
        thread.start()

    def startDownload(self, videoitag: int, audioitag: int) -> None:
        try:
            self.yt.streams.get_by_itag(videoitag).download(filename=(re.sub(r'[\\/*?:"<>|]', "", self.yt.title + " - " + self.yt.author) + "video.mp4"))
            self.yt.streams.get_by_itag(audioitag).download(filename=(re.sub(r'[\\/*?:"<>|]', "", self.yt.title + " - " + self.yt.author) + "audio.mp4"))
            if self.finishCallback:
                self.finishCallback()
        except Exception as e:
            print(f"Download failed: {e}")
            if self.failCallback:
                self.failCallback()