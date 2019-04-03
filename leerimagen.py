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
from tkinter import messagebox
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
    global image
    image = d_file.pixel_array    

    imageProcessing(d_file)                

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
    
def histogram():    
    rows = np.size(image,1)
    columns = np.size(image,0)  
    array = [0]*65536
    
    for i in range(rows):
        for j in range(columns):
            array[image[i,j]]=array[image[i,j]]+1
            
    array = np.asarray(array)
    plt.plot(array)
    fig = plt.gcf()
    fig.canvas.set_window_title('Histogram')           
    plt.show()
    return array

def imageProcessing(file):     
    text_frame.pack()  
    setInfo(file)    
    # hacer una copia de la imagen y a esa aplicarle el plt.gray
    image_rows = file.Rows
    image_columns = file.Columns          
    imgAux = np.ndarray((image_rows,image_columns), np.int64)
    imgAux = file.pixel_array
    #plt.set_cmap(plt.gray()) 
    imag = fig.add_subplot(121)    
    #imag.imshow(np.flipud(file.pixel_array))             
    imag.imshow(imgAux, cmap=plt.cm.gray)
    canvas.draw()       
              
def convolution(kernel, scalar):   
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
    imag.imshow(imgAux, cmap=plt.cm.gray)
    canvas.draw()
    return imgAux

# median filter
# n: kernel size
def medianFilter(n = 1):		
    size_kern = (2*n)+1
    size_array = size_kern**2
    image_rows = np.size(image,1) 
    image_columns = np.size(image,0)
    img_aux = np.ndarray((image_rows,image_columns), np.int64)
	
    for i in range(image_rows):
	    for j in range(image_columns):
		    if i<n or i>((image_rows-1)-n) or j<n or j>((image_columns-1)-n):
			    img_aux[i,j]=0
		    else:
			    array =[]*size_array

			    for x in range(i-n,i+n+1):
				    for y in range(j-n,j+n+1):
					    array.append(img_aux[x][y])

			    array = sorted(array) # for ordering
			    mid = int((len(array)-1)/2)
			    img_aux[i,j] = array[mid]

    plt.imshow(img_aux, cmap=plt.cm.gray)
    plt.show()

    return img_aux

# function to apply the filters
def apply_filter():    
    fil = filter_cbb.get()    
    if fil == 'Gaussian Filter':               
        messagebox.showinfo(message="Applying Gaussian Filter...\n\nPlease wait", title="Applying Filter")         
        return convolution(gaussian_kernel, gaussian_scalar)         
    elif fil == 'Rayleigh Filter':        
        messagebox.showinfo(message="Applying Rayleigh Filter...\n\nPlease wait", title="Applying Filter")         
        return convolution(rayleigh_kernel, rayleigh_scalar)
    elif fil == 'Sobel Filter':
        messagebox.showinfo(message="Applying Sobel Filter...\n\nPlease wait", title="Applying Filter")         
        return sobel_filter(gradient_x_kernel, gradient_y_kernel)
    else:        
        strg = "Function not found"
        return strg  

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
def sobel_filter(kernel_x, kernel_y):    
    image_rows = np.size(image,1) 
    image_columns = np.size(image,0)       
    magnitude_matrix = np.ndarray((image_rows,image_columns), np.int64)
    magnitude_matrix = convolution(gaussian_kernel, gaussian_scalar)
    gradient_x = kernel_x
    gradient_y = kernel_y
      
    aux_x = convolution(gradient_x, 1)
    aux_y = convolution(gradient_y, 1)
    magnitude_matrix = abs(aux_x) + abs(aux_y)
             
    imag = fig.add_subplot(122)
    imag.imshow(magnitude_matrix, cmap=plt.cm.gray)
    canvas.draw()    

    return magnitude_matrix

# k-means function
# k number of clusters (k centroids)
def define_centroids(k):
    image_rows = np.size(image,1) 
    image_columns = np.size(image,0)
    aux = 0
    centroids = np.ndarray((image_rows,image_columns), np.int64)
    cn = []        
    for i in range(k):
        cn.append(int(255/k)*i)
    
    while(aux < 2):
        arrayCn = []        
        for n in range(k):
            arrayCn.append([])
        for i in range(image_rows):
            for j in range(image_columns):
                distances = []
                for n in range(k):
                    distances.append(math.fabs(cn[n]- image[i][j]))
                index = distances.index(np.amin(distances))
                arrayCn[index].append(image[i][j])
                centroids[i][j] = index*int(255/k)
            #print("row: " + str(i)+" columns: "+str(j))
        equals = True                
        for n in range(k):
            if(cn[n] != int(np.mean(arrayCn[n]))):
                cn[n] = int(np.mean(arrayCn[n]))
                equals = False 

        if(equals):
            aux += 1

    return centroids

def kmeans():
    messagebox.showinfo(message="Calculating K-means", title="K-means")

    img_aux = image
    centroids = centroids_cbb.get()
    print(centroids)
    centroids = int(centroids)
    img_aux = define_centroids(centroids) 
    
    imag = fig.add_subplot(122)    
    imag.imshow(img_aux)
    canvas.draw()    

    return img_aux	

# button to open the image
aplicacion.abrirbtn = tk.Button(master=back, text="Open image", command=openfile)
aplicacion.abrirbtn.pack(side="top")
aplicacion.abrirbtn.place(x=50, y=63)
# cbb filter
filter_cbb = ttk.Combobox(aplicacion, state="readonly")
filter_cbb.place(x=170, y=68)
filter_cbb["values"] = ['Gaussian Filter', 'Rayleigh Filter', 'Sobel Filter']
filter_cbb.set('Gaussian Filter')
# button to apply filter
filter_btn = tk.Button(master=back, text="Apply Filter", command=apply_filter)
filter_btn.pack(side="top")
filter_btn.place(x=350, y=63)
# button histogram
hist_btn = tk.Button(master=back, text="Histogram", command=histogram)
hist_btn.pack(side="top")
hist_btn.place(x=54, y=93)
#button to close the app
aplicacion.quit = tk.Button(master=back, text="Exit", fg="red", command=aplicacion.destroy)
aplicacion.quit.pack(side="top")
aplicacion.quit.place(x=500, y=63)
# cbb number or centroids
centroids_cbb = ttk.Combobox(aplicacion, state="readonly")
centroids_cbb.place(x=170, y=98)
centroids_cbb["values"] = ['2', '3', '4', '5']
centroids_cbb.set('2')
# button to apply k-means
kmeans_btn = tk.Button(master=back, text="Apply K-means", command=kmeans)
kmeans_btn.pack(side="top")
kmeans_btn.place(x=347, y=93)

canvas.get_tk_widget().pack()

aplicacion.mainloop()
