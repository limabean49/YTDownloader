from gui import GUI
import importer

class App:
    def __init__(self):
        self.gui = GUI(callback=self.onSubmit)

    def onSubmit(self, input):
        video = importer.requestVideo(input)
        self.gui.updateSelectedVideo(title=video["title"], thumbnail=video["thumbnail"])

    def run(self):
        self.gui.run()

if __name__ == "__main__":
    app = App()
    app.run()
