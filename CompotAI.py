import os, sys, threading
import time

import numpy as np
#import matplotlib.pyplot as plt
#import pickle

try:
    from pynput.keyboard import Listener
    import torch
    import torch.nn as nn
    import pyautogui
    import cv2
    import torchvision.transforms as transformer
except ImportError:
    if sys.platform.startswith('win'):
        os.system('python -m pip install torch torchvision cv2 pyautogui pynput')
    else:
        os.system('python3 -m pip install torch torchvision cv2 pyautogui pynput')
    try:
        from pynput.keyboard import Listener
        import torch
        import torch.nn as nn
        import pyautogui
        import cv2
        import torchvision.transforms as transformer
    except ImportError:
        print("Couldn't install needed packages: torch torchvision cv2 pyautogui pynput")


class BrawlhallaAI(nn.Module):
    def __init__(self, learning_rate=0.1,
                 selected_hero='thor', save_hero='thor-1', use_eyes1=False):
        super().__init__()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.selected_hero = selected_hero
        self.learning_rate = learning_rate
        self.use_eyes2 = use_eyes1
        self.keys = ["s", "a", "d", "w", "space", "shift", "left-click", "right-click", "h", "down-s", "down-a",
                     "down-d", "down-w", "up-s", "up-a", "up-d", "up-w"]
        self.save_hero = save_hero

        # Define the transforms to be applied to the input image
        self.transform = transformer.Compose([
            transformer.ToPILImage(),
            transformer.Resize((224, 224)),
            transformer.ToTensor(),
            transformer.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])

        # Define the neural network architecture
        self.module = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Flatten(),
            # 32 * 56 * 56
            nn.Linear(100352, 128),
            nn.ReLU(),
            nn.Linear(128, 17)
        ).to(device=self.device)

        # self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.module.parameters(), lr=learning_rate)
        self.reward = 0
        self.screen = None

    def forward(self, x):
        x = self.transform(x)
        x = x.unsqueeze(0)
        x = self.module(x)
        key_probabilities = torch.sigmoid(x[0])
        top_key_indices = torch.multinomial(key_probabilities, 1, replacement=True)
        top_keys = [self.keys[i] for i in top_key_indices]
        return top_keys

    def generate_key_combination(self):
        while True:
            self.screen = np.array(pyautogui.screenshot())
            if self.use_eyes2:
                cv2.imshow("Bot's Eyes", self.screen)
                if cv2.waitKey(1) == ord('q'):
                    pass
            key_probabilities = self.forward(self.screen)
            if len(key_probabilities) > 0:
                print('[*] Predicted Combo', key_probabilities)
                # Press the keys in the combination
                for key in key_probabilities:
                    self.press_key(key)

                # Calculate loss based on reward and punishment
                loss = torch.tensor([self.reward] * len(key_probabilities),
                                    dtype=torch.float32, requires_grad=True)
                self.optimizer.zero_grad()
                loss.mean().backward(retain_graph=True)
                self.optimizer.step()
                #print('[+] Learned')
                self.save()
                self.reward = 0
            else:
                self.reward = -1
                print('[-] No Combo Predicted')

    def press_key(self, key):
        if key == "left-click":
            pyautogui.leftClick()
        elif key == "right-click":
            pyautogui.rightClick()
        elif key == "down-s":
            pyautogui.keyDown("s")
        elif key == "down-a":
            pyautogui.keyDown("a")
        elif key == "down-d":
            pyautogui.keyDown("d")
        elif key == "down-w":
            pyautogui.keyDown("w")
        elif key == "up-w":
            pyautogui.keyUp("w")
        elif key == "up-s":
            pyautogui.keyUp("s")
        elif key == "up-a":
            pyautogui.keyUp("a")
        elif key == "up-d":
            pyautogui.keyUp("d")
        else:
            pyautogui.keyDown(key)
            pyautogui.sleep(0.003)
            pyautogui.keyUp(key)
            #pyautogui.press(key)
        # 0.22
        # 0.02
        #pyautogui.sleep(0.22)

    def give_reward(self):
        self.reward = 1
        print("[+] Given Reward")

    def give_punishment(self):
        self.reward = -1
        print("[-] Given Punishment")

    def save(self):
        torch.save(self.module.state_dict(), self.save_hero)
        print("[+] Saved the model state")

    def load(self):
        if os.path.exists(self.selected_hero):
            # , map_location=self.device, pickle_module=pickle
            try:
                self.module.load_state_dict(torch.load(self.selected_hero))
            except Exception as e:
                print("[-] Couldn't load the model. Maybe the file is corrupted. Try to load older files. Error: ", e)
                exit()
            else:
                print('[+] Successfully loaded state model', self.selected_hero)


if __name__ == "__main__":
    running = False
    while True:
        print('[!] It is recommended that the names are not the same!')
        hero = input("[?] What should the bot play as? | Ex: thor-1 >> ").lower()
        if hero != "":
            print()
            print('[!] It is recommended that the names are not the same!')
            hero_save = input("[?] How do you want to save the learned model? | Ex: thor-2 >> ").lower()
            if hero_save != "":
                hero += '.pkl'
                hero_save += '.pkl'
                print()
                use_eyes = input("[?] Do you want to see when the bot sees (Y)es / (N)o ? >> ").lower()
                use_eyes = False if use_eyes != 'yes' and use_eyes != 'y' else True
                break

    ai = BrawlhallaAI(selected_hero=hero, use_eyes1=use_eyes, save_hero=hero_save)
    ai.load()

    def on_press(key):
        global running
        if str(key) == "'p'":
            # punishment for AI
            ai.give_punishment()
        elif str(key) == "'o'":
            # reward for AI
            ai.give_reward()
        elif str(key) == "'i'":
            # start the bot
            if not running:
                print("[+] Starting")
                threading.Thread(target=ai.generate_key_combination, daemon=True).start()
                running = True
        elif str(key) == "'k'":
            # save the learned
            ai.save()

    print('''
    
    
    [!] Listening for commands [!]
    
    Press   |  Action
             |
    p       |  Punishment for the bot. You press "p" when you don't like what the bot is doing.
           |
    o       |  Reward for the bot. You press "o" when you like what the bot is doing.
           |
    i       |   The bot starts playing and you can't do anything about it.
           | 
    k       |  You save when the bot has learned.
    
    ''')

    with Listener(on_press=on_press) as listener:
        listener.join()



























