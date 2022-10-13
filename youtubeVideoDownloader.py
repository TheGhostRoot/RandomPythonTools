import os
import time

try:
    from pytube import YouTube
except ImportError:
    if os.name.startswith("win"):
        os.system("python -m pip install pytube")
    else:
        os.system("python3 -m pip install pytube")

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    if os.name.startswith("win"):
        os.system("python -m pip install tkinter")
    else:
        os.system("python3 -m pip install tkinter")

p = ""
if not os.path.exists(os.getcwd()+"\youtubeconf.txt"):
    file = open("youtubeconf.txt", "a")
    file.write("youtubeDownloads/")
    file.close()
    p = "youtubeDownloads/"
else:
    file = open("youtubeconf.txt", "rt")
    for line in file:
        p = line
    file.close()

if p == "":
    p = "youtubeDownloads/"

if not os.path.exists(os.getcwd() + "\youtubeDownloads") and p == "youtubeDownloads/":
    os.mkdir("youtubeDownloads")

G = False
while True:
    try:
        gui = input("GUI Y/N: ")
        if gui != "":
            gui = gui.lower()
            if gui == "y" or gui == "yes":
                G = True
                break
            else:
                break
    except ImportError:
        print("Exiting..")
        exit()


def entry_fields():
    start_time = time.time()
    YouTube(e1.get()).streams.get_highest_resolution().download(output_path=p)
    end_time = time.time()
    popup = tk.Tk()
    popup.wm_title("Download Status")
    str1 = "download successful !\n"
    str2 = "Total time taken: {} seconds".format(round(end_time - start_time, 3))
    msg = str1 + str2
    label = ttk.Label(popup, text=msg, font=("Verdana", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Ok", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def entry_fields_a():
    vTitle = YouTube(e1.get()).streams.get_audio_only().title
    start_time = time.time()
    YouTube(e1.get()).streams.get_audio_only().download(output_path=p, filename=vTitle + ".mp3")
    end_time = time.time()
    popup = tk.Tk()
    popup.wm_title("Download Status")
    str1 = "download successful !\n"
    str2 = "Total time taken: {} seconds".format(round(end_time - start_time, 3))
    msg = str1 + str2
    label = ttk.Label(popup, text=msg, font=("Verdana", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Ok", command=popup.destroy)
    B1.pack()
    popup.mainloop()


if G:
    master = tk.Tk()
    master.geometry("345x100")
    master.wm_title("Youtube Downloader")
    tk.Label(master, text="Youtube Video URL: ").grid(row=0)
    e1 = tk.Entry(master)
    e1.grid(row=0, column=1)

    tk.Button(master,
              text='Download Video', command=entry_fields, anchor=tk.CENTER).grid(row=1,
                                                                                  sticky=tk.W,
                                                                                  pady=4)

    tk.Button(master,
              text='Download Audio', command=entry_fields_a, anchor=tk.CENTER).grid(row=2,
                                                                                    sticky=tk.W,
                                                                                    pady=4)

    tk.mainloop()
else:
    while True:
        try:
            url = input("YouTube Video Link: ")
            if url != "":
                video = input("(A)udio / (V)deo: ")
                if video != "":
                    video = video.lower()
                    if video == "v" or video == "video":
                        start_time = time.time()
                        YouTube(url).streams.get_highest_resolution().download(output_path=p)
                        end_time = time.time()
                    else:
                        vTitle = YouTube(url).streams.get_audio_only().title
                        start_time = time.time()
                        YouTube(url).streams.get_audio_only().download(output_path=p, filename=vTitle + ".mp3")
                        end_time = time.time()
                    print("Downloaded!")
                    print("Total time taken: {} seconds".format(round(end_time - start_time, 3)))
        except KeyboardInterrupt:
            print("Exiting...")
            exit()

