import time
import keyboard

from pynput.keyboard import Controller


class Writer:
    to_write: list

    def __init__(self):
        self.to_write = []

    def add_hotkey(self, keys):
        self.to_write.append((keys, 'hotkey'))

    def add_key(self, key):
        self.to_write.append((key, 'key'))

    def add_text(self, text):
        try:
            last_was_hotkey = self.to_write[-1][1] == 'hotkey'
        except IndexError:
            last_was_hotkey = False

        if last_was_hotkey:  # Sometimes we need time to process hotkeys
            self.add_wait(0.2)
            self.to_write.append((text, 'text'))
            self.add_wait(0.2)
        else:
            self.to_write.append((text, 'text'))

    def add_wait(self, seconds):
        self.to_write.append((seconds, 'wait'))

    def add_start_pressing(self, key):
        self.to_write.append((key, 'start_pressing'))

    def add_stop_pressing(self, key):
        self.to_write.append((key, 'stop_pressing'))

    def execute(self):
        controller = Controller()

        for element, element_type in self.to_write:
            if element_type == 'hotkey':
                pressed = []

                for key in element[:-1]:
                    controller.press(key)
                    pressed.insert(0, key)

                controller.press(element[-1])
                controller.release(element[-1])

                for key in pressed:
                    controller.release(key)
            elif element_type == 'key':
                controller.press(element)
                controller.release(element)
            elif element_type == 'text':
                keyboard.write(element)
            elif element_type == 'wait':
                time.sleep(element)
            elif element_type == 'start_pressing':
                controller.press(element)
            elif element_type == 'stop_pressing':
                controller.release(element)
