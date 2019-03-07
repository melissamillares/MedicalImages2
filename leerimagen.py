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
gradient_x_kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
gradient_x_kernel = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])

title = 'medical image processing'
back = tk.Frame(master=aplicacion,bg='#177497')
back.master.title(title)
back.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
back.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window

img = PhotoImage(file='./medical2.png')   
#label title
aplicacion.titulolbl = tk.Label(master=back, text="MEDICAL IMAGE PROCESSING", anchor="center", font=("Ubuntu", 28), bg='#177497')
aplicacion.titulolbl.place(x=80, y=10)

#function to choose the image 
def openfile():   
    archivo = tk.filedialog.askopenfile() #askdirectory()    
    dcmfile = archivo.name              
    # Get ref file
    d_file = pydicom.dcmread(dcmfile) 
    #t = type(d_file)
    #print(t)
    imageProcessing(d_file) 
    #convolution(d_file, gaussian_kernel)    
    otsu_thresholding(histogram(d_file))
    return d_file     
'''
def apply_filter():
    file = openfile() #se abre el dir de nuevo :'v
    fil = filter_cbb.get()    
    if fil == 'Gaussian Filter':        
        convolution(file, gaussian_kernel)         
    elif fil == 'Rayleigh Filter':
        print("Rayleigh")
        convolution(ds, rayleigh_kernel)
    else:
        print("Function not found")  
'''
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
    image_rows = file.Rows 
    image_columns = file.Columns      
    image = file.pixel_array
    imgAux = np.ndarray((image_rows,image_columns), np.int64)
    summ = 0   
    for i in range(0,image_rows):
        for j in range(0,image_columns):
            if i==0 or j==0 or i==image_rows-1 or j==image_columns-1:
                imgAux[i,j] = image[i,j]                
                continue            
            x = 0
            y = 0
            summ = 0
            for k in range(i-1, i+1+1):
                for l in range(j-1, j+1+1):
                    summ += (image[k,l]*kernel[x,y])
                    y = y+1
                y = 0
                x = x+1            
            total = summ/scalar                    
            imgAux[i,j] = np.int64(total + 0.5)
    plt.imshow(imgAux)                 
    plt.show()

def otsu_thresholding(histogram):
    weight_back = 0
    weight_foreg = 0
    mean_back = 0
    mean_foreg = 0
    threshold = 0
    summ = 0
    sum_back = 0
    var_max = 0
    var_between = 0
    total = sum(histogram)
    print(total)
    for t in histogram:
        summ += t * histogram[t]
    
    for t in histogram:
        weight_back += histogram[t]
        if weight_back == 0:
            continue        
        weight_foreg = total - weight_back
        if weight_foreg == 0:
            break
        sum_back += t*histogram[t]
        mean_back = sum_back/weight_back
        mean_foreg = (summ - sum_back)/weight_foreg
        var_between = weight_back * weight_foreg * (mean_back - mean_foreg) * (mean_back - mean_foreg)    
        if var_between > var_max:
            var_max = var_between
            threshold = t
    return threshold

def sobel_filter(file, kernel_x, kernel_y):
    convolution(file, rayleigh_kernel)
    image_rows = file.Rows 
    image_columns = file.Columns 
    image = file.pixel_array
    magnitude_matrix = np.ndarray((image_rows,image_columns), np.int64)
'''
    for i in range():
        for j in range():
            if i==0 or j==0 or i==imagse_rows-1 or j==image_columns-1:
                magnitude_matrix[i,j] = 0                
                continue
'''

def magnitude_gradient():
    print("gradiente")

#button to open the image
aplicacion.abrirbtn = tk.Button(master=back, text="Open image", command=openfile)
aplicacion.abrirbtn.pack(side="top")
aplicacion.abrirbtn.place(x=50, y=70)
#cbb filter
filter_cbb = ttk.Combobox(aplicacion, state="readonly")
filter_cbb.place(x=170, y=70)
filter_cbb["values"] = ['Gaussian Filter', 'Rayleigh Filter']
filter_cbb.set('Gaussian Filter')
apply_function = tk.Button(master=back, text="Apply Function")#, command=apply_filter)
apply_function.pack(side="top")
apply_function.place(x=190, y=90)
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
