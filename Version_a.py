import tkinter as tk
from pynput import keyboard

class WPMTracker:
    MOVING_AVERAGE = 5
    IGNORED_KEYS = {
        keyboard.Key.backspace, keyboard.Key.shift_l, keyboard.Key.shift_r, 
        keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.alt_l, 
        keyboard.Key.alt_r, keyboard.Key.caps_lock, keyboard.Key.cmd
    }

    def __init__(self, parent):
        self.parent = parent
        self.history = [0] * self.MOVING_AVERAGE
        self.current_key_presses = 0
        self.show_suffix = True
        self.enable_smoothing = True
        self.lerping_wpm = 0
        self.current_wpm = 0

        # Configure parent window properties
        self.parent.title("WPM Counter")
        self.parent.overrideredirect(True)  # Hide the window decorations
        self.parent.wm_attributes("-topmost", True)  # Make window stay on top

        self.text_widget = tk.Text(parent, font=("Arial", 30), fg="red", bg="black", bd=0, highlightthickness=0)
        self.text_widget.pack(fill="both", expand=True)

        # Register the on_release function to be called when a key is released
        self.listener = keyboard.Listener(on_release=self.on_key_release)
        self.listener.start()

        self.update_wpm()

    def on_key_release(self, key):
        if hasattr(key, 'char'):
            if key not in self.IGNORED_KEYS:
                self.current_key_presses += 1

    def shift_history(self, last_value):
        self.history = self.history[1:] + [last_value]

    def calculate_wpm(self):
        return (sum(self.history) / self.MOVING_AVERAGE) / 5 * 60

    def update_wpm(self):
        self.shift_history(self.current_key_presses)
        self.current_key_presses = 0
        self.current_wpm = self.calculate_wpm()

        if self.enable_smoothing:
            self.lerping_wpm = self.lerp(self.lerping_wpm, self.current_wpm, 0.1)
        else:
            self.lerping_wpm = self.current_wpm

        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("end", f"{round(self.lerping_wpm)}" + (" WPM" if self.show_suffix else ""))
        self.parent.after(1000, self.update_wpm)

    def lerp(self, a, b, t):
        return (1 - t) * a + t * b

def main():
    root = tk.Tk()
    root.attributes("-transparentcolor", "black")  # Make the window transparent
    wpm_tracker = WPMTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
