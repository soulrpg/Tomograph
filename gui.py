import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import messagebox
import os
from logic import *
from PIL import Image, ImageTk

ITER_NUM = 180

CANVAS_WIDTH = 1100
CANVAS_HEIGHT = 540

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
        
        self.top_menu_3 = ttk.Frame(self.container)
        self.top_menu_3.pack()
        
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
        
        # Trzeci wiersz - CANVAS
        
        self.canvas = tk.Canvas(self.top_menu_3, bg="black", width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.pack()
        
        
        
        # Uruchamianie petli zdarzen
        self.window.mainloop()
        
    def load_clicked(self):
        if self.file_list.get()[-3:] == "DCM":
            self.logic.load_dicom("img/" + self.file_list.get())
        else:
            self.logic.load_img("img/" + self.file_list.get())

        #kod niczym z redrawCanvas aby wyswietlic 1 obraz po zaladowaniu
        cv2.imwrite("imgSaved/imgOrginal.jpg", self.logic.image)
        img_orginal = cv2.imread("imgSaved/imgOrginal.jpg")
        img_orginal = cv2.rectangle(img_orginal, (0, 0), (img_orginal.shape[0] - 1, img_orginal.shape[1] - 1),
                                    (240, 240, 240), 1)

        scale = self.getScaleRatio(img_orginal.shape)

        self.stackedImg = ImageTk.PhotoImage(
            image=Image.fromarray(self.stackImages(scale, ([img_orginal]))))

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.stackedImg)
        self.canvas.update()
        self.window.update_idletasks()
        self.window.update()



    def start_clicked(self):
        if type(self.logic.image) != None and len(self.stepEntry.get()) > 0 and len(self.detectorsEntry.get()) > 0 and len(self.range_spanEntry.get()) > 0 :
            tmp = self.logic.start_transform(ITER_NUM, float(self.stepEntry.get()), int(self.detectorsEntry.get()), float(self.range_spanEntry.get()), self.checkbutton_value.get())
        self.redrawCanvas(tmp)
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
        self.window.update_idletasks()
        self.window.update()
        self.logic.inverse_radeon_transform(iter_num)
        cv2.imshow('Sinogram iter', np.array(self.logic.sinogram[0:iter_num][:], dtype=np.uint8))
        cv2.waitKey(0)
        cv2.destroyAllWindows()    

    def redrawCanvas(self, img):
        #dimensions = (CANVAS_WIDTH, CANVAS_HEIGHT)
        #resized = cv2.resize(img, dimensions, interpolation = cv2.INTER_AREA)
        #img = cv2.cvtColor(resized, cv2.COLOR_GRAY2RGB)
        #im = Image.fromarray(img)
        # Musi byc utworzony jako self gdyz w innym przypadku nie jest przechowywany w pamieci
        #self.new_img = ImageTk.PhotoImage(image = im)

        cv2.imwrite("imgSaved/imgResult.jpg",self.logic.result_image)
        #odczytuje z pliku bo cos nie dzialalo z obrazem, tak lawtiej
        img_orginal = cv2.imread("imgSaved/imgOrginal.jpg")
        img_result = cv2.imread("imgSaved/imgResult.jpg")

        img_orginal = cv2.rectangle(img_orginal, (0, 0), (img_orginal.shape[0] - 1, img_orginal.shape[1] - 1), (240, 240, 240),1)
        img_result = cv2.rectangle(img_result, (0,0), (img_result.shape[0]-1,img_result.shape[1]-1), (200,240,240), 1)

        scale = self.getScaleRatio(img_orginal.shape)

        self.stackedImg =  ImageTk.PhotoImage(image=Image.fromarray(self.stackImages(scale,([img_orginal,img_result])) ))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.stackedImg)
        self.canvas.update()
        self.window.update_idletasks()
        self.window.update()

        
    def checkbutton_change(self):
        print(self.checkbutton_value.get())
        
    def form_open(self):
        self.logic.dicom.show_form(self.window)


    def stackImages(self, scale, imgArray):
        rows = len(imgArray)
        cols = len(imgArray[0])
        rowsAvailable = isinstance(imgArray[0], list)
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]
        if rowsAvailable:
            for x in range(0, rows):
                for y in range(0, cols):
                    if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                    else:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                    None, scale, scale)
                    if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank] * rows
            hor_con = [imageBlank] * rows
            for x in range(0, rows):
                hor[x] = np.hstack(imgArray[x])
            ver = np.vstack(hor)
        else:
            for x in range(0, rows):
                if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                    imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
                else:
                    imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale,
                                             scale)
                if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            hor = np.hstack(imgArray)
            ver = hor
        return ver

    def getScaleRatio(self,shapeTab):
        ratioWidth = shapeTab[0]*2/ CANVAS_WIDTH
        ratioHeight = shapeTab[1] / CANVAS_HEIGHT
        scale = 1.0
        if (max(ratioWidth, ratioHeight) > 1):
            scale = 1.0 / max(ratioWidth, ratioHeight)
        return scale
