import pydicom
import numpy as np #is a standard to use this alias for NumPy package
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.font

from tkinter import *
from matplotlib import pyplot as plt

aplicacion = tk.Tk()

#The following line used to display the results of the images in the notebook
#%matplotlib inline 

#variables to save info about the dcm file
var = StringVar() 
varModality = StringVar()
varStudy = StringVar()
varProtocol = StringVar()

#FRAME CONFIGURATION
#aplicacion.geometry("600x500")
title = 'pydicom image'
back = tk.Frame(master=aplicacion,bg='#177497')
back.master.title(title)
back.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
back.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window

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

    # Load spacing values (in mm)
    try:
        SliceThickness = float(RefDs.SliceThickness)
    except AttributeError:
        SliceThickness = 1.0

    ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), SliceThickness)
    #print(RefDs)
    #print(ConstPixelDims)
    #print(ConstPixelSpacing)
    x = np.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
    y = np.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
    z = np.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])

    half = int(np.round(x.shape[0] / 2))
    
    # The array is sized based on 'ConstPixelDims'
    ArrayDicom = np.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

    ds = pydicom.dcmread(dcmfile)
    #print(ds)
    # store the raw image data
    ArrayDicom[:, :, 0] = ds.pixel_array
    print(ds)
    print(ds.pixel_array) 
    print(ds.pixel_array.shape)# ds.pixel_array.shape returns the shape of a NumPy ndarray

    #variables with information about the dcm file
    var.set(ds.pixel_array.shape)  
    modality = ds.data_element("Modality")  
    varModality.set(modality.value)
    study = ds.data_element("StudyDescription")  
    varStudy.set(study.value)
    protocol = ds.data_element("ProtocolName")  
    varProtocol.set(protocol.value)
    #labels for the info
    aplicacion.infolbl = tk.Label(master=back, text="Dimension (pixels):", font=('Ubuntu', 12), bg='#177497')
    aplicacion.infolbl.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    aplicacion.dimensionlbl = tk.Label(master=back, textvariable=var, font=('Ubuntu', 12), bg='#177497')
    aplicacion.dimensionlbl.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=(N, S, E, W))

    aplicacion.infomlbl = tk.Label(master=back, text="Modality:", font=("Ubuntu", 12), bg='#177497')
    aplicacion.infomlbl.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    aplicacion.modalitylbl = tk.Label(master=back, textvariable=varModality, font=("Ubuntu", 12), bg='#177497')
    aplicacion.modalitylbl.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=(N, S, E, W))

    aplicacion.infoslbl = tk.Label(master=back, text="Study description:", font=("Ubuntu", 12), bg='#177497')
    aplicacion.infoslbl.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    aplicacion.studylbl = tk.Label(master=back, textvariable=varStudy, font=("Ubuntu", 12), bg='#177497')
    aplicacion.studylbl.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky=(N, S, E, W))

    aplicacion.infoplbl = tk.Label(master=back, text="Protocol Name:", font=("Ubuntu", 12), bg='#177497')
    aplicacion.infoplbl.grid(row=9, column=0, columnspan=2, padx=10, pady=10)
    aplicacion.protocollbl = tk.Label(master=back, textvariable=varProtocol, font=("Ubuntu", 12), bg='#177497')
    aplicacion.protocollbl.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky=(N, S, E, W))

    img = np.flipud(ArrayDicom[:, :, 0])

    #histogram    
    hist,bins = np.histogram(img,256,[0,256])
    plt.hist(img.ravel(),256,[0,256])
    plt.title('Histogram')
    plt.show()

    #show the image
    plt.figure(dpi=300)
    plt.axes().set_aspect('equal')
    plt.set_cmap(plt.gray())
    '''
    #If you are using MAMMOGRAPHY_PRESENTATION.dcm or MAMMOGRAPHY_RAW.dcm use
    plt.pcolormesh(x, y, np.flipud(ArrayDicom[:, :, 0]).T)
    #else, use the line below
    #plt.pcolormesh(x, y, np.flipud(ArrayDicom[:, :, 0]))
    '''
    plt.imshow(img)
    plt.show()

#label 
img = PhotoImage(file='/home/melissa/Imágenes/medical2.png')
#aplicacion.imagenlbl = tk.Label(master=back, textvariable=var, bg='white', font=("Helvetica", 20))
#aplicacion.imagenlbl.pack(side="top")       

#basics window interface
#label title
aplicacion.titulolbl = tk.Label(master=back, text="MEDICAL IMAGES", anchor="center", font=("Ubuntu", 28), bg='#177497')
aplicacion.titulolbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=(N, S, E, W))
#label for the histogram
aplicacion.imagenlbl = tk.Label(master=back, image=img)
aplicacion.imagenlbl.grid(row=1, column=0, columnspan=2, rowspan=2, padx=10, pady=10, sticky=(N, S, E, W))
#button to open the image
aplicacion.abrirbtn = tk.Button(master=back, text="Open image", command=openfile)
aplicacion.abrirbtn.pack(side="top")
aplicacion.abrirbtn.grid(row=11, column=0, pady=5)
#button to close the app
aplicacion.quit = tk.Button(master=back, text="Exit", fg="red", command=aplicacion.destroy)
aplicacion.quit.pack(side="top")
aplicacion.quit.grid(row=11, column=1, pady=5)

aplicacion.mainloop()
