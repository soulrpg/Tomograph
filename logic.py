import pydicom
from pydicom.data import get_testdata_file
import cv2
import numpy as np
import math

class Logic:
    def __init__(self):
        pass
    
    # Jezeli nie mamy pliku DICOM - tylko sam obrazek
    def load_img(self, filename):
        self.image = cv2.imread(filename)
    
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
        
    def brasenham_line(self, begin, end):
        pass