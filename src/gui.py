from customtkinter import *
import requests
from PIL import ImageTk, Image
from io import BytesIO

class GUI:
    def __init__(self, callback) -> None:
        self.callback = callback

        self.main = CTk()
        self.main.geometry('1280x720')
        self.main.title("YT Downloader")
        self.video = ""
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

        self.submitButton = CTkButton(self.entryFrame, text="Submit", font=("Helvetica", 20), corner_radius=32, hover_color="#3b63f1", command=self.buttonClicked)
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

    def buttonClicked(self) -> None:
        input = self.entry.get()
        self.video = self.entry.get().split("&")[0]
        self.callback(input)

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

    def run(self) -> None:
        self.main.mainloop()