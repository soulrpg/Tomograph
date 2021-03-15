import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import messagebox
import os
from logic import *

ITER_NUM = 180

class GUI:
    def __init__(self, title, WIDTH, HEIGHT, RESIZABLE):
        self.logic = Logic()
    
        # Tworzenie okna
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(str(WIDTH) + "x" + str(HEIGHT))
        self.window.resizable(RESIZABLE, RESIZABLE)
        
        # Specjalna zmienna, która przechowuje stan checkbuttona
        self.checkbutton_value = tk.IntVar()
        # Specjalna zmienna, która przechowuje stan slidera
        self.slider_value = tk.IntVar()
        
        # Glowna ramka
        self.container = ttk.Frame(self.window)
        self.container.pack()
        
        self.top_menu = ttk.Frame(self.container)
        self.top_menu.pack()
        
        self.top_menu_2 = ttk.Frame(self.container)
        self.top_menu_2.pack()
        
        path = os.getcwd() + "//img"
        filenames = list(os.listdir(path))
        
        # PIERWSZY WIERSZ
        self.file = ttk.Label(self.top_menu, text="Plik:")
        self.file.pack(side=tk.LEFT, pady=10)
        self.file_list = ttk.Combobox(self.top_menu, 
                            values=filenames)
        self.file_list.pack(side=tk.LEFT)
        
        self.loadButton = ttk.Button(self.top_menu, text="Ładuj", command=lambda: self.load_clicked())
        self.loadButton.pack(side = tk.LEFT)
        
        # DRUGI WIERSZ
        self.step = ttk.Label(self.top_menu_2, text="Krok alfa:")
        self.step.pack(side=tk.LEFT)
        
        self.stepEntry = ttk.Entry(self.top_menu_2, width = 5)
        self.stepEntry.insert(0, "2");
        self.stepEntry.pack(side = tk.LEFT)
        
        self.detectors = ttk.Label(self.top_menu_2, text="Liczba detektorów:")
        self.detectors.pack(side=tk.LEFT, padx=10)
        
        self.detectorsEntry = ttk.Entry(self.top_menu_2, width = 5)
        self.detectorsEntry.insert(0, "3")
        self.detectorsEntry.pack(side = tk.LEFT)
        
        self.range_span = ttk.Label(self.top_menu_2, text="Rozpiętość:")
        self.range_span.pack(side=tk.LEFT, padx=10)
        
        self.range_spanEntry = ttk.Entry(self.top_menu_2, width = 5)
        self.range_spanEntry.insert(0, "180");
        self.range_spanEntry.pack(side = tk.LEFT)
        
        self.checkbutton = ttk.Checkbutton(self.top_menu_2, text="Filtr splotu", offvalue = 0, onvalue = 1, command=lambda: self.                     checkbutton_change(), variable = self.checkbutton_value) 
        self.checkbutton.pack(side = tk.LEFT, padx=10)
        
        self.startButton = ttk.Button(self.top_menu_2, text="Start", command=lambda: self.start_clicked())
        self.startButton.pack(side = tk.LEFT, padx=10)
        
        self.slider = ttk.Scale(self.top_menu_2, variable = self.slider_value,  
           from_ = 1, to = 20,  
           orient = tk.HORIZONTAL)
        self.slider.pack(side = tk.LEFT, padx=10)
        
        # Uruchamianie petli zdarzen
        self.window.mainloop()
        
    def load_clicked(self):
        if self.file_list.get()[-3:] == "DCM":
            self.logic.load_dicom("img/" + self.file_list.get())
        else:
            self.logic.load_img("img/" + self.file_list.get())
        
    def start_clicked(self):
        if type(self.logic.image) != None and len(self.stepEntry.get()) > 0 and len(self.detectorsEntry.get()) > 0 and len(self.range_spanEntry.get()) > 0 :
            self.logic.start_transform(ITER_NUM, float(self.stepEntry.get()), int(self.detectorsEntry.get()), float(self.range_spanEntry.get()), self.checkbutton_value)
        
        #self.slider.destroy()
        #self.slider = ttk.Scale(self.top_menu_2, variable = self.slider_value,  
        #   from_ = 1, to = ITER_NUM,  
        #   orient = tk.HORIZONTAL)
        #self.slider.pack(side = tk.LEFT, padx=10)
        
    def checkbutton_change(self):
        print(self.checkbutton_value.get())