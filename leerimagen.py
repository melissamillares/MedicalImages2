import pydicom
import numpy as np #is a standard to use this alias for NumPy package
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.font
import matplotlib.image as mpimg
import Gaussian

from tkinter import *
from tkinter import ttk 
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

gaussian_kernel = Gaussian.get_gaussian_filter()
rayleigh_kernel = Gaussian.get_rayleigh_filter()

title = 'medical image processing'
back = tk.Frame(master=aplicacion,bg='#177497')
back.master.title(title)
back.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
back.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window

img = PhotoImage(file='./medical2.png')   
#label title
aplicacion.titulolbl = tk.Label(master=back, text="MEDICAL IMAGE PROCESSING", anchor="center", font=("Ubuntu", 28), bg='#177497')
aplicacion.titulolbl.place(x=80, y=10)
#label
#aplicacion.imagenlbl = tk.Label(master=back, image=img)
#aplicacion.imagenlbl.grid(row=1, column=0, columnspan=2, rowspan=2, padx=10, pady=10, sticky=(N, S, E, W))

#function to choose the image 
def openfile():   
    archivo = tk.filedialog.askopenfile() #askdirectory()    
    dcmfile = archivo.name              
    # Get ref file
    ds = pydicom.dcmread(dcmfile) 
    
    imageProcessing(ds)    
    #histogram(ds)      
    fil = filter_cbb.get()
    if fil == 'Gaussian Filter':
        print("gaussian")
        convolution(ds, gaussian_kernel)         
    else:
        print("Function not found")  

    #convolution(ds, gaussian_kernel)

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
    #imag.imshow(np.flipud(file.pixel_array))             
    imag.imshow(file.pixel_array)
    canvas.draw()       
              
def convolution(file, kernel): 
    kernel = gaussian_kernel[0]
    scalar = gaussian_kernel[1]
    rows = len(kernel)
    columns = len(kernel[0])        
    image = file.pixel_array
    imgAux = image
    summ = 0
    print(kernel)    
    for i in range(file.Rows):
        for j in range(file.Columns):
            if i==0 or j==0:
                imgAux[i,j] = image[i,j]                
                continue
            x = 0
            y = 0
            for k in range(i, rows):
                for l in range(j, columns):
                    print("for ",k,",",l)
                    print("for2 ",x,",",y)
                    summ += (image[k,l]*kernel[x,y])
                    y = y+1
                y = 0
                x = x+1            
            total = summ/scalar                    
            imgAux[i,j] = int(total + 0.5)
    print("imagen")
    '''
    for i in range(file.Rows):
        for j in range(file.Columns):            
            #print(imgAux[i,j], end=" ")
        print()
    '''
    plt.imshow(imgAux)                 
    plt.show()

#button to open the image
aplicacion.abrirbtn = tk.Button(master=back, text="Open image", command=openfile)
aplicacion.abrirbtn.pack(side="top")
aplicacion.abrirbtn.place(x=50, y=70)
#cbb filter
filter_cbb = ttk.Combobox(aplicacion, state="readonly")
filter_cbb.place(x=180, y=70)
filter_cbb["values"] = ['Gaussian Filter', 'Rayleigh Filter']
apply_function = tk.Button(master=back, text="Apply Function") #, command=apply_filter
apply_function.pack(side="top")
apply_function.place(x=200, y=90)
#button histogram
histBtn = tk.Button(master=back, text="Histogram") 
histBtn.pack(side="top")
histBtn.place(x=350, y=70)
#button to close the app
aplicacion.quit = tk.Button(master=back, text="Exit", fg="red", command=aplicacion.destroy)
aplicacion.quit.pack(side="top")
aplicacion.quit.place(x=500, y=70)

canvas.get_tk_widget().pack()

aplicacion.mainloop()
