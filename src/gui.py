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
        self.set_appearance_mode("dark")
        self.inputPage()

    def inputPage(self):
        for i in self.main.winfo_children():
            i.destroy()

        self.text = CTkLabel(self.main, text="Enter a YouTube video link to download:", font=("Helvetica", 20))
        self.text.pack()

        self.entry = CTkEntry(self.main, width=40, font=("Arial", 14))
        self.entry.pack(pady=20)

        self.submitButton = CTkButton(self.main, text="Submit", font=("Helvetica", 20), corner_radius=20, command=self.buttonClicked)
        self.submitButton.pack(pady=20)

        self.label = CTkLabel(self.main, text="", font=("Helvetica", 20))
        self.label.pack()

        self.image = CTkLabel(self.main)
        self.image.pack()

        self.download = CTkButton(self.main, text="Next", font=("Helvetica", 20),  command=self.downloadPage)

    def downloadPage(self):
        for i in self.main.winfo_children():
            i.destroy()
        
        self.back = CTkButton(self.main, text="Back", font=("Helvetica", 20),  command=self.inputPage)
        self.back.place(relx=0.1, rely=0.9, anchor=CENTER)
        
        self.text = CTkLabel(self.main, text="Choose settings for download:", font=("Helvetica", 20))
        self.text.pack()

    def buttonClicked(self):
        input = self.entry.get()
        self.callback(input)

    def updateSelectedVideo(self, title, thumbnail):
        self.label.config(text=title)
        image = Image.open(BytesIO(requests.get(url=thumbnail).content))
        image = image.crop((0, 60, 640, 420))
        self.photo = ImageTk.PhotoImage(image)

        self.image.config(image=self.photo)

        self.download.place(relx=0.9, rely=0.9, anchor=CENTER)

    def run(self):
        self.main.mainloop()
