import pydicom
from pydicom.data import get_testdata_file
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
import datetime
from datetime import date
import os
import tempfile

import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import messagebox

class Dicom:
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.sex = "K"
        self.age = "0"
        self.birth_date = "//"
        self.body_part = ""
        self.comment = ""
        self.patient_id = ""
        self.image = None
        
    def load_from_dcm(self, filename):
        self.ds = pydicom.dcmread(filename)
        print(self.ds)
        print(self.ds.PatientName)
        self.last_name = str(self.ds.PatientName).split("^")[0]
        self.first_name = str(self.ds.PatientName).split("^")[1]
        if hasattr(self.ds, 'PatientID'):
            self.patient_id = self.ds.PatientID
        if hasattr(self.ds, 'PatientSex'):
            self.sex = self.ds.PatientSex
        if hasattr(self.ds, 'PatientAge'):
            self.age = self.ds.PatientAge
        if hasattr(self.ds, 'PatientBirthDate'):
            self.birth_date = self.ds.PatientBirthDate
        if hasattr(self.ds, 'BodyPartExamined'):
            self.body_part = self.ds.BodyPartExamined
        if hasattr(self.ds, 'PatientComments'):
            self.comment = self.ds.PatientComments
        self.image = self.ds.pixel_array
        
    def set_image(self, img):
        # Dla zapisywania
        self.image = img
        
    def save_to_dcm(self):
        print("Setting file meta information...")
        # Populate required values for file meta information
        file_meta = FileMetaDataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
        file_meta.MediaStorageSOPInstanceUID = "1.2.3"
        file_meta.ImplementationClassUID = "1.2.3.4"
        file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
        #file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'#pydicom.uid.ImplicitVRLittleEndian
        print("Setting dataset values...")
        # Create the FileDataset instance (initially no data elements, but file_meta
        # supplied)
        tmp_ds = FileDataset(self.file_name_field.get(), {}, file_meta=file_meta, preamble=b"\0" * 128)
        
        tmp_ds.SOPClassUID = "123"
        tmp_ds.SOPInstanceUID = "123"
        tmp_ds.StudyInstanceUID = "123"
        tmp_ds.SeriesInstanceUID = "123"
        tmp_ds.Modality = "CT"
        tmp_ds.ImageType = ['ORIGINAL', 'PRIMARY', 'AXIAL']
        
        # Set the transfer syntax
        tmp_ds.is_little_endian = True
        tmp_ds.is_implicit_VR = True

        # Set creation date/time
        dt = datetime.datetime.now()
        tmp_ds.ContentDate = dt.strftime('%Y%m%d')
        timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
        tmp_ds.ContentTime = timeStr
        
        tmp_ds.PatientName = self.last_name_field.get() + "^" + self.first_name_field.get()
        tmp_ds.PatientID = self.id_field.get()
        tmp_ds.PatientAge = self.age_field.get()
        tmp_ds.PatientSex = self.sex_field.get()
        tmp_ds.BodyPartExamined = self.body_part_field.get()
        tmp_ds.PatientBirthDate = self.birth_date_field.get()
        tmp_ds.PatientComments = self.comment_entry.get("1.0", tk.END)
        tmp_ds.StudyID = ""
        tmp_ds.SeriesInstanceUID = tmp_ds.StudyInstanceUID = pydicom.uid.generate_uid()
        
        tmp_ds.PixelData = self.image#.tobytes()
        
        tmp_ds.BitsAllocated = 8
        tmp_ds.Rows = self.image.shape[0]
        tmp_ds.Columns = self.image.shape[1]
        tmp_ds.PixelRepresentation = 0
        tmp_ds.SamplesPerPixel = 1
        tmp_ds.PhotometricInterpretation = "MONOCHROME2"
        tmp_ds.NumberOfFrames = 1
        tmp_ds.PlanarConfiguration = 0
        tmp_ds.BitsAllocated = 8
        tmp_ds.BitsStored = 8
        tmp_ds.HighBit = 7

        print("Writing test file", self.file_name_field.get())
        tmp_ds.save_as("img/" + self.file_name_field.get(), write_like_original=False)
        print("File saved.")

        
    def show_form(self, master):
        # Tworzenie nowego okna na formularz
        self.form = tk.Toplevel(master)
        self.form.title("DICOM")
        self.form.geometry("250x500")
        
        # ID pacjenta
        self.id_label = ttk.Label(self.form, text="ID pacjenta:")
        self.id_label.pack(side=tk.TOP)
             
        self.id_field = ttk.Entry(self.form, width=30)
        self.id_field.pack(side=tk.TOP)
             
        self.id_field.insert(0, self.patient_id)
        
        # Imię
        self.first_name_label = ttk.Label(self.form, text="Imię:")
        self.first_name_label.pack(side=tk.TOP)
        
        self.first_name_field = ttk.Entry(self.form, width=30)
        self.first_name_field.pack(side=tk.TOP)
        
        self.first_name_field.insert(0, self.first_name)
        
        # Nazwisko
        self.last_name_label = ttk.Label(self.form, text="Nazwisko:")
        self.last_name_label.pack(side=tk.TOP)
             
        self.last_name_field = ttk.Entry(self.form, width=30)
        self.last_name_field.pack(side=tk.TOP)
        
        self.last_name_field.insert(0, self.last_name)
        
        # Wiek
        self.age_label = ttk.Label(self.form, text="Wiek:")
        self.age_label.pack(side=tk.TOP)
             
        self.age_field = ttk.Entry(self.form, width=30)
        self.age_field.pack(side=tk.TOP)
        
        self.age_field.insert(0, self.age)
        
        # Płeć
        self.sex_label = ttk.Label(self.form, text="Płeć:")
        self.sex_label.pack(side=tk.TOP)
             
        self.sex_field = ttk.Entry(self.form, width=30)
        self.sex_field.pack(side=tk.TOP)
             
        self.sex_field.insert(0, self.sex)
        
        # Badana część ciała
        self.body_part_label = ttk.Label(self.form, text="Badana część ciała:")
        self.body_part_label.pack(side=tk.TOP)
             
        self.body_part_field = ttk.Entry(self.form, width=30)
        self.body_part_field.pack(side=tk.TOP)
             
        self.body_part_field.insert(0, self.body_part)
        
        # Data urodzenia
        self.birth_date_label = ttk.Label(self.form, text="Data urodzenia [DD/MM/RRRR]:")
        self.birth_date_label.pack(side=tk.TOP)
             
        self.birth_date_field = ttk.Entry(self.form, width=30)
        self.birth_date_field.pack(side=tk.TOP)
             
        self.birth_date_field.insert(0, self.birth_date)
        
        # Komentarz
        self.comment_label = ttk.Label(self.form, text="Komentarz nt. pacjenta:")
        self.comment_label.pack(side=tk.TOP)
        
        self.comment_entry = tk.Text(self.form, height=5, width=30)
        self.comment_entry.insert(tk.INSERT, self.comment)
        self.comment_entry.pack(side=tk.TOP)
        
        # Nazwa pliku
        self.file_name_label = ttk.Label(self.form, text="Nazwa pliku:")
        self.file_name_label.pack(side=tk.TOP)
             
        self.file_name_field = ttk.Entry(self.form, width=30)
        self.file_name_field.pack(side=tk.TOP)
             
        self.file_name_field.insert(0, ".DCM")
        
        # Przycisk zapisu
        self.save_button = ttk.Button(self.form, text="Zapisz DICOM", command=lambda: self.save_to_dcm())
        self.save_button.pack(side=tk.TOP)
        
        
        
        
    #ds = pydicom.dcmread(filename)
    # ds.pixel_array -> zwraca obrazek z formatu dicom
    # print(ds)
    #self.image = ds.pixel_array 
    # ds.PatientName -> zwraca nazwisko i imie
    # ds.PatientAge, ds.PatientSex, ds.BodyPartExamined, ds.PatientID, ds.PatientBirthDate ds.StudyDate, 
    # nie wiem jakie metapole odpowiada za komentarz?