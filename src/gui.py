from customtkinter import *
import requests
from PIL import ImageTk, Image
from io import BytesIO

class GUI:
    def __init__(self, callback):
        self.callback = callback

        self.main = CTk()
        self.main.geometry('1280x720')
        self.main.title("YT Downloader")
        self.video = ""
        set_appearance_mode("dark")

        self.main.bind("<Configure>", self.onResize)

        self.inputPage()

    def inputPage(self):
        for i in self.main.winfo_children():
            i.destroy()

        # Top: entry frame
        self.entryFrame = CTkFrame(self.main, corner_radius=32)
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
        self.contentFrame = CTkFrame(self.main,corner_radius=32)
        self.contentFrame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        # Left: image frame
        self.imageFrame = CTkFrame(self.contentFrame, corner_radius=32)
        self.imageFrame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.imageLabel = CTkLabel(self.imageFrame, text="Thumbnail will appear here")
        self.imageLabel.pack(expand=True)

        # Right: text frame
        self.labelFrame = CTkFrame(self.contentFrame, corner_radius=32)
        self.labelFrame.pack(side="left", fill="both", expand=True)

        self.label = CTkLabel(self.labelFrame, text=" ", font=("Helvetica", 20), wraplength=400, corner_radius=32)
        self.label.pack(fill="both", expand=True)

        self.download = CTkButton(self.main, text="Next", font=("Helvetica", 20), corner_radius=32, hover_color="#3b63f1", command=self.downloadPage)

    def downloadPage(self):
        for i in self.main.winfo_children():
            i.destroy()
        
        self.back = CTkButton(self.main, text="Back", font=("Helvetica", 20), corner_radius=32, hover_color="#3b63f1", command=self.inputPage)
        self.back.place(relx=0.15, rely=0.9, anchor=CENTER)
        
        self.text = CTkLabel(self.main, text="Choose settings for download:", font=("Helvetica", 20))
        self.text.pack(pady=10)

    def buttonClicked(self):
        input = self.entry.get()
        self.video = self.entry.get().split("&")[0]
        self.callback(input)

    def updateSelectedVideo(self, title, thumbnail):
        self.label.configure(text=title)

        ctkimage = Image.open(BytesIO(requests.get(url=thumbnail).content))
        ctkimage = CTkImage(ctkimage.crop((0, 60, 640, 420)), size=(640, 360))

        self.imageLabel.configure(image=ctkimage, text="")
        self.download.place(relx=0.9, rely=0.9, anchor=CENTER)

        print(self.video)

    def onResize(self, event):
        width = self.label.winfo_width()
        self.label.configure(wraplength=(width - 20))

    def run(self):
        self.main.mainloop()