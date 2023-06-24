# ANTENNA TEST AUTOMATION ROUTINE
# 
# Author: Vitor Carvalho de Almeida
# Local: UnB_Gama-LabTelecom --- Autotrac

import numpy as np
import csv
import math
from time import sleep, strftime, localtime
import os
from datetime import datetime
import pandas as pd

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pyqtgraph as pg

import threading
import configparser

# project functions

from aux_functions import sph2cart, float_range
                
import SCPI_devices
import serial_devices


print(".........................")
print ("Running Sequence")
print(" ")


#---------------INPUTS--------------------------------

config = configparser.ConfigParser()
config.read('config.ini')
# num_samples = config.get("MEASUREMENT","num_samples")

cal_dict = dict(config.items("CALIBRATION"))
phi_center = int(cal_dict["phi"])
theta_center = int(cal_dict["theta"])
alpha_center = int(cal_dict["alpha"])
margin_max = float(cal_dict["margin_max"])
margin_step = float(cal_dict["margin_step"])

limits_dict = dict(config.items("LIMITS"))
phi_min = int(limits_dict["phi_min"])
theta_min = int(limits_dict["theta_min"])
alpha_min = int(limits_dict["alpha_min"])
phi_max = int(limits_dict["phi_max"])
theta_max = int(limits_dict["theta_max"])
alpha_max = int(limits_dict["alpha_max"])

meas_dict = dict(config.items("MEASUREMENT"))
num_samples = int(meas_dict["num_samples"])
wait_time = float(meas_dict["wait_time"])
freq_span = int(meas_dict["freq_span"])

plot_dict = dict(config.items("PLOT"))
plot_enable = bool(config.getboolean('PLOT','plot_enable'))
plot_2d_var = str(plot_dict["var_2d"])

#----------INITIALIZING VARIABLES----------------------------

mag=[]
phi=[]
theta=[]
alpha=[]

freq=[]
time_stamp=[]
date_time=[]

first_measure=True
first_plot = True

#----------FUNCTIONS----------------------------


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
    global time_stamp, date_time, wait_time
    global phi, theta, alpha
    global mag

    global phi_center, theta_center, alpha_center

    # applying reference offset
    phi_show = [x - phi_center for x in phi]
    theta_show = [x - theta_center for x in theta]
    alpha_show = [x - alpha_center for x in alpha]

    print("Movement...")

    i=0

    RF_gen.RF_on() #turning on RF output

    for i in range(0, len(phi)): # values area appended to the general table
        positioner.set_position(phi[i],theta[i],alpha[i])
        
        print("Waiting "+str(wait_time)+" seconds (all)")
        sleep(wait_time) #waiting

        RF_gen.set_freq(int(freq[i]))

        print("Frequency set on generator")

        SA.set_freq(int(freq[i]))

        print("Frequency set on analyzer")

        mag.append(measure(num_samples))

        print("Magnitude captured")

        #timestamp
        date_time.append(datetime.now()) # Getting the current date and time
        time_stamp.append(datetime.timestamp(date_time[i])) # getting the timestamp

        export_csv('a',True)
        if plot_enable:
            plot_2d()
        

    RF_gen.RF_off() #turning off RF output
    


def import_sequencing(filename): #reads the input csv file and stores the parameters on the lists
    input_data = pd.read_csv(filename)
    phi = input_data.phi
    theta = input_data.theta
    alpha = input_data.alpha
    freq = input_data.freq

    return phi, theta, alpha, freq

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

def export_csv(filename, safe_copy): # file export function
    global mag, phi, theta, alpha, freq
    global date_time, time_stamp

    global phi_center, theta_center, alpha_center

    #remaping angles from center calibration

    if (safe_copy == False):
        with open(filename, mode='w', newline='') as diagram:
            wr = csv.writer(diagram, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wr.writerow(["phi","theta","alpha" ,"freq","mag","date_time","time_stamp"]) # writing csv header
            for i in range(0,len(mag)): # writing rolls for each direction
                export_data=[phi[i]-phi_center,theta[i]-theta_center,alpha[i]-alpha_center,freq[i],mag[i],date_time[i],time_stamp[i]] #organizing data lines
                wr.writerow(export_data)
        diagram.close() #closing file

    elif (safe_copy == True):
        #saving a copy file for safety
        if not os.path.exists('./autosaved'):
            os.makedirs('./autosaved')
        copy_filename=strftime("./autosaved/autosaved_date-%Y-%m-%d_time-%H-%M-%S.csv", localtime())
        with open(copy_filename, mode='w', newline='') as diagram:
            wr = csv.writer(diagram, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wr.writerow(["phi","theta","alpha" ,"freq","mag","date_time","time_stamp"]) # writing csv header
            for i in range(0,len(mag)): # writing rolls for each direction
                export_data=[phi[i]-phi_center,theta[i]-theta_center,alpha[i]-alpha_center,freq[i],mag[i],date_time[i],time_stamp[i]] #organizing data lines
                wr.writerow(export_data)
        diagram.close() #closing file
    else:
        print('Invalid Option')
        return -1


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

#-------------------plots-------------------

# função plota diagrama 2D no eixo disponível na UI
# utiliza variáveis globais

def plot_2d():
    global phi, theta, alpha, mag
    global first_plot

 
    print('plotando...')
    
    # clear axis
    ax.clear()
    if plot_2d_var == "phi":
        ax.plot(phi[0:len(mag)],mag)
    elif plot_2d_var == "theta":
        ax.plot(theta[0:len(mag)],mag)
    elif plot_2d_var == "alpha":
        ax.plot(alpha[0:len(mag)],mag)
    else:
        print("Variável de plotagem invalida")


    plt.show()
    plt.pause(0.0001)

        

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
    global num_samples, wait_time,margin_max, margin_step,phi_max, phi_min, theta_max, theta_min, alpha_max, alpha_min
    
    #setting frequency on instruments
    f_center= float(freq)
    RF_gen.set_freq(f_center)
    SA.set_freq(f_center)

    RF_gen.RF_on() #turning RF on

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
    theta_test=[]
  
    #for phi in range(phi0-range_phi_d,phi0+range_phi_u,1):
    for phi in float_range(int(phi0-range_phi_d),phi0+range_phi_u,str(margin_step)):
        for theta in float_range(int(theta0-range_theta_d),theta0+range_theta_u,str(margin_step)):
            positioner.set_position(phi, theta, alpha0)
            sleep(wait_time) # settling time
            phi_test.append(phi)
            theta_test.append(theta)
            mag_test.append(measure(num_samples))


    index_max=np.argmax(mag_test)
    phi_max=phi_test[index_max]
    theta_max=theta_test[index_max]
    print("phi max = " + str(phi_max))
    print("theta max = " + str(theta_max))

   
    RF_gen.RF_off() #turning RF off

    return phi_max,theta_max



###########  MAIN ##########

# atribuindo objetos
SA = SCPI_devices.spectrum_analyser("SA_X")
RF_gen = SCPI_devices.RF_generator("gerador_x")
positioner = serial_devices.positioner("posicionador_X")

SA.connect("sim",9)
RF_gen.connect("sim",8)
positioner.connect("serial_mock",0,0)

RF_gen.RF_off()

filename = 'parameters_list.csv'
phi, theta, alpha, freq = import_sequencing(filename)

if plot_enable:
    # define and adjust figure
    plt.ion()
    fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
    ax = plt.subplot(121)
    ax.set_facecolor('#DEDEDE')


move_and_measure()

if not os.path.exists('./results'):
    os.makedirs('./results')

output_filename = 'output.csv'

export_csv('./results/' + output_filename, False)

SA.disconnect_equip()
RF_gen.disconnect_equip()
positioner.disconnect_equip()