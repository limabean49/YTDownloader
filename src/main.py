from gui import GUI
from importer import YouTubeVideo

class App:
    def __init__(self) -> None:
        self.gui = GUI(callback=self.onSubmit)

    def onSubmit(self: GUI, input: str) -> None:
        yt = YouTubeVideo(url=input)
        video = yt.getValues()
        self.gui.updateSelectedVideo(title=video["title"],
            thumbnail=video["thumbnail"],
            views=video["views"],
            length=video["length"],
            uploadDate=video["uploadDate"])
        
        self.gui.configureStreams(streams=yt.getStreams())

    def downloadVideo(self):
        pass

    def run(self) -> None:
        self.gui.run()

if __name__ == "__main__":
    app = App()
    app.run()