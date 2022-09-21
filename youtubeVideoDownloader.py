from pytube import YouTube
import time
import tkinter as tk
from tkinter import ttk

NORM_FONT = ("Verdana", 10)
#video_url = input("Please enter the Youtube video link/URL: ")


def entry_fields():
    start_time = time.time()
    download_location = "youtubeDownloads/"
    YouTube(e1.get()).streams.get_highest_resolution().download(download_location)
    end_time = time.time()
    popup = tk.Tk()
    popup.wm_title("Download Status")
    str1 = "download successful !!\n"
    str2 = "Total time taken: {} seconds".format(round(end_time - start_time, 3))
    msg = str1 + str2
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Ok", command=popup.destroy)
    B1.pack()
    popup.mainloop()


master = tk.Tk()
master.geometry("345x60")
master.wm_title("Youtube Downloader")
tk.Label(master, text="Enter Youtube Video URL: ").grid(row=0)
e1 = tk.Entry(master)
e1.grid(row=0, column=1)

tk.Button(master,
          text='Download', command=entry_fields, anchor=tk.CENTER).grid(row=1,
                                                                        sticky=tk.W,
                                                                        pady=4)
tk.mainloop()
