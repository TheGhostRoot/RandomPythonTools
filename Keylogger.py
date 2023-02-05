import os

try:
    from pynput.keyboard import Listener, Key
except ImportError:
    os.system('python -m pip install pynput')
    os.system('python3 -m pip install pynput')
    try:
        from pynput.keyboard import Listener, Key
    except ImportError:
        print("You need pythom and pynput")
        exit()

keys = []

def on_press(key):
    keys.append(key)
    print(str(key))

with Listener(on_press=on_press) as listener:
    listener.join()
