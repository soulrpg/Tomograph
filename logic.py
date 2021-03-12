import pydicom
from pydicom.data import get_testdata_file
import cv2
import numpy as np
import math
import copy

class Logic:
    def __init__(self):
        self.image = None
        self.angle = 0
        self.emiter_pos = [None, None]
        self.detectors_pos = []
        self.sinogram = []
        
    # Metoda rozpoczynajaca obliczenia
    def start_transform(self, iters, step, detectors_num, range_span, filter=False):
        self.create_square_image()
        self.image_copy = self.image.copy()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Wejscie', self.image)
        self.iters = iters
        self.step = math.radians(step)
        for i in range(detectors_num):
            self.detectors_pos.append([None, None])
        self.range_span = range_span
        self.filter = filter
        self.radius = self.image.shape[0]/2
        self.sinogram = []
        # Właściwy algorytm
        for i in range(self.iters):
            self.set_positions()
            self.sinogram.append([])
            cv2.circle(self.image_copy, (int(self.emiter_pos[1]), int(self.emiter_pos[0])), 5, (0,255,0), -1)
            for j in range(detectors_num):
                path = self.bresenham_line(self.emiter_pos, self.detectors_pos[j])
                print(self.detectors_pos[j])
                cv2.circle(self.image_copy, (int(self.detectors_pos[j][1]), int(self.detectors_pos[j][0])), 5, (0,0,255), -1)
                value = 0
                for coord in path:
                    value += self.image[min(coord[1], self.image.shape[0] - 1), min(coord[0], self.image.shape[0] - 1)]
                    self.image_copy[min(coord[1], self.image.shape[0] - 1), min(coord[0], self.image.shape[0] - 1)] = [255, 0, 0] 
                self.sinogram[i].append(value)
            self.angle += self.step
            cv2.imshow('Linia', self.image_copy)
        max_value = 0
        for line in self.sinogram:
            if max(line) > max_value:
                max_value = max(line)
        for line in self.sinogram:
            print(line)
            for i in range(len(line)):
                if max_value != 0:
                    line[i] = elem/max_value * 255
                else:
                    break
        cv2.imshow('Sinogram', np.array(self.sinogram, dtype=np.uint8))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    # Jezeli nie mamy pliku DICOM - tylko sam obrazek
    def load_img(self, filename):
        self.image = cv2.imread(filename)
        print("Img loaded!")
    
    def load_dicom(self, filename):
        ds = pydicom.dcmread(filename)
        # ds.pixel_array -> zwraca obrazek z formatu dicom
        print(ds)
        self.image = ds.pixel_array 
        # ds.PatientName -> zwraca nazwisko i imie
        # ds.PatientAge, ds.PatientSex, ds.BodyPartExamined, ds.PatientID, ds.PatientBirthDate ds.StudyDate, 
        # nie wiem jakie metapole odpowiada za komentarz?
        print(ds.PatientName)
        
    # Zmienia prostokatny obrazek na kwadratowy i przemnaza jego rozmiar w obu wymiarach o sqrt(2) 
    def create_square_image(self):
        size = max(self.image.shape)
        size = math.ceil(size * math.sqrt(2))
        height, width, _ = self.image.shape
        square_image = np.zeros((size, size, 3), np.uint8)
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
        delta_x = end[0] - begin[0]
        delta_y = end[1] - begin[1]
        if delta_x > delta_y: # x to driving axis
            m = delta_y / delta_x
            i1 = math.floor(begin[0])
            j = math.floor(begin[1])
            i2 = math.floor(end[0])
            error = -(1 - (begin[1] - j) - delta_y * ((1 - (begin[0]-i1))/delta_x))
            for i in range(i1, i2):
                path.append([i, j])
                if error >= 0:
                    j += 1
                    error -= 1.0
                i += 1
                error += m
        else:
            m = delta_x / delta_y 
            i1 = math.floor(begin[1])
            j = math.floor(begin[0])
            i2 = math.floor(end[1])
            error = -(1 - (begin[0] - j) - delta_x * ((1 - (begin[1]-i1))/delta_y))
            for i in range(i1, i2):
                path.append([j, i])
                if error >= 0:
                    j += 1
                    error -= 1.0
                i += 1
                error += m
        return path
                
        
        
        
        
        
        