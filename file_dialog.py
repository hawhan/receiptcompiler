import tkinter as tk
from tkinter import filedialog
import sys

def select_files():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    files = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")])
    root.destroy()
    
    # Print files separated by a delimiter (e.g., |)
    if files:
        print("|".join(files))

if __name__ == "__main__":
    select_files()
