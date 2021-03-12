from gui import *
import logic

def main():
    logic = Logic()
    #logic.load_dicom("img/0002.DCM")
    #logic.load_img("img/CT_ScoutView.jpg")
    #logic.create_square_image()
    gui = GUI("Tomograph", 920, 700, False)
  

if __name__ == '__main__':
    main()