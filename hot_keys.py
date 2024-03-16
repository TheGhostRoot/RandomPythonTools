"""
from pynput.keyboard import Listener, Key, Controller
#"l": [dd]
isPrint = True
hot_keys = {
Key.
Key.page_up: [Key.up, Key.down, Key.right, Key.left, Key.up]

}




keyboard = Controller()

def press_key(key):
  for i in hot_keys[key]:
    keyboard.press(i)

def on_press(key):
    if isPrint:
      print(key)

    #if k == "\x03":
    #  exit()

    if key in hot_keys.keys():
      press_key(key)
    
    try:
      if key.char in hot_keys.keys():
        press_key(key.char)
    except Exception:
      pass


with Listener(on_press=on_press) as listener:
    listener.join()
"""



import tkinter as tk
from pynput.keyboard import Listener, Key, Controller

isPrint = True
running = False
hot_keys = {
    "l": ["o"],
    Key.page_up: [Key.up, Key.down, Key.right, Key.left, Key.up]
}

keyboard = Controller()

def press_key(key):
    for i in hot_keys[key]:
        keyboard.press(i)

def on_press(key):
    global running
    if running:
        if isPrint:
            key_label.config(text=str(key))
        if key in hot_keys.keys():
            press_key(key)
        try:
            if key.char in hot_keys.keys():
                press_key(key.char)
        except AttributeError:
            pass

def start_listener():
    global running
    if not running:
        listener = Listener(on_press=on_press)
        listener.start()
        running = True
        status_label.config(text="Running")

def stop_listener():
    global running
    if running:
        running = False
        status_label.config(text="Stopped")

# GUI setup
root = tk.Tk()
root.title("Keyboard Listener")
root.geometry("300x150")

start_button = tk.Button(root, text="Start", command=start_listener)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_listener)
stop_button.pack(pady=5)

status_label = tk.Label(root, text="Stopped")
status_label.pack(pady=5)

key_label = tk.Label(root, text="")
key_label.pack(pady=5)

root.mainloop()

