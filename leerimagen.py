import pydicom
import numpy as np #is a standard to use this alias for NumPy package
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.font
import matplotlib.image as mpimg
import Gaussian
import math

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
fig.set_facecolor('#177497')
canvas = FigureCanvasTkAgg(fig, master=aplicacion)

gaussian_kernel = Gaussian.get_gaussian_filter()[0]
gaussian_scalar = Gaussian.get_gaussian_filter()[1]
rayleigh_kernel = Gaussian.get_rayleigh_filter()[0]
rayleigh_scalar = Gaussian.get_gaussian_filter()[1]
gradient_x_kernel = np.asarray([[-1,0,1],[-2,0,2],[-1,0,1]])
gradient_y_kernel = np.asarray([[1,2,1],[0,0,0],[-1,-2,-1]])

title = 'medical image processing'
back = tk.Frame(master=aplicacion,bg='#177497')
back.master.title(title)
back.pack_propagate(0) # Don't allow the widgets inside to determine the frame's width / height
back.pack(fill=tk.BOTH, expand=1) # Expand the frame to fill the root window

img = PhotoImage(file='./medical2.png')   
# label title
aplicacion.titulolbl = tk.Label(master=back, text="MEDICAL IMAGE PROCESSING", anchor="center", font=("Ubuntu", 28), bg='#177497')
aplicacion.titulolbl.place(x=80, y=10)

# function to choose the image 
def openfile():   
    archivo = tk.filedialog.askopenfile() 
    dcmfile = archivo.name              
    # Get ref file
    d_file = pydicom.dcmread(dcmfile) 
    image = d_file.pixel_array

    imageProcessing(d_file) 
    # original image histogram
    #oih = histogram(image)
    '''
    #button histogram
    histBtn = tk.Button(master=back, text="Histogram", command=oih)
    histBtn.pack(side="top")
    histBtn.place(x=350, y=70)
    '''
    # image with filter
    #apply_filter(image)
    '''
    # button apply_function
    apply_function = tk.Button(master=back, text="Apply Function", command=filtr)
    apply_function.pack(side="top")
    apply_function.place(x=190, y=90)    
    '''
    # image with filter
    filtr = convolution(image, gaussian_kernel, gaussian_scalar) 

    # image histogram with filter 
    h = histogram(filtr)     
    sobel_filter(image, gradient_x_kernel, gradient_y_kernel)  
    #return d_file     

def apply_filter(image):    
    fil = filter_cbb.get()    
    if fil == 'Gaussian Filter':  
        print("Gaussian")      
        return convolution(image, gaussian_kernel, gaussian_scalar)         
    elif fil == 'Rayleigh Filter':
        print("Rayleigh")
        return convolution(image, rayleigh_kernel, rayleigh_scalar)
    else:
        print("Function not found")
        strg = "Function not found"
        return strg  

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
    rows = np.size(file,1)
    columns = np.size(file,0)  
    array = [0]*65536
    
    for i in range(rows):
        for j in range(columns):
            array[file[i,j]]=array[file[i,j]]+1
            
    array = np.asarray(array)
    plt.plot(array)
    fig = plt.gcf()
    fig.canvas.set_window_title('Histogram')           
    plt.show()
    return array

def imageProcessing(file):     
    text_frame.pack()  
    setInfo(file)    
    plt.set_cmap(plt.gray()) 
    imag = fig.add_subplot(121)    
    #imag.imshow(np.flipud(file.pixel_array))             
    imag.imshow(file.pixel_array)
    canvas.draw()       
              
def convolution(image, kernel, scalar):   
    image_rows = np.size(image,1) 
    image_columns = np.size(image,0)          
    imgAux = np.ndarray((image_rows,image_columns), np.int64)
    summ = 0  

    for i in range(0,image_rows):
        for j in range(0,image_columns):
            if i==0 or j==0 or i==image_rows-1 or j==image_columns-1:
                imgAux[i,j] = image[i,j]                
                continue            
            x = 0 #iterator for kernel
            y = 0 #iterator for kernel
            summ = 0
            for k in range(i-1, i+1+1):
                for l in range(j-1, j+1+1):
                    summ += (image[k,l]*kernel[x][y])
                    y = y+1
                y = 0
                x = x+1            
            total = summ/scalar                    
            imgAux[i,j] = np.int64(total + 0.5)
    #plt.set_cmap(plt.gray())
    imag = fig.add_subplot(122)
    imag.imshow(imgAux)
    canvas.draw()

    return imgAux

# otsu thresholding function
def otsu_thresholding(histogram):
    weight_back = 0
    weight_foreg = 0
    mean_back = 0
    mean_foreg = 0
    threshold = 0
    summ = 0
    sum_back = 0
    var_max = 0
    var_between = 0.0
    total = sum(histogram)    
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

# sobel filter for borders
def sobel_filter(image, kernel_x, kernel_y):    
    image_rows = np.size(image,1) 
    image_columns = np.size(image,0)       
    magnitude_matrix = np.ndarray((image_rows,image_columns), np.int64)
    magnitude_matrix = convolution(image, gaussian_kernel, gaussian_scalar)
    gradient_x = kernel_x
    gradient_y = kernel_y
      
    aux_x = convolution(image, gradient_x, 1)
    aux_y = convolution(image, gradient_y, 1)
    magnitude_matrix = abs(aux_x) + abs(aux_y)
             
    imag = fig.add_subplot(122)
    imag.imshow(magnitude_matrix)
    canvas.draw()

    return magnitude_matrix
'''
# k-means function
# @arguments: k number of clusters (k centroids)
def defineCentroid(k):
    contador=0

    centroides= ds.pixel_array.copy()

    cn = []

    for i in range(k):
        cn.append(int(255/k)*i)

    
    while(contador<2):
        arrayCn = []
        
        for n in range(k):
            arrayCn.append([])
        for i in range(rows):
            for j in range(columns):
                distancias=[]
                for n in range(k):
                    distancias.append(fabs(cn[n]-ds.pixel_array[i][j]))

                index=distancias.index(np.amin(distancias))
                arrayCn[index].append(ds.pixel_array[i][j])

                centroides[i][j]=index*int(255/k)
            #print("row: " + str(i)+" columns: "+str(j))

        iguales=True                
        for n in range(k):
            if(cn[n]!=int(np.mean(arrayCn[n]))):
                cn[n]=int(np.mean(arrayCn[n]))
                iguales=False
        
        if(iguales):
            contador+=1

    return centroides

def kmeans():
	copia = ds.pixel_array.copy()

	centroides = numCents.get()
	centroides = int(centroides)

	copia = definirCentroides(centroides)
	
	plt.imshow(copia)
plt.show()
'''

# button to open the image
aplicacion.abrirbtn = tk.Button(master=back, text="Open image", command=openfile)
aplicacion.abrirbtn.pack(side="top")
aplicacion.abrirbtn.place(x=50, y=70)
# cbb filter
filter_cbb = ttk.Combobox(aplicacion, state="readonly")
filter_cbb.place(x=170, y=70)
filter_cbb["values"] = ['Gaussian Filter', 'Rayleigh Filter']
filter_cbb.set('Gaussian Filter')
#button to close the app
aplicacion.quit = tk.Button(master=back, text="Exit", fg="red", command=aplicacion.destroy)
aplicacion.quit.pack(side="top")
aplicacion.quit.place(x=500, y=70)

canvas.get_tk_widget().pack()

aplicacion.mainloop()
