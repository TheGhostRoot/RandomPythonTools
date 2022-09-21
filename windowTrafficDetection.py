import os
os.system("pip install win10toast")
os.system("pip install psutil")
os.system("pip install tkinter-page")

try:
	import tkinter as tk
	from psutil import net_io_counters
	from win10toast import ToastNotifier
except Exception:
	print("Python3.7.9 is required!")

# Variables for use in the size() function.
KB = float(1024)
MB = float(KB ** 2)  # 1,048,576
GB = float(KB ** 3)  # 1,073,741,824
TB = float(KB ** 4)  # 1,099,511,627,776

def size(B):

	B = float(B)
	if B < KB:
		return f"{B} Bytes"
	elif KB <= B < MB:
		return f"{B/KB:.2f} KB"
	elif MB <= B < GB:
		return f"{B/MB:.2f} MB"
	elif GB <= B < TB:
		return f"{B/GB:.2f} GB"
	elif TB <= B:
		return f"{B/TB:.2f} TB"

## Constants
WINDOW_SIZE = (400, 400)  # Width x Height
WINDOW_RESIZEABLE = False  # If the window is resizeable or not.
REFRESH_DELAY = 150  # Window update delay in ms.

## Variables
last_send, last_recive, send_speed, down_speed = 0, 0, 0, 0

## Initializing
window = tk.Tk()

window.title("Network Bandwidth Monitor")  # Setting the window title.
# Setting the window size.
window.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
# We now lock the window.
window.resizable(width=WINDOW_RESIZEABLE, height=WINDOW_RESIZEABLE)

label_total_send_header = tk.Label(
	text="Total send:", font="Quicksand 12 bold")
label_total_send_header.pack()
label_total_send = tk.Label(text="Calculating...", font="Quicksand 12")
label_total_send.pack()

label_total_recive_header = tk.Label(
	text="Total recive:", font="Quicksand 12 bold")
label_total_recive_header.pack()
label_total_recive = tk.Label(text="Calculating...", font="Quicksand 12")
label_total_recive.pack()

label_total_usage_header = tk.Label(
	text="Total Usage:", font="Quicksand 12 bold")
label_total_usage_header.pack()
label_total_usage = tk.Label(text="Calculating...\n", font="Quicksand 12")
label_total_usage.pack()

label_send_header = tk.Label(text="send:", font="Quicksand 12 bold")
label_send_header.pack()
label_send = tk.Label(text="Calculating...", font="Quicksand 12")
label_send.pack()

label_recive_header = tk.Label(text="recive:", font="Quicksand 12 bold")
label_recive_header.pack()
label_recive = tk.Label(text="Calculating...", font="Quicksand 12")
label_recive.pack()

attribution = tk.Label(text="\n~ Bandwidth traffic ~", font="Quicksand 11 italic")
attribution.pack()

# Updating Labels

def update():
	global last_send, last_recive, send_speed, down_speed
	counter = net_io_counters()

	send = counter.bytes_sent
	recive = counter.bytes_recv
	total = send + recive

	if last_send > 0:
		if send < last_send:
			send_speed = 0
		else:
			send_speed = send - last_send

	if last_recive > 0:
		if recive < last_recive:
			down_speed = 0
		else:
			down_speed = recive - last_recive
			
	last_send = send
	last_recive = recive

	label_total_send["text"] = f"{size(send)} ({send} Bytes)"
	label_total_recive["text"] = f"{size(recive)} ({recive} Bytes)"
	label_total_usage["text"] = f"{size(total)}\n"

	label_send["text"] = size(send_speed)
	label_recive["text"] = size(down_speed)

	label_total_send.pack()
	label_total_recive.pack()
	label_total_usage.pack()
	label_send.pack()
	label_recive.pack()
	
	window.after(REFRESH_DELAY, update)  # reschedule event in refresh delay.

counter = net_io_counters()
send = counter.bytes_sent
recive = counter.bytes_recv
total = send + recive
toaster = ToastNotifier()

def windowUp():
	window.after(REFRESH_DELAY, update)
	window.mainloop()

windowUp()
