from customtkinter import *
import requests
from PIL import ImageTk, Image
from io import BytesIO

class GUI:
    def __init__(self, callback, downloadCallback) -> None:
        self.callback = callback
        self.downloadCallback = downloadCallback

        self.main = CTk()
        self.main.geometry('1280x720')
        self.main.title("YT Downloader")
        self.video: str = ""
        self.cancelRequested: bool = False
        set_appearance_mode("dark")

        self.ctkimage = None
        self.info = None

        self.inputPage()

    def inputPage(self) -> None:
        for i in self.main.winfo_children():
            i.destroy()

        # Frame for input page
        self.inputPageFrame = CTkFrame(self.main)
        self.inputPageFrame.pack(side="top", fill="both", expand=True)
        self.inputPageFrame.bind("<Configure>", self.onResize)

        # Top: entry frame
        self.entryFrame = CTkFrame(self.inputPageFrame, corner_radius=32)
        self.entryFrame.pack(side="top", fill="x", expand=False, padx=20, pady=10)

        self.text = CTkLabel(self.entryFrame, text="Enter a YouTube video link to download:", font=("Helvetica", 20))
        self.text.pack(pady=10)

        self.entry = CTkEntry(self.entryFrame, width=500, font=("Helvetica", 16))
        if self.video:
            self.entry.insert(0, self.video)
        self.entry.pack(pady=20)

        self.submitButton = CTkButton(self.entryFrame, text="Submit", font=("Helvetica", 20), corner_radius=32, hover_color="#3b63f1", command=self.submitClicked)
        self.submitButton.pack(pady=20)

        # Middle content frame
        self.contentFrame = CTkFrame(self.inputPageFrame,corner_radius=32)
        self.contentFrame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        # Left: image frame
        self.imageFrame = CTkFrame(self.contentFrame, corner_radius=32)
        self.imageFrame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        if self.ctkimage:
            self.imageLabel = CTkLabel(self.imageFrame, image=self.ctkimage, text="")
        else:
            self.imageLabel = CTkLabel(self.imageFrame, text="Thumbnail will appear here")
        self.imageLabel.pack(expand=True)

        # Right: text frame
        self.labelFrame = CTkFrame(self.contentFrame, corner_radius=32)
        self.labelFrame.pack(side="left", fill="both", expand=True)

        if self.info:
            self.label = CTkLabel(self.labelFrame, text=self.info, font=("Helvetica", 20), wraplength=400, corner_radius=32)
            self.label.pack(fill="both", expand=True)
            self.label.bind("<Configure>", self.onResize)
            self.onResize(None) # Adjust label size immediately
        else:
            self.label = CTkLabel(self.labelFrame, text=" ", font=("Helvetica", 20), wraplength=400, corner_radius=32)
            self.label.bind("<Configure>", self.onResize)
            self.label.pack(fill="both", expand=True)

        self.download = CTkButton(self.inputPageFrame, text="Next", font=("Helvetica", 20), corner_radius=32, hover_color="#3b63f1", command=self.downloadPage)
        if self.info:
            self.download.place(relx=0.9, rely=0.9, anchor=CENTER)

    def downloadPage(self) -> None:
        for i in self.main.winfo_children():
            i.destroy()
        
        # Frame for download options
        self.downloadFrame = CTkFrame(self.main, corner_radius=32)
        self.downloadFrame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        self.back = CTkButton(self.downloadFrame, text="Back", font=("Helvetica", 20), corner_radius=32, hover_color="#3b63f1", command=self.inputPage)
        self.back.place(relx=0.1, rely=0.9, anchor=CENTER)

        self.text = CTkLabel(self.downloadFrame, text="Choose settings for download:", font=("Helvetica", 20))
        self.text.pack(pady=10)

        self.videoDropdown = CTkComboBox(self.downloadFrame, width=350, corner_radius=10, values=[label for label, string in self.videoOptions])
        self.videoDropdown.place(relx=0.3, rely=0.15, anchor=CENTER)

        self.audioDropdown = CTkComboBox(self.downloadFrame, width=350, corner_radius=10, values=[label for label, string in self.audioOptions])
        self.audioDropdown.place(relx=0.7, rely=0.15, anchor=CENTER)

        self.downloadButton = CTkButton(self.downloadFrame, text="Download!", width=150, corner_radius=32, command=self.downloadClicked)
        self.downloadButton.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.progressBar = CTkProgressBar(self.downloadFrame, corner_radius=32, width=500, mode="determinate")
        self.progressBar.set(0)
        self.progressBar.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.progressText = CTkLabel(self.downloadFrame, text="Progress: 0% - 0 MB of - MB", font=("Helvetica", 20))
        self.progressText.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.cancelButton = CTkButton(self.downloadFrame, text="Cancel", font=("Helvetica", 20), corner_radius=32, hover_color="#f83535", command=self.cancelDownload)
        self.cancelButton.place(relx=0.5, rely=0.7, anchor=CENTER)

    def submitClicked(self) -> None:
        input = self.entry.get()
        self.video = self.entry.get().split("&")[0]
        self.callback(input)

    def downloadClicked(self) -> None:
        selectedVLabel = self.videoDropdown.get()
        videoStream = next(stream for label, stream in self.videoOptions if label == selectedVLabel)

        selectedALabel = self.audioDropdown.get()
        audioStream = next(stream for label, stream in self.audioOptions if label == selectedALabel)

        self.downloadCallback(videoInput=videoStream.itag, audioInput=audioStream.itag)

    def updateSelectedVideo(self, title: str, thumbnail: str, views: str, length: str, uploadDate: str) -> None:
        self.info = f"{title} \n\n{views} views - {length} - Upload Date: {uploadDate}"
        self.label.configure(text=self.info)

        self.ctkimage = Image.open(BytesIO(requests.get(url=thumbnail).content))
        self.ctkimage = CTkImage(self.ctkimage.crop((0, 60, 640, 420)), size=(640, 360))

        self.imageLabel.configure(image=self.ctkimage, text="")
        self.download.place(relx=0.9, rely=0.9, anchor=CENTER)
        self.onResize(None)  # Adjust label size immediately

    def configureStreams(self, streams) -> None:
        self.videoOptions = []
        self.audioOptions = []

        for stream in streams:
            if not stream.is_progressive:
                if stream.resolution:
                    label = f"Video: {stream.resolution} - {stream.fps}fps - Codec: {stream.codecs[0]} ({stream.mime_type[6:]})"
                    self.videoOptions.append((label, stream))
                else:
                    label = f"Audio: {stream.abr} - Codec: {stream.codecs[0]}"
                    self.audioOptions.append((label, stream))
    
    def onResize(self, event) -> None:
        width = self.label.winfo_width()
        self.label.configure(wraplength=(width - 20))

    def progressCallback(self, stream, chunk, bytes_remaining):
        if self.cancelRequested:
            raise Exception("Download cancelled by user")
        downloadedMB = (stream.filesize - bytes_remaining) / 1024 / 1024
        totalMB = stream.filesize / 1024 / 1024
        percent = downloadedMB / totalMB

        self.progressBar.after(0, lambda: self.progressBar.set(percent))
        self.progressText.after(0, lambda: self.progressText.configure(text=f"Progress: {downloadedMB / totalMB * 100:.2f}% - {downloadedMB:.2f} MB of {totalMB:.2f} MB"))

    def completeCallback(self, stream, file_path):
        if self.cancelRequested:
            self.cancelRequested = False
            self.completeText = CTkLabel(self.downloadFrame, text=f"Download cancelled by user", font=("Helvetica", 14))
        else:
            self.progressBar.set(1.0)
            self.completeText = CTkLabel(self.downloadFrame, text=f"Download complete at {file_path} ! :)", font=("Helvetica", 16))
            self.statusLabel = CTkLabel(self.downloadFrame, text=f"Combining video and audio...", font=("Helvetica", 16))
            self.statusLabel.place(relx=0.5, rely=0.85, anchor=CENTER)
        self.completeText.place(relx=0.5, rely=0.8, anchor=CENTER)
    
    def combineText(self, text):
        self.statusLabel.configure(text=text)

    def cancelDownload(self):
        self.cancelRequested = True

    def run(self) -> None:
        self.main.mainloop()