import pydicom
from pydicom.data import get_testdata_file
import cv2
import numpy as np
import math
import copy
from dicom import *

class Logic:
    def __init__(self):
        self.image = None
        self.angle = 0
        self.emiter_pos = [None, None]
        self.detectors_pos = []
        self.sinogram = []
        self.brehensam_path = []
        self.sinogram_filtered = []
        self.dicom = Dicom()

    # Metoda rozpoczynajaca obliczenia
    def start_transform(self, iters, step, detectors_num, range_span, filter=False):
        # Skopiowany konstruktor (w wiekszosci) - czyszcze informacje, zeby nie trzeba bylo otwierac GUI na nowo
        self.angle = 0
        self.emiter_pos = [None, None]
        self.detectors_pos = []
        self.sinogram = []
        self.brehensam_path = []
        self.sinogram_filtered = []
        
        self.iters = math.ceil(360/step)
        cv2.imshow('Wejscie', self.image)
        self.step = math.radians(step)
        for i in range(detectors_num):
            self.detectors_pos.append([None, None])
        self.range_span = math.radians(range_span)
        self.filter = filter
        self.radius = self.image.shape[0]/2
        self.sinogram = []
        # Tworzymy liste zapisujaca ile razy algorytm przechodzi przez kazdy pixel obrazu
        self.val_count = []
        for i in range(self.image.shape[1]):
            self.val_count.append([])
            self.val_count[i] = [0] * self.image.shape[0] 
        # Właściwy algorytm
        self.brehensam_path = []
        for i in range(self.iters):
            self.set_positions()
            self.sinogram.append([])
            cv2.circle(self.image_copy, (int(self.emiter_pos[0]), int(self.emiter_pos[1])), 5, (0,255,0), -1)
            for j in range(detectors_num):
                path = self.bresenham_line(copy.copy(self.emiter_pos), copy.copy(self.detectors_pos[j]))
                self.brehensam_path.append(path)
                cv2.circle(self.image_copy, (int(self. detectors_pos[j][0]), int(self.detectors_pos[j][1])), 5, (0,0,255), -1)
                value = 0
                for coord in path:
                    value += self.image[min(coord[1], self.image.shape[1] - 1), min(coord[0], self.image.shape[0] - 1)]
                    self.image_copy[min(coord[1], self.image.shape[1] - 1), min(coord[0], self.image.shape[0] - 1)] = [255, 0, 0] 
                self.sinogram[i].append(value)
            self.angle += self.step
            cv2.imshow('Linia', self.image_copy)
        max_value = 0
        # Normalizacja sinogramu
        for line in self.sinogram:
            if max(line) > max_value:
                max_value = max(line)
        for line in self.sinogram:
            #print(line)
            for i in range(len(line)):
                if max_value != 0:
                    line[i] = line[i]/max_value * 255
                else:
                    break
                    
        if self.filter:
            self.sinogram_filtered = []
            for line in self.sinogram:
                self.sinogram_filtered.append(self.convolution(line))
            cv2.imshow('FIltered sinogram', np.array(self.sinogram_filtered, dtype=np.uint8))
        else:
            cv2.imshow('Sinogram', np.array(self.sinogram, dtype=np.uint8))
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        self.inverse_radeon_transform()
        
        return self.result_image
        
    
    def convolution(self, row):
        row_fft = np.fft.fft(row)
        finall_row = [None] * len(row)

        k_max = int(len(row_fft) / 4)
        h = 0

        for i in range(len(row_fft)):
            sum = 0
            # dodatnie wartosci k
            for k in range(k_max):
                if k == 0:
                    h = 1
                elif k % 2 == 0:
                    h = 0
                else:
                    h = -4 / ((math.pi ** 2) * (k ** 2))
                sum += h * row_fft[i]

            # ujemne wartosci k
            for k in range(1, k_max):
                if k % 2 == 0:
                    h = 0
                else:
                    h = -4 / ((math.pi ** 2) * (k ** 2))

                if ((i - k) >= 0):
                    sum += h * row_fft[i - k]

            finall_row[i] = sum

        finall_row_clipped = np.fft.ifft(finall_row)
        finall_row_clipped = np.clip(finall_row_clipped, 0, 255)

        return finall_row_clipped

    # Przeksztalcenie sinogramu na obrazek
    def inverse_radeon_transform(self, iter=None):

        if self.filter:
            sinograme=self.sinogram_filtered;
        else:
            sinograme=self.sinogram;
            
        if type(iter) == type(None):
            iter = self.iters

        # Odwrotna transformacja
        self.angle = 0
        self.value_array = []
        print("Val count:", len(self.val_count))
        print("Val count i:", len(self.val_count[0]))
        print("image shape:", self.image.shape)
        for i in range(self.image.shape[0]):
            self.value_array.append([])
            for j in range(self.image.shape[1]):
                self.value_array[i].append(0)
        for i in range(iter):
            self.set_positions()
            for j in range(len(self.detectors_pos)):
                for coord in self.brehensam_path[j+(i*len(self.detectors_pos))]:
                    self.value_array[min(coord[1], self.image.shape[1]-1)][min(coord[0], self.image.shape[0]-1)] += sinograme[i][j]
                    # Odnotowujemy przejscie po danym pixelu
                    self.val_count[min(coord[1], self.image.shape[1] - 1)][min(coord[0], self.image.shape[0] - 1)] += 1
                    #self.value_array[min(coord[1], self.image.shape[1]-1)][min(coord[0], self.image.shape[0]-1)] = 255
            #self.inverse_base.append(copy.deepcopy(self.value_array))
            self.angle += self.step
            
        #print(self.val_count)
            
        # Normalizacja II - dzielimy kazda wartosc pixela przez ilosc lini jakie przeszly przez dany pixel
        #for i in range(len(self.value_array)):
        #    for j in range(len(self.value_array[i])):
        #        if self.val_count[i][j] != 0:
        #            self.value_array[i][j] /= self.val_count[i][j]
        #        else:
        #            if
        #            print(self.value_array[i][j])
        max_value = 0
        for line in self.value_array:
            if max(line) > max_value:
                max_value = max(line)
        for line in self.value_array:
            for i in range(len(line)):
                if max_value != 0:
                    line[i] = line[i]/max_value*255
                else:
                    break
        self.value_array = np.array(self.value_array, dtype=np.uint8)
        self.result_image = self.value_array #self.cut_picture()
        # Dla zapisywania jako plik DICOM
        self.dicom.set_image(self.result_image)
        if iter != self.iters:
            cv2.imshow('Odwrotna transformacja ucięta (iter x)', self.result_image)
        else:
            cv2.imshow('Odwrotna transformacja ucięta', self.result_image)
        print("RMSE:", self.rmse()) 

    def rmse(self):
        err = np.sum((self.original_image.astype("float") - self.result_image.astype("float")) ** 2)
        err /= float(self.original_image.shape[0] * self.result_image.shape[1])
        return math.sqrt(err)
        
    def cut_picture(self):
        print("Radius:", self.radius)
        print("Shape X/2:", self.old_image_shape[1]/2)
        print("Shape Y/2:", self.old_image_shape[0]/2)
        print(self.value_array.shape)
        #npic = pic[100:200, 100:200]
        npic = self.value_array[int(self.radius) - math.ceil(self.old_image_shape[1]/2): int(self.radius) + math.ceil(self.old_image_shape[1]/2), int(self.radius) - math.ceil(self.old_image_shape[0]/2): int(self.radius) + math.ceil(self.old_image_shape[0]/2)]
        print(npic.shape)
        return npic
         
    # Jezeli nie mamy pliku DICOM - tylko sam obrazek
    def load_img(self, filename):
        self.image = cv2.imread(filename)
        self.original_image = self.image.copy()
        self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        #self.create_square_image()
        self.image_copy = self.image.copy()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        print("Img loaded!")
    
    def load_dicom(self, filename):
        self.dicom.load_from_dcm(filename)
        self.image = self.dicom.image
        self.original_image = self.image.copy()
        #self.create_square_image()
        self.image_copy = self.image.copy()
        print(self.image.shape)
        print("DICOM Img loaded!")
        
    # Zmienia prostokatny obrazek na kwadratowy i przemnaza jego rozmiar w obu wymiarach o sqrt(2) 
    def create_square_image(self):
        self.old_image_shape = copy.copy(self.image.shape)
        size = max(self.image.shape)
        size = math.ceil(size * math.sqrt(2))
        height, width, square_image = None, None, None
        if len(self.image.shape) == 3:
            height, width, _ = self.image.shape
            square_image = np.zeros((size, size, 3), np.uint8)
        else:
            height, width = self.image.shape
            square_image = np.zeros((size, size), np.uint8)
        square_image[int((size-height)/2):int((size+height)/2), int((size-width)/2):int((size+width)/2)] = self.image
        self.image = square_image
        #cv2.imshow('image', self.image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
    # Ustawia pozycje emiterow i detektorow zaleznie od iteracji (kata)
    def set_positions(self):
        self.emiter_pos[0] = self.radius * math.cos(self.angle) + self.radius
        self.emiter_pos[1] = self.radius * math.sin(self.angle) + self.radius
        #print("Emiter:")
        #print(self.emiter_pos[0], self.emiter_pos[1])
        for i in range(len(self.detectors_pos)):
            self.detectors_pos[i][0] = self.radius * math.cos(self.angle + math.pi - (self.range_span/2) + (i * self.range_span/(len(self.detectors_pos)-1))) + self.radius
            self.detectors_pos[i][1] = self.radius * math.sin(self.angle + math.pi - (self.range_span/2) + (i * self.range_span/(len(self.detectors_pos)-1))) + self.radius 
            #print("Detektor:", i)
            #print(self.detectors_pos[i][0], self.detectors_pos[i][1])
    
    def bresenham_line(self, begin, end):
        path = []
        #print("Start point:", begin)
        #print("End point:", end)
        delta_x = abs(end[0] - begin[0])
        delta_y = abs(end[1] - begin[1])
        #print("Delta x:", delta_x)
        #print("Delta y:", delta_y)
        if delta_x > delta_y: # x to driving axis
            #print("X driving axis")
            if end[0] < begin[0]:
                end, begin = begin, end
            m = delta_y / delta_x
            i1 = math.floor(begin[0])
            j = math.floor(begin[1])
            i2 = math.floor(end[0])
            error = -(1 - (begin[1] - j) - delta_y * ((1 - (begin[0]-i1))/delta_x))
            for i in range(i1, i2):
                path.append([i, j])
                #print("Path:", i, j)
                if error >= 0:
                    if end[1] < begin[1]:
                        j -= 1
                    else:
                        j += 1
                    error -= 1.0
                i += 1
                error += m
        else: # Y to driving axis
            #print("Y driving axis")
            if end[1] < begin[1]:
                end, begin = begin, end
            m = delta_x / delta_y 
            i1 = math.floor(begin[1])
            j = math.floor(begin[0])
            i2 = math.floor(end[1])
            error = -(1 - (begin[0] - j) - delta_x * ((1 - (begin[1]-i1))/delta_y))
            for i in range(i1, i2):
                path.append([j, i])
                #print("Path:", j, i)
                if error >= 0:
                    if end[0] < begin[0]:
                        j -= 1
                    else:
                        j += 1
                    error -= 1.0
                i += 1
                error += m
        return path
                
        
        

