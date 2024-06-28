import tkinter as tk
from pynput import keyboard
import time

class WPMCounter(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("WPM Counter")
        self.configure(bg="black")

        # Hide the window decorations
        self.overrideredirect(True)

        # Make window stay on top
        self.wm_attributes("-topmost", True)

        # Create a label widget for displaying WPM
        self.wpm_label = tk.Label(self, text="0 WPM", font=("Arial", 30), fg="white", bg="black")
        self.wpm_label.pack(expand=True)

        # Initialize variables
        self.key_press_times = []

        # Start listening to keyboard events
        self.listener = keyboard.Listener(on_release=self.on_release)
        self.listener.start()

        # Schedule the update function to run every second
        self.update_wpm()

    def on_release(self, key):
        # Record the timestamp of key press
        try:
            if hasattr(key, 'char') and key.char.isalnum():
                self.key_press_times.append(time.time())
        except:
            pass

    def update_wpm(self):
        # Calculate the start time of the rolling window (3 seconds ago)
        start_time = time.time() - 10

        # Count the number of key presses within the last 3 seconds
        key_presses = sum(1 for t in self.key_press_times if t >= start_time)

        # Calculate words per minute
        wpm = int((key_presses / 10 * 60)/4.6) if key_presses > 0 else 0

        # Update the WPM label
        self.wpm_label.config(text=f"{wpm} WPM")

        # Remove timestamps older than 3 seconds
        self.key_press_times = [t for t in self.key_press_times if t >= start_time]

        # Schedule the update function to run again after 1 second
        self.after(1000, self.update_wpm)

# Create and run the WPMCounter application
app = WPMCounter()
app.mainloop()
