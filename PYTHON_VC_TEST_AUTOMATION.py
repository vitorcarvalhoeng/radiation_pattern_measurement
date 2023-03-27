# ANTENNA TEST AUTOMATION ROUTINE
# 
# Author: Vitor Carvalho de Almeida
# Local: UnB_Gama-LabTelecom --- Autotrac

import os
import numpy as np
import csv
from functools import partial
import math
from time import strftime, localtime, sleep
import sys

from datetime import datetime

import pandas as pd


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pyqtgraph as pg

# project functions

import infos
from aux_functions import sph2cart, float_range

import threading

import SCPI_devices
import serial_devices




print(".........................")
print ("Running Sequence")
print(" ")


#---------------INPUTS--------------------------------
freq_span = 100e3

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

    phi_center, theta_center, alpha_center = infos.load_cal()

    #remaping angles from center calibration

    with open(filename, mode='w', newline='') as diagram:
        wr = csv.writer(diagram, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        wr.writerow(["phi","theta","alpha" ,"freq","mag","time_stamp"]) # writing csv header
        print("Measured points:")
        print("(phi,theta,alpha,freq,E)")
        for i in range(0,len(mag)): # writing rolls for each direction
            export_data=[phi[i]-phi_center,theta[i]-theta_center,alpha[i]-alpha_center,freq[i],mag[i],time_stamp[i]] #organizing data lines
            print (export_data)
            wr.writerow(export_data)
    diagram.close() #closing file

    #saving a copy file for safety
    copy_filename=strftime("DIAGRAMA_autosaved_date-%Y-%m-%d_time-%H-%M-%S.csv", localtime())
    with open(copy_filename, mode='w', newline='') as diagram:
        wr = csv.writer(diagram, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        wr.writerow(["phi","theta","alpha" ,"freq","mag","time_stamp"]) # writing csv header
        for i in range(0,len(mag)): # writing rolls for each direction
            export_data=[phi[i]-phi_center,theta[i]-theta_center,alpha[i]-alpha_center,freq[i],mag[i],time_stamp[i]] #organizing data lines
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
# inteiros: speed,freq. (velocidade de movimento, frequência de medição, em Hz)
# strings: port, equipment_meas (porta do equipamento apontador e IP do SA)
# retorna inteiros phi_max e theta_max, correspondentes aos ângulos de máximo ganho encontrados


def search_max(phi0,theta0,alpha0,speed,freq,port, equipment_meas):
    
    global equipment
    global margin_max

    num_samples, wait_time_phi,wait_time_all,margin_max, margin_step = infos.load_config()

    equipment=equipment_meas
    config_VISA(freq,equipment)

    phi_min=0
    phi_max=360

    theta_min=0
    apont_equip=infos.load_equip()

    if apont_equip=="PI2":
        theta_max=100
    elif apont_equip == "rotor":
        theta_max=180

    range_phi_d=margin_max
    range_phi_u=margin_max

    range_theta_d=margin_max
    range_theta_u=margin_max

    # limits correction

    phi0=int(phi0)
    theta0=int(theta0)
    alpha0=int(alpha0)
    speed=int(speed)


    if phi0-range_phi_d < phi_min:
        range_phi_d=abs(phi0)
    elif phi0+range_phi_u > phi_max:
        range_phi_u=phi_max-phi0

    if theta0-range_theta_d < theta_min:
        range_theta_d=abs(theta0)
    elif theta0+range_theta_u > theta_max:
        range_theta_u=theta_max-theta0



    #phi sweep   
    mag_test=[]
    phi_test=[]


    #for phi in range(phi0-range_phi_d,phi0+range_phi_u,1):
    for phi in float_range(int(phi0-range_phi_d),phi0+range_phi_u,str(margin_step)):
        move([phi, theta0, alpha0, speed],"send_gcode", port)
        f_center= float(freq)*1e9
        phi_test.append(phi)
        mag_test.append(measure(f_center))


    index_max=np.argmax(mag_test)
    phi_max=phi_test[index_max]

    print(phi_max)


    #theta sweep
    mag_test=[]
    theta_test=[]

    #for theta in range(theta0-range_theta_d,theta0+range_theta_u,1):
    for theta in float_range(int(theta0-range_theta_d),theta0+range_theta_u,str(margin_step)):
        move([phi_max, theta, alpha0, speed],"send_gcode", port)
        f_center= float(freq)*1e9
        theta_test.append(theta)
        mag_test.append(measure(f_center))


    index_max=np.argmax(mag_test)
    theta_max=theta_test[index_max]


    return phi_max,theta_max


#------------------------MAIN-----------------------------

# função principal do código, organiza opções definidas na UI e inicia o processo de medição, chamando as outras funções de comando
#
# recebe:
# inteiros: ax_options1,ax_options2 - opções dos eixos (1=phi, 2=theta, 3=alpha)
# inteiro: ax_mode - modo dos eixos (1, 2 ou 3 eixos)
# vetor: angles - opções de início, fim e passo para cada eixo
# string: freq_mode - opção de varredura na frequência ('single', 'center-span', 'start-stop')
# vetor: freq_opts - valores para frequência (central/start, span/final, passo)
# inteiro: spd - velocidade de movimentação do braço mecânico (somente usada braço 3 eixos)
# string: output_filename - nome do arquivo csv de saída
# classe: ui_obj - objeto da UI
# string: port_dev - porta serial à qual está conectada o equipamento apontador
#
# reotrna vetor de vetores: mag (magnitudes medidas). phi ,theta, alpha (angulos apontados), pointing_angle (ângulos de máximo ganho)

def start_measurement(ax_options1,ax_options2,ax_mode,angles,freq_mode,freq_opts, spd, output_filename,ui_obj, port_dev):
    global start1, stop1, step1
    global start2, stop2, step2

    global phi_start, phi_stop, phi_step
    global theta_start, theta_stop, theta_step
    global alpha_start, alpha_stop, alpha_step
    
    global f_mode, f_opts

    global axis_options1, axis_options2, axis_mode

    global speed
    global ui
    global equipment

    global port

    global num_samples, wait_time_phi,wait_time_all, margin_max

    num_samples, wait_time_phi,wait_time_all,margin_max,margin_step = infos.load_config()

    port = port_dev

    ui = ui_obj

    equipment=ui.lineEdit_ce_filename.text()
    
    ui.listWidget_progress.addItem('Processo iniciado...')
    ui.listWidget_progress.scrollToBottom()
    ui.refresh_text_box()


    #-----getting informations from GUI-------

    axis_options1= ax_options1
    axis_options2=ax_options2
    axis_mode = ax_mode


    f_mode = freq_mode
    f_opts = freq_opts

    speed=spd

    phi_start=angles[0]
    phi_stop=angles[1]
    phi_step=angles[2]

    theta_start=angles[3]
    theta_stop=angles[4]
    theta_step=angles[5]

    alpha_start=angles[6]
    alpha_stop=angles[7]
    alpha_step=angles[8]

    f_center= float(f_opts[0])*1e9
    config_VISA(f_center,equipment)


    #--------running------------------------


    start1, stop1, step1 = limits(axis_options1) #defining limits
    start2, stop2, step2 = limits(axis_options2)

    run_sweep(axis_mode) #move and measure sequence

    #--------exporting data------------------------
    print(output_filename)
    export_csv(output_filename) # exporting results to file


    index_max=np.argmax(mag)

    phi_center, theta_center, alpha_center = infos.load_cal()


    # applying reference offset
    phi_show = [x - phi_center for x in phi]
    theta_show = [x - theta_center for x in theta]
    alpha_show = [x - alpha_center for x in alpha]
    

    #pointing_angle=[eixo_plot[index_max],theta[index_max],alpha[index_max],freq[index_max]]
    pointing_angle=[phi_show[index_max],theta_show[index_max],alpha_show[index_max],freq[index_max]]

    #--------finishing------------------------
    print(" ")
    print ("... FINISHED!")
    ui.listWidget_progress.addItem('.......................')
    ui.listWidget_progress.addItem('Processo Finalizado')
    ui.listWidget_progress.addItem('.......................')
    ui.listWidget_progress.scrollToBottom()
    ui.refresh_text_box()

    
    if axis_mode==2:
        print(" ")
        print ("Close figure window to exit")
        plot_3d(0,1)

    return mag,phi,theta,alpha,pointing_angle

