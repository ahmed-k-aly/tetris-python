from pynput.keyboard import Key, Controller

class GenerateInput():
    def __init__(self, action):
        self.action = action
        self.keyboard = Controller()



    def pressButton(self):
        if self.action == 'down':
            self.keyboard.press(Key.down)
        elif self.action == 'left':
            self.keyboard.press(Key.left)
        elif self.action == 'right':
            self.keyboard.press(Key.right)
        elif self.action == 'downRight':
            self.keyboard.press(Key.down)
            self.keyboard.press(Key.right)
        elif self.action == 'downLeft':
            self.keyboard.press(Key.down)
            self.keyboard.press(Key.left)
        elif self.action == 'R_rotate':
            self.keyboard.press(Key.up)
        elif self.action == 'L_rotate':
            self.keyboard.press('z')
        elif self.action == 'restart':
            self.keyboard.press(Key.enter)
        
        
    def releaseButton(self):
        if self.action == 'down':
            self.keyboard.release(Key.down)
        elif self.action == 'left':
            self.keyboard.release(Key.left)
        elif self.action == 'right':
            self.keyboard.release(Key.right)
        elif self.action == 'downRight':
            self.keyboard.release(Key.down)
            self.keyboard.release(Key.right)
        elif self.action == 'downLeft':
            self.keyboard.release(Key.down)
            self.keyboard.release(Key.left)
        elif self.action == 'R_rotate':
            self.keyboard.release(Key.up)
        elif self.action == 'L_rotate':
            self.keyboard.release("z")
        elif self.action == 'restart':
            self.keyboard.release(Key.enter)
