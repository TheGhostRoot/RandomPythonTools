from moviepy.editor import VideoFileClip

while True:
	name = input("Enter the name of the video >> ")
	GIFname = input(" Enter the name of the gif >> ")
	FPSS = int(input("  Enter the fps you want the gif to be >> "))
	if name != "" or name != " ":
		clip = VideoFileClip(name)
		clip.write_gif(GIFname, fps=FPSS)