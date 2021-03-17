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
        # 
        self.slider_text_value = tk.StringVar()
        
        self.slider_text_value.set("1")
        
        self.rmse_text_value = tk.StringVar()
        self.rmse_text_value.set("RMSE: -")
       
        
        # Glowna ramka
        self.container = ttk.Frame(self.window)
        self.container.pack()
        
        self.top_menu = ttk.Frame(self.container)
        self.top_menu.pack()
        
        self.top_menu_2 = ttk.Frame(self.container)
        self.top_menu_2.pack()
        
        self.bottom_menu = ttk.Frame(self.container)
        self.bottom_menu.pack(side = tk.BOTTOM)
        
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
        
        self.iter = ttk.Label(self.top_menu_2, textvariable=self.slider_text_value)
        self.iter.pack(side=tk.LEFT, padx=10)
        
        
        self.slider = ttk.Scale(self.top_menu_2, variable = self.slider_text_value,  
           from_ = 1, to = 20,  
           orient = tk.HORIZONTAL)
        self.slider.pack(side = tk.LEFT, padx=10)
        
        # Wynik RMSE
        self.rmse_text = ttk.Label(self.bottom_menu, textvariable=self.rmse_text_value)
        self.rmse_text.pack(side=tk.LEFT, padx=20)
        
        self.form_button = ttk.Button(self.bottom_menu, text="Formularz DICOM", command=lambda: self.form_open())
        self.form_button.pack(side=tk.LEFT, padx=10)
        
        
        
        # Uruchamianie petli zdarzen
        self.window.mainloop()
        
    def load_clicked(self):
        if self.file_list.get()[-3:] == "DCM":
            self.logic.load_dicom("img/" + self.file_list.get())
        else:
            self.logic.load_img("img/" + self.file_list.get())
        
    def start_clicked(self):
        if type(self.logic.image) != None and len(self.stepEntry.get()) > 0 and len(self.detectorsEntry.get()) > 0 and len(self.range_spanEntry.get()) > 0 :
            self.logic.start_transform(ITER_NUM, float(self.stepEntry.get()), int(self.detectorsEntry.get()), float(self.range_spanEntry.get()), self.checkbutton_value.get())
        self.slider.destroy()
        self.slider = ttk.Scale(self.top_menu_2, variable = self.slider_value,  
           from_ = 1, to = int(360/float(self.stepEntry.get())),  
           orient = tk.HORIZONTAL)
        self.slider.bind("<ButtonRelease-1>", self.sliderUpdate)
        self.slider.pack(side = tk.LEFT, padx=10)
        tmp_rmse_result = "RMSE: " + str(round(self.logic.rmse(), 2))
        print("TMP:", tmp_rmse_result)
        self.rmse_text_value.set(tmp_rmse_result)
        self.window.update_idletasks()
        self.window.update()
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
        
    def sliderUpdate(self, event):
        iter_num = int(self.slider.get())
        print("Slider iter:", iter_num)
        self.slider_text_value.set(str(int(self.slider.get())))
        result = self.logic.get_iter(iter_num)
        self.window.update_idletasks()
        self.window.update()
        cv2.imshow('Odwrotna transformacja iter', np.array(result, dtype=np.uint8))
        cv2.waitKey(0)
        cv2.destroyAllWindows()     
        
    def checkbutton_change(self):
        print(self.checkbutton_value.get())
        
    def form_open(self):
        self.logic.dicom.show_form(self.window)