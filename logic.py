import pydicom
from pydicom.data import get_testdata_file
import cv2

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