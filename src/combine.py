import ffmpeg
import os
import threading
from gui import GUI

def combineFiles(videoPath: str, audioPath: str, outputPath: str, gui: GUI) -> None:
    def task():
        try:
            audio_ext = os.path.splitext(audioPath)[1].lower()
            if audio_ext == ".opus":
                acodec = "copy"
            else:
                acodec = "aac"

            ffmpeg.output(
                ffmpeg.input(videoPath),
                ffmpeg.input(audioPath),
                outputPath,
                vcodec="copy",
                acodec=acodec,
                strict="experimental"
            ).run(overwrite_output=True)
        except Exception as e:
            gui.combineText(text="Error during combine")
            print("Error: " + str(e))
        else:
            gui.combineText(text="Combined video and audio!")

    threading.Thread(target=task).start()
