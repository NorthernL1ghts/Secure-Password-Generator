import tkinter as tk
from Window import Window

class EntryPoint:
    @staticmethod
    def Run():
        """Run the password generator with GUI."""
        root = tk.Tk()
        window = Window(root)
        root.mainloop()

if __name__ == "__main__":
    EntryPoint.Run()
