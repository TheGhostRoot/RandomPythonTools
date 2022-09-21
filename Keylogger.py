from pynput.keyboard import Listener, Key

keys = []

def on_press(key):
    keys.append(key)
    print(str(key))

with Listener(on_press=on_press) as listener:
    listener.join()
