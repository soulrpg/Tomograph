import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import messagebox
import os
from logic import *

class GUI:
    def __init__(self, title, WIDTH, HEIGHT, RESIZABLE):
        # Tworzenie okna
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(str(WIDTH) + "x" + str(HEIGHT))
        self.window.resizable(RESIZABLE, RESIZABLE)
        
        # Glowna ramka
        self.container = ttk.Frame(self.window)
        self.container.pack()
        
        self.top_menu = ttk.Frame(self.container)
        self.top_menu.pack()
        
        path = os.getcwd() + "//img"
        filenames = list(os.listdir(path))
        
        self.file = ttk.Label(self.top_menu, text="Plik:")
        self.file.pack(side=tk.LEFT, pady=10)
        self.file_list = ttk.Combobox(self.top_menu, 
                            values=filenames)
        self.file_list.pack(side=tk.LEFT)
        
        # Uruchamianie petli zdarzen
        self.window.mainloop()