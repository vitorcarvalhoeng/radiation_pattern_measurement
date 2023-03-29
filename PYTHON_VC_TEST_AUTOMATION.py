# ANTENNA TEST AUTOMATION ROUTINE
# 
# Author: Vitor Carvalho de Almeida
# Local: UnB_Gama-LabTelecom --- Autotrac

import numpy as np
import csv
import math
from time import sleep, strftime, localtime

from datetime import datetime

import pandas as pd


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pyqtgraph as pg

# project functions

import infos
from aux_functions import sph2cart, float_range

import SCPI_devices
import serial_devices

print(".........................")
print ("Running Sequence")
print(" ")


#---------------INPUTS--------------------------------
freq_span = 100e3
num_samples, wait_time_phi,wait_time_all,margin_max, margin_step = infos.load_config()

#----------INITIALIZING VARIABLES----------------------------

mag=[]
phi=[]
theta=[]
alpha=[]

freq=[]
time_stamp=[]
date_time=[]

first_measure=True



# atribuindo objetos
SA = SCPI_devices.spectrum_analyser("SA_X")
RF_gen = SCPI_devices.RF_generator("gerador_x")
positioner = serial_devices.positioner("posicionador_X")

RF_gen.RF_off()

#importing sequencing parameters into a general table
sequencing = pd.read_csv('parameters_list.csv')

phi = sequencing.phi
theta = sequencing.theta
alpha = sequencing.alpha
freq = sequencing.freq


#----------FUNCTIONS----------------------------

#--------------commands--------------------------   


# função de medição
# recebe inteiro 'num_samples'
# realiza internamente a média da magnitude linear com o número de amostras
# retorna um float com a magnitude medida no SA, em dBm

def measure(num_samples): # measurement equipment control
    
    # if first_measure:
    #     print("First Measure")
    #     sleep(2)
    #     first_measure=False

    meas=np.ones(num_samples)    

    for i in range(0,num_samples):
        temp_values = SA.peak_search()

        meas[i] = float(temp_values)
        sleep(0.05)

    mag = max(meas)
    return mag


# funcão mover e medir
# sincroniza movimento e medição
# não recebe argumentos, utiliza as variáveis globais, configuradas por outras funções
# não retorna valores, modifica as variáveis globais

def move_and_measure():
    global freq
    global time_stamp, wait_time_all
    global phi, theta, alpha
    global mag


    phi_center, theta_center, alpha_center = infos.load_cal()

    # applying reference offset
    phi_show = [x - phi_center for x in phi]
    theta_show = [x - theta_center for x in theta]
    alpha_show = [x - alpha_center for x in alpha]

    print("Movement...")

    i=0

    RF_gen.RF_on() #turning on RF output

    for i in range(0, len(phi)): # values area appended to the general table
        positioner.set_position(phi[i],theta[i],alpha[i])
        
        print("Waiting "+str(wait_time_all)+" seconds (all)")
        sleep(wait_time_all) #waiting

        RF_gen.set_freq(freq[i])

        print("Frequency set on generator")

        SA.set_freq(freq[i])

        print("Frequency set on analyzer")

        mag.append(measure(num_samples))

        print("Magnitude captured")

        #timestamp
        date_time.append = datetime.now() # Getting the current date and time
        time_stamp.append(datetime.timestamp(date_time)) # getting the timestamp

    RF_gen.RF_off() #turning off RF output


def import_sequencing(filename): #reads the input csv file and stores the parameters on the lists
    global mag, phi, theta, alpha, freq

    input_data = pd.read_csv(filename)
    phi = input_data.phi
    theta = input_data.theta
    alpha = input_data.alpha
    freq = input_data.freq

    #In python if you open a file but forget to close it, 
    # python will close it for you at the end of the function block 
    # (during garbage collection).
    #ref:https://stackoverflow.com/questions/29416968/python-pandas-does-read-csv-keep-file-open

# exporta resultados para arquivo csv
# recebe string com nome do arquivo a ser gerado
# salva um arquivo csv contendo as informações para cada ponto medido:
# phi, theta, alpha, freq, mag, time_stamp
# salva uma cópia idêntica do arquivo com um nome exclusivo:
# 'DIAGRAMA_autosaved_date-%Y-%m-%d_time-%H-%M-%S.csv'
# não retorna valores
# utiliza variáveis globais, mas nao as altera

def export_csv(filename): # file export function
    global mag, phi, theta, alpha, freq
    global date_time, time_stamp

    phi_center, theta_center, alpha_center = infos.load_cal()

    #remaping angles from center calibration

    with open(filename, mode='w', newline='') as diagram:
        wr = csv.writer(diagram, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        wr.writerow(["phi","theta","alpha" ,"freq","mag","date_time","time_stamp"]) # writing csv header
        print("Measured points:")
        print("(phi,theta,alpha,freq,E)")
        for i in range(0,len(mag)): # writing rolls for each direction
            export_data=[phi[i]-phi_center,theta[i]-theta_center,alpha[i]-alpha_center,freq[i],mag[i],date_time[i],time_stamp[i]] #organizing data lines
            print (export_data)
            wr.writerow(export_data)
    diagram.close() #closing file

    #saving a copy file for safety
    copy_filename=strftime("DIAGRAMA_autosaved_date-%Y-%m-%d_time-%H-%M-%S.csv", localtime())
    with open(copy_filename, mode='w', newline='') as diagram:
        wr = csv.writer(diagram, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        wr.writerow(["phi","theta","alpha" ,"freq","mag","date_time","time_stamp"]) # writing csv header
        for i in range(0,len(mag)): # writing rolls for each direction
            export_data=[phi[i]-phi_center,theta[i]-theta_center,alpha[i]-alpha_center,freq[i],mag[i],date_time[i],time_stamp[i]] #organizing data lines
            print (export_data)
            wr.writerow(export_data)
    diagram.close() #closing file


# função 'reset'
# reinicializa as variáveis globais para que possa ser realizada outra medição sem carregar os valores da anterior

def reset():
    global mag,freq,phi,theta,alpha
    global first_measure

    mag=[]
    phi=[]
    theta=[]
    alpha=[]
    freq=[]

    first_measure = True


def update_configs(): # update global configuration variables with information from csv file
    global num_samples, wait_time_phi,wait_time_all,margin_max, margin_step
    num_samples, wait_time_phi,wait_time_all,margin_max, margin_step = infos.load_config()

#-------------------plots-------------------

# função plota diagrama 2D no eixo disponível na UI
# utiliza variáveis globais

def plot_2d(final):
    global phi, theta, alpha, mag
    global axis_options1
    global ui

    #ref: https://matplotlib.org/tutorials/introductory/pyplot.html
    switcher = { # executing axis choice 
        1: [phi, r'$\phi$'],
        2: [theta, r'$\theta$'],
        3: [alpha, r'$\alpha$']
    }
    axis,axis_label= switcher.get(axis_options1, "Invalid axis options")
    
    phi_center, theta_center, alpha_center = infos.load_cal()


    # applying reference offset
    if axis==phi:
        axis_show = [x - phi_center for x in phi]
    elif axis==theta:
        axis_show = [x - theta_center for x in theta]
    elif axis==alpha:
        axis_show = [x - alpha_center for x in alpha]

  
    ui.graphicsView_diagram.plot(axis_show,mag, pen=pg.mkPen('b', width=5)) #x,y
    # plot = ui.graphicsView_diagram
    # for r in range(-90,-30,10):
    #     circle=pg.QtGui.QGraphicsEllipseItem(-r,-r,r*2,r*2)
    #     circle.setPen(pg.mkPen(0.2))
    #     plot.addItem(circle)


    # th = np.deg2rad(phi)
    # radius = mag

    # x=radius*np.cos(th)
    # y=radius*np.sin(th)

    # plot.plot(x,y)

    #plot.refresh_text_box()
    ui.graphicsView_diagram.plot(axis_show,mag, pen=pg.mkPen('b', width=5)) #x,y
    ui.refresh_text_box()



    '''plt.ylabel('E')
    plt.xlabel(str(axis_label))
    plt.ion() # enable interactivity
    plt.show()
    plt.draw()
    plt.pause(0.25)
    if not final: # if it is still running
        plt.clf() #clear previous plot
    else: # if the measurement has finished
        plt.savefig('graph_2D.png') #save fig
        plt.show(block=True) # hold the graph'''
        

# função plota diagrama 3D em janela extra
# utiliza variáveis globais
# recebe bool init e final, correspontes à informação de inicio e fim do procedimento, respectivamente

def plot_3d(init,final):
    global theta, phi, mag
    global fig

    #ref: https://medium.com/@johngrant/antenna-arrays-and-python-plotting-with-pyplot-ae895236396a

    """Plots 3D surface plot over given theta/phi range in 
    Fields by calculating cartesian coordinate equivalent of spherical form."""

    if init==1:
        fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    phiSize = len(phi)   # Finds the phi & theta range
    thetaSize = len(theta)

    X = np.ones((phiSize, thetaSize)) # Prepare arrays to hold the cartesian coordinate data.
    Y = np.ones((phiSize, thetaSize))
    Z = np.ones((phiSize, thetaSize))

    
    for phi_i in range(phiSize): # Iterate over all phi/theta range
        for theta_i in range(thetaSize):
            e = mag[phi_i]

            xe, ye, ze = sph2cart(e, math.radians(theta[theta_i]), math.radians(phi[phi_i]))  # Calculate cartesian coordinates

            X[phi_i, theta_i] = xe  # Store cartesian coordinates
            Y[phi_i, theta_i] = ye
            Z[phi_i, theta_i] = ze

    ax.plot_surface(X, Y, Z, color='b') # Plot surface
    plt.ylabel(r'$\theta$')
    plt.xlabel(r'$\phi$')
    ax.set_zlabel('|E|')
   
    plt.ion() # enable interactivity
    plt.show()
    plt.draw()
    plt.pause(1)
    if not final:
        plt.clf() #clear previous plot
    else:
        plt.savefig('./graph_3D.png') #save fig
        plt.show(block=True) # hold graph
    
        
# função procura máximo
# recebe:
# inteiros: phi0,theta0,alpha0. (pontos de máximo da simulação)
# inteiros: freq. (frequência de medição, em Hz)
# retorna inteiros phi_max e theta_max, correspondentes aos ângulos de máximo ganho encontrados


def search_max(phi0,theta0,alpha0,freq):
    global num_samples, wait_time_phi,wait_time_all,margin_max, margin_step
    
    #setting frequency on instruments
    f_center= float(freq)*1e9
    RF_gen.set_freq(f_center)
    SA.set_freq(f_center)

    RF_gen.RF_on() #turning RF on

    #stablishing limits for search on axis
    phi_min=0
    phi_max=360

    theta_min=0
    apont_equip=infos.load_equip()

    if apont_equip=="PI2":
        theta_max=100
    elif apont_equip == "rotor":
        theta_max=180

    #margins for searching
    range_phi_d=margin_max
    range_phi_u=margin_max

    range_theta_d=margin_max
    range_theta_u=margin_max

    # values correction
    phi0=int(phi0)
    theta0=int(theta0)
    alpha0=int(alpha0)

    if phi0-range_phi_d < phi_min:
        range_phi_d=abs(phi0)
    elif phi0+range_phi_u > phi_max:
        range_phi_u=phi_max-phi0

    if theta0-range_theta_d < theta_min:
        range_theta_d=abs(theta0)
    elif theta0+range_theta_u > theta_max:
        range_theta_u=theta_max-theta0

    #phi sweep   
    #finding the maximum measured magnitude on phi axis around phi0

    mag_test=[]
    phi_test=[]
  
    #for phi in range(phi0-range_phi_d,phi0+range_phi_u,1):
    for phi in float_range(int(phi0-range_phi_d),phi0+range_phi_u,str(margin_step)):
        positioner.set_position(phi, theta0, alpha0)
        sleep(wait_time_all) # settling time
        phi_test.append(phi)
        mag_test.append(measure(num_samples))

    index_max=np.argmax(mag_test)
    phi_max=phi_test[index_max]
    print("phi max = " + str(phi_max))

    #theta sweep
    #finding the maximum measured magnitude on theta axis aroung theta0, on the phi_max position
    mag_test=[]
    theta_test=[]

    #for theta in range(theta0-range_theta_d,theta0+range_theta_u,1):
    for theta in float_range(int(theta0-range_theta_d),theta0+range_theta_u,str(margin_step)):
        positioner.set_position(phi_max, theta, alpha0)
        sleep(wait_time_all) # settling time
        theta_test.append(theta)
        mag_test.append(measure(num_samples))

    index_max=np.argmax(mag_test)
    theta_max=theta_test[index_max]
    print("theta max = " + str(theta_max))

    RF_gen.RF_off() #turning RF off

    return phi_max,theta_max