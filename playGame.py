from pynput.keyboard import Key, Controller

class GenerateInput():
    def __init__(self, action):
        self.action = action
        self.performAction()

    
    def performAction(self):
        keyboard = Controller()
        if self.action == 'down':
            keyboard.press("down")
            keyboard.release("down")
        elif self.action == 'left':
            keyboard.press("left")
            keyboard.release("left")
        elif self.action == 'right':
            keyboard.press("right")
            keyboard.release("right")
        elif self.action == 'downRight':
            keyboard.press("down")
            keyboard.press("right")
            keyboard.release("down")
            keyboard.release("right")
        elif self.action == 'downLeft':
            keyboard.press("down")
            keyboard.press("left")
            keyboard.release("down")
            keyboard.release("left")
        elif self.action == 'R_rotate':
            keyboard.press('up')
            keyboard.release('up')
        elif self.action == 'L_rotate':
            keyboard.press('z')
            keyboard.release("z")
        elif self.action == 'restart':
            keyboard.press('enter')
            keyboard.release('enter')
        