import pyautogui
import serial
import sys
import time
import select
import threading
import msvcrt
import os

class KeybindEditor:
    def __init__(self):
        self.keybinds = {
            "Index & Thumb": "right",
            "Middle & Thumb": "left",
            "Ring & Thumb": "space",
            "Pinky & Thumb": "f",
            "Make a Fist": "esc",
            "Only Index Finger Down": "up",
            "Only Middle Finger Down": "down",
            "Only Ring Finger Down": "m",
            # Add more events and default keybinds here
        }

        # Define triggers for each event
        self.event_triggers = {
            "Index & Thumb": False,
            "Middle & Thumb": False,
            "Ring & Thumb": False,
            "Pinky & Thumb": False,
            "Make a Fist": False,
            "Finger Gun": False,
            "Only Index Finger Down": False,
            "Only Middle Finger Down": False,
            "Only Ring Finger Down": False,
            # Add more events and triggers here
        }

    def save_keybind(self, event_name, new_keybind):
        old_keybind = self.keybinds[event_name]
        self.keybinds[event_name] = new_keybind
        print(f"Keybind for {event_name} updated to {new_keybind}")

        # Rebind the event with the new keybind
        self.rebind_event(event_name, old_keybind, new_keybind)

    def rebind_event(self, event_name, old_keybind, new_keybind):
        if old_keybind:
            pyautogui.hotkey('ctrl', 'alt', 'shift', old_keybind)
        pyautogui.hotkey('ctrl', 'alt', 'shift', new_keybind)

    def event_handler(self, event_name):
        if self.event_triggers[event_name]:
            print(f"Performing action for {event_name} event with keybind {self.keybinds[event_name]}")
            self.simulate_keybind(event_name)

    def simulate_keybind(self, event_name):
        keybind = self.keybinds[event_name]
        print(f"Simulating keybind '{keybind}' for event '{event_name}'")
        pyautogui.press(keybind)

def read_sensor_data():
    ser = serial.Serial('COM4', 9600, timeout=1)
    time.sleep(0.4)  # Allow some time for the Arduino to reset
    
    try:
        while True:
            read_pipeline()
            line = ser.readline().decode('utf-8').strip()

            if line == "Idle":
                print("Idle")
            elif line == "Waiting":
                print("Waiting")
            elif line == "Index Gesture":
                print("Index & Thumb")
                keybind_editor.event_triggers["Index & Thumb"] = True
            elif line == "Middle Gesture":
                print("Middle & Thumb")
                keybind_editor.event_triggers["Middle & Thumb"] = True
            elif line == "Ring Gesture":
                print("Ring & Thumb")
                keybind_editor.event_triggers["Ring & Thumb"] = True
            elif line == "Pinky Gesture":
                print("Pinky & Thumb")
                keybind_editor.event_triggers["Pinky & Thumb"] = True
            elif line == "ALL FLEXED":
                print("Make a Fist")
                keybind_editor.event_triggers["Make a Fist"] = True
            elif line == "Finger Gun":
                print("Finger Gun")
                keybind_editor.event_triggers["Finger Gun"] = True
            elif line == "IndexFlexed Gesture":
                print("Only Index Finger Down")
                keybind_editor.event_triggers["Only Index Finger Down"] = True
            elif line == "MiddleFlexed Gesture":
                print("Only Middle Finger Down")
                keybind_editor.event_triggers["Only Middle Finger Down"] = True
            elif line == "RingFlexed Gesture":
                print("Only Ring Finger Down")
                keybind_editor.event_triggers["Only Ring Finger Down"] = True


            for event_name, trigger in keybind_editor.event_triggers.items():
                if trigger:
                    keybind_editor.event_handler(event_name)
                    keybind_editor.event_triggers[event_name] = False 

            time.sleep(0.1)  
    except KeyboardInterrupt:
        ser.close()

def read_pipeline():
    gestures = {}  
    gesture = None  
    keybind = None

    with open("gestures.txt", 'r') as file:
        for line in file:
            line = line.strip()  
            if line:
                if gesture is None:
                    gesture = line
                else:
                    keybind = line
                    gestures[gesture] = keybind
                    gesture = None
                    keybind = None

    if len(gestures) > 0:
        

        for g, key in gestures.items():
            for gest, k in keybind_editor.keybinds.items():
                if g== gest:
                    keybind_editor.keybinds[gest] = key
                    print("inside identified\n")
                    print(keybind_editor.keybinds)
                    break

        with open("gestures.txt", "w") as file:
                msvcrt.locking(file.fileno(), 1, 0)
                file.truncate(0)
                msvcrt.locking(file.fileno(), 8, 0)

    file.close()
  

def main():
    global keybind_editor
    keybind_editor = KeybindEditor()

    read_sensor_data()

if __name__ == "__main__":
    main()
