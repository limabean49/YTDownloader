from gui import GUI
import importer

class App:
    def __init__(self):
        self.gui = GUI(callback=self.onSubmit)

    def onSubmit(self: GUI, input: str):
        video = importer.requestVideo(input)
        self.gui.updateSelectedVideo(title=video["title"],
                                      thumbnail=video["thumbnail"],
                                      views=video["views"],
                                      length=video["length"],
                                      uploadDate=video["uploadDate"])

    def run(self):
        self.gui.run()

if __name__ == "__main__":
    app = App()
    app.run()