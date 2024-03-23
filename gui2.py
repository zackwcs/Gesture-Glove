import tkinter
import customtkinter
import msvcrt
import os

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.predefinedGestures = []

        self.gestures = {
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

        # configure window
        self.title("Glove Gui.py")
        self.geometry(f"{1100}x{580}")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

         # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Predefined Gestures", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.my_frame =  customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=1, sticky="nsew")
        self.my_frame.grid_columnconfigure(0, weight=1)

        self.widgets = [] 

        self.event_label = customtkinter.CTkLabel(self.my_frame, text="Gesture:",  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.event_label.grid(row=0, column=0, sticky="w", padx=40, pady=10)

        customtkinter.CTkLabel(self.my_frame, text="").grid(row=0, column=1, sticky="ew", padx=40, pady=10)

        self.event_name = customtkinter.CTkLabel(self.my_frame, text="Keybind",  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.event_name.grid(row=0, column=2, sticky="w", padx=0, pady=10)

        customtkinter.CTkLabel(self.my_frame, text="").grid(row=0, column=3, sticky="ew", padx=40, pady=10)

        self.rebind_name = customtkinter.CTkLabel(self.my_frame, text="Rebind Gesture",  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.rebind_name.grid(row=0, column=4, sticky="w", padx=40, pady=10)

        self.create_gesture()

    def create_gesture(self):
        for index, (gesture, keybind) in enumerate(self.gestures.items()):
            label = customtkinter.CTkLabel(self.my_frame, text=gesture,  font=customtkinter.CTkFont(size=20, weight="bold"))
            label.grid(row=index+1, column=0, sticky="w", padx=40, pady=10)

            customtkinter.CTkLabel(self.my_frame, text="").grid(row=index+1, column=1, sticky="ew", padx=40, pady=10)

            keybind_text = customtkinter.CTkLabel(self.my_frame, text=keybind)
            keybind_text.grid(row=index+1, column=2, sticky="w", padx=40, pady=10)

            customtkinter.CTkLabel(self.my_frame, text="").grid(row=index+1, column=3, sticky="ew", padx=40, pady=10)

            rebind_button = customtkinter.CTkButton(self.my_frame, text="Rebind", command=lambda label=label, text=keybind_text: self.rebind_key(label, text))
            rebind_button.grid(row=index+1, column=4, padx=40, pady=10)

            # Add all the corresponding labels and buttons for each gesture to a widget list
            self.widgets.append((label, keybind_text, rebind_button))

    def create_gesture_combo(self, index, gestureData):
        gestures = customtkinter.CTkButton(self.sidebar_frame, text="Preset " + str(index + 1), command=lambda: self.updateGestures(gestureData))
        gestures.grid(row=index+1, column=0, padx=40, pady=10)

    def updateGestures(self, gestureData):
        gesture_keys = list(gestureData.keys())
        gesture_values = list(gestureData.values())
        #print(gesture_keys)
        with open("gestures.txt", "w") as file:
            msvcrt.locking(file.fileno(), 1, 0)
            for index, widget in enumerate(self.widgets):
                value = gesture_values[index]
                widget[1].configure(text=value)
            

                
                file.write(widget[0].cget("text") + "\n")
                file.write(widget[1].cget("text") + "\n")
        
            msvcrt.locking(file.fileno(), 8, 0)

    def rebind_key(self, label, text):
        for widget in self.widgets:
            if widget[0] == label and widget[1] == text:
                button = widget[2]
                break
        button.configure(state="disabled")
        text.configure(text="Press a key...")

        self.bind("<Key>",  lambda event, label=label, text=text, button=button: self.update_keybind(event, label, text, button))

    def update_keybind(self, event, label, text, button):
        key_pressed = event.keysym
        text.configure(text=key_pressed)

        # Unbind the key
        self.unbind("<Key>")

        # Enable the rebind button
        button.configure(state="normal")
        self.update_gesture(label, text)

    def update_gesture(self, label, text):
        gestureSent = label.cget("text")
        textSent = text.cget("text")

        with open("gestures.txt", "w") as file:
            msvcrt.locking(file.fileno(), 1, 0)
            file.write(gestureSent + "\n")
            file.write(textSent + "\n")
            msvcrt.locking(file.fileno(), 8, 0)

        file.close()

    def parse_Gestures(self):
        data = [] 
        gestures = {}
        gesture = None
        keybind = None

        with open("predefinedGestures.txt", 'r') as file:
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
                else:
                    data.append(gestures.copy())
                    gestures = {}

        if gestures:
            data.append(gestures.copy())

        return data

    
if __name__ == "__main__":
    gui = Gui()
    
    gui.predefinedGestures = gui.parse_Gestures()
    print(gui.predefinedGestures)
    for i, gest in enumerate(gui.predefinedGestures):
            gui.create_gesture_combo(i, gest)

    # Clear all text in gesture.txt if some are still stored when starting
    with open("gestures.txt", "w") as file:
            msvcrt.locking(file.fileno(), 1, 0)
            file.truncate(0)
            msvcrt.locking(file.fileno(), 8, 0)

    gui.mainloop()