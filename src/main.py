from gui import GUI
from importer import YouTubeVideo

class App:
    def __init__(self) -> None:
        self.gui = GUI(callback=self.onSubmit, downloadCallback=self.downloadVideo)

    def onSubmit(self: GUI, input: str) -> None:
        self.yt = YouTubeVideo(url=input, onProgress=self.gui.progressCallback, onComplete=self.gui.completeCallback, failCallback=self.failMessage)
        video = self.yt.getValues()
        self.gui.updateSelectedVideo(title=video["title"],
            thumbnail=video["thumbnail"],
            views=video["views"],
            length=video["length"],
            uploadDate=video["uploadDate"])
        
        self.gui.configureStreams(streams=self.yt.getStreams())

    def downloadVideo(self, videoInput, audioInput):
        self.yt.downloadVideo(videoInput=videoInput, audioInput=audioInput)

    def run(self) -> None:
        self.gui.run()
    
    def failMessage(self) -> None:
        self.gui.completeCallback(None, None)

if __name__ == "__main__":
    app = App()
    app.run()