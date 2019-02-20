import pydicom
import numpy as np #is a standard to use this alias for NumPy package
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.font
import matplotlib.image as mpimg

from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Basics window interface
aplicacion = tk.Tk()
aplicacion.geometry("600x750")
text_frame = Frame(aplicacion)
text_frame.configure(bg='#177497')
text = tk.Text(text_frame, width = 90, height = 8)
text.pack(side=LEFT, padx=20, pady=10)

fig = Figure()
canvas = FigureCanvasTkAgg(fig, master=aplicacion)

title = 'pydicom image'
back = tk.Frame(master=aplicacion,bg='#177497')
back.master.title(title)
back.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
back.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window

img = PhotoImage(file='./medical2.png')   
#label title
aplicacion.titulolbl = tk.Label(master=back, text="MEDICAL IMAGES", anchor="center", font=("Ubuntu", 28), bg='#177497')
aplicacion.titulolbl.place(x=190, y=10)
#label
#aplicacion.imagenlbl = tk.Label(master=back, image=img)
#aplicacion.imagenlbl.grid(row=1, column=0, columnspan=2, rowspan=2, padx=10, pady=10, sticky=(N, S, E, W))

#function to choose the image 
def openfile():   
    archivo = tk.filedialog.askopenfile() #askdirectory()    
    dcmfile = archivo.name   
    print(dcmfile)         
    # Get ref file
    RefDs = pydicom.dcmread(dcmfile)#lstFilesDCM[0]
    # Load dimensions based on the number of rows, columns, and slices (along the Z axis)
    #ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))
    ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), 1)
    # The array is sized based on 'ConstPixelDims'
    ArrayDicom = np.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)
    ds = pydicom.dcmread(dcmfile)

    # store the raw image data
    ArrayDicom[:, :, 0] = ds.pixel_array
    #print(ds)
    print(ds.pixel_array) 
    print(ds.pixel_array.shape)# ds.pixel_array.shape returns the shape of a NumPy ndarray
    
    imageProcessing(ds)
    histogram(ds)
    
    img = np.flipud(ArrayDicom[:, :, 0])

    '''#histogram    
    hist,bins = np.histogram(img,256,[0,256])
    plt.hist(img.ravel(),256,[0,256])
    plt.title('Histogram')
    plt.show()'''

def setInfo(header):
    text.delete('1.0', END)
    text.config(state=NORMAL) 
    #variables with information about the dcm file     
    acquisition = header.data_element("MRAcquisitionType")
    modality = header.data_element("Modality")  
    study = header.data_element("StudyDescription")      
    protocol = header.data_element("ProtocolName") 
    patients_sex = header.data_element("PatientSex")
    patients_age = header.data_element("PatientAge")
    info = "*Image Dimension: " + str(header.pixel_array.shape)
    info += "\n*MR Acquisition Type: " + acquisition.value
    info += "\n*Modality: " + modality.value 
    info += "\n*Study Description: " + study.value
    info += "\n*Protocol Name: " + protocol.value    
    info += "\n*Patient's Sex: " + patients_sex.value
    info += "\n*Patient's Age: " + patients_age.value
    text.delete('1.0', END)
    text.insert('1.0', info)
    text.config(state=DISABLED)
    
def histogram(file):    
    rows = int(file.Rows)
    columns = int(file.Columns)
    pixelArray = file.pixel_array    
    array = [0]*65536
    
    for i in range(rows):
        for j in range(columns):
            array[pixelArray[i,j]]=array[pixelArray[i,j]]+1
            
    array = np.asarray(array)
    plt.plot(array)
    fig = plt.gcf()
    fig.canvas.set_window_title('Histogram')           
    plt.show()  

def imageProcessing(file):     
    text_frame.pack()  
    setInfo(file)    
    plt.set_cmap(plt.gray()) 
    imag = fig.add_subplot(111)    
    imag.imshow(np.flipud(file.pixel_array))             
    canvas.draw()        
              

'''
def convolution(imagen, kernel):
    
'''
#button to open the image
aplicacion.abrirbtn = tk.Button(master=back, text="Open image", command=openfile)
aplicacion.abrirbtn.pack(side="top")
aplicacion.abrirbtn.place(x=50, y=70)
#cbb 

#button to close the app
aplicacion.quit = tk.Button(master=back, text="Exit", fg="red", command=aplicacion.destroy)
aplicacion.quit.pack(side="top")
aplicacion.quit.place(x=500, y=70)

canvas.get_tk_widget().pack()

aplicacion.mainloop()
