import pydicom
import numpy as np #is a standard to use this alias for NumPy package
import os
import tkinter as tk
import tkinter.filedialog

from tkinter import *
from matplotlib import pyplot as plt

aplicacion = tk.Tk()

#The following line used to display the results of the images in the notebook
#%matplotlib inline 

PathDicom = "/home/melissa/MIMIA/Imagenes/MRI/" 
lstFilesDCM = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName,filename))
            
#Lets check what we have in the list
print(lstFilesDCM)

# Get ref file
RefDs = pydicom.dcmread(lstFilesDCM[0])

# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))

# Load spacing values (in mm)
try:
    SliceThickness = float(RefDs.SliceThickness)
except AttributeError:
    SliceThickness = 1.0

ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), SliceThickness)

print(RefDs)
print(ConstPixelDims)
print(ConstPixelSpacing)

#Create the array staring from 0, to ConstPixelDims[0]+1 (because stop is an open interval) 
#and the ConstPixelSpacing gives the scale to the volume. 
#If ConstPixelSpacing == 1, then values go to ConstPixelDims[0]+1. It creates a cube.

x = np.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = np.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
z = np.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])

half = int(np.round(x.shape[0] / 2))
print(x[:half]) #print half the values. Starting from index 0 to half-1

# The array is sized based on 'ConstPixelDims'
ArrayDicom = np.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

# loop through all the DICOM files
for filenameDCM in lstFilesDCM:
    # read the file
    ds = pydicom.dcmread(filenameDCM)
    # store the raw image data
    ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array

print(ds.pixel_array) 
print(ds.pixel_array.shape)# ds.pixel_array.shape returns the shape of a NumPy ndarray

'''
plt.figure(dpi=300)
plt.axes().set_aspect('equal')
plt.set_cmap(plt.gray())

#If you are using MAMMOGRAPHY_PRESENTATION.dcm or MAMMOGRAPHY_RAW.dcm use
plt.pcolormesh(x, y, np.flipud(ArrayDicom[:, :, 0]).T)
#else, use the line below
#plt.pcolormesh(x, y, np.flipud(ArrayDicom[:, :, 0]))
'''
plt.imshow(np.flipud(ArrayDicom[:, :, 0]))

'''
Interfaz
''' 
aplicacion.geometry("600x500")

back = tk.Frame(master=aplicacion,bg='gray')
back.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
back.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window

#label 
img = PhotoImage(file='/home/melissa/Imágenes/Captura.png')
var = StringVar() 
#aplicacion.imagenlbl = tk.Label(master=back, textvariable=var, bg='white', font=("Helvetica", 20))
#aplicacion.imagenlbl.pack(side="top")

#funcion para escoger la imagen 
def funcion():   
    archivo = tk.filedialog.askopenfile()  
    print(archivo) 
    var.set("holiii")
    #label de info
    aplicacion.infolbl = tk.Label(master=back, textvariable=var, font=("Helvetica", 14), bg='gray')
    aplicacion.infolbl.grid(row=1, column=2, columnspan=2, rowspan=2, padx=10, pady=10, sticky=(N, S, E, W))
    #aplicacion.imagenlbl = tk.Label(master=back, image=img)
    #aplicacion.imagenlbl.pack()             

#label de titulo
aplicacion.titulolbl = tk.Label(master=back, text="Medical Images", anchor="center", font=("Helvetica", 28), bg='gray')
aplicacion.titulolbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=(N, S, E, W))
#label para poner imagen
aplicacion.imagenlbl = tk.Label(master=back, text="Imagen aqui", font=("Helvetica", 28), bg='white')
aplicacion.imagenlbl.grid(row=1, column=0, columnspan=2, rowspan=2, padx=10, pady=10, sticky=(N, S, E, W))
#boton para abrir la imagen
aplicacion.abrirbtn = tk.Button(master=back, text="Abrir imagen", command=funcion)
aplicacion.abrirbtn.pack(side="top")
aplicacion.abrirbtn.grid(row=3, column=0, pady=5)
#boton para cerrar la app
aplicacion.quit = tk.Button(master=back, text="Salir", fg="red", command=aplicacion.destroy)
aplicacion.quit.pack(side="top")
aplicacion.quit.grid(row=3, column=1, pady=5)

aplicacion.mainloop()
