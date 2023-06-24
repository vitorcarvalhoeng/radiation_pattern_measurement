# Autor: André Fellipe
# LabTelecom


"""
1-Get values at axils and convert to a Gcode string
Input X, Y and Z, speed F

    X -> first axil
    Y -> second axil
    Z -> Polarization
    F -> Speed
User only command G1

2 Serial USB communication to Arduino.
    Send and recive string from Arduino Mega 2560, serial speed 1150200.
    Send Gcode and confimetion to recived
    Send commande of Homing and confimetion to recived

"""


# SERIAL


import serial
import time
import threading
import csv

import configparser

config = configparser.ConfigParser()
config.read('config.ini')
limits_dict = dict(config.items("LIMITS"))


# Inicia a conexão serial com o equipamento apontador
# recebe:
# String com a porta serial selecionada
# Opjeto da UI (para atualização de informações)
def start_serial(port,baud):
    #ui=ui_window      
    try:
        print(port)
        ser = serial.Serial(port, baud, timeout=2)
        print('Connected')
        # ui.listWidget_progress.addItem('Conectado!')
        # ui.refresh_text_box()
        # ui.listWidget_progress.scrollToBottom()
        return ser
    except:
        print('Could not connect')
        # ui.listWidget_progress.addItem('Erro ao conectar')
        # ui.refresh_text_box()
        # ui.listWidget_progress.scrollToBottom()
        return False


# desconecta o equipamento apontador da porta serial
def disconnect(ser):
        ser.close()


#####################################################################################

# Convert coordinate to string Gcode
def Gcode_G1(coordinate): 

    # physical limit of axil respectively X,Y and Z

    x = int(limits_dict["phi_max"])
    y = int(limits_dict["theta_max"])
    z = int(limits_dict["alpha_max"])
    #physical_limit = [360, 100, 360]
    physical_limit = [x, y, z]
    variable_name = ['X', 'Y', 'Z', 'F']
    send_coordinate = "G1"
    for i in range(len(coordinate)):  # Build string to Gcode
        send_coordinate += " " + variable_name[i] + str(coordinate[i])
        if (i < len(coordinate)-1):
            if (0 > coordinate[i] or coordinate[i] > physical_limit[i]):
                return "Error: Corrdinates exceed physical limits"
    return send_coordinate + "\n"
#####################################################################################

# echo:busy: processing



# Treatment of inputs recived from Arduino, returns 'ok'
def Received(ser): 
    if (True):
        # return "ok"
        while True:
            print('Reading serial...')
            rec = ser.readline().decode()
            print('read:'+ rec)
            if(rec.endswith('ok\n')):
                print("Recived")

                return "ok"
    else:
        return "Miss: Didn't recive Gcode"

#####################################################################################

# Envia a string Gcode pel porta serial
# Recebe string Gcode
# Retorna execução da função Received()
def Send_Gcode(ser,send_coord):
    print("Sending Gcode")
    #ser.write("M121\n".encode())  # Disable endstop
    # print("M121")
    ser.write(send_coord.encode())
    print(send_coord)
    time.sleep(1)
    Received(ser)
    time.sleep
    # Received(ser)
    # ser.write("M400\n".encode())
    # print("M400")
    # Received(ser)
    

    

    # return Received(ser)
#####################################################################################

# Envia o comando de procura dos sensores fim de curso (homming) geral
# Retorna execução da função Received()
def Homing_Send(ser):

    ser.write("G28\n".encode())
    print("........")
    print("Sending axis to Homing")
    print("G28")
    print("........")

    return Received(ser)

# Envia o comando de procura dos sensores fim de curso (homming) phi
# Retorna execução da função Received()
def Homing_x(ser):
    ser.write("G28 X\n".encode())
    print("........")
    print("Sending axis to Homing")
    print("G28 X")
    print("........")

    return Received(ser)

# Envia o comando de procura dos sensores fim de curso (homming) theta
# Retorna execução da função Received()
def Homing_y(ser):
    ser.write("G28 Y\n".encode())
    print("........")
    print("Sending axis to Homing")
    print("G28 Y")
    print("........")

    return Received(ser)

# Envia o comando de procura dos sensores fim de curso (homming) alpha
# Retorna execução da função Received()
def Homing_z(ser):
    ser.write("G28 Z\n".encode())
    print("........")
    print("Sending axis to Homing")
    print("G28 Z")
    print("........")

    return Received(ser)
#####################################################################################

# Emergency Stop
def EMERGENCY_PARSER(ser): 
    ser.write("M112\n".encode())
    print("M112")
#####################################################################################

# On or Off Steper Motor
def On_Off_Steper(ser,state):  
    if(state == 1):

        ser.write("M17\n".encode())
        print("M17")
        print("Enable power on all steper motors ")

        return Received(ser)
    elif(state == 0):

        ser.write("M18\n".encode())
        print("M18")
        print("Disable all stepers")

        return Received(ser)
    else:
        print("Invalid command")
#####################################################################################

# Reset to mast
def Send_Reset(ser):  
    ser.write("M999\n".encode())
    print("M999")
#####################################################################################

# Configura posição atual como referência 0,0,0
def Set_Reference(ser):
    print("........")
    print("Setting current pointing as reference")

    ser.write("M206\n".encode())  # Disable endstop
    ser.write("G92 X0 Y0 Z0\n".encode())
    print("G92 X0 Y0 Z0")
    print("........")

# Aguarda fim da movimentação
def g_wait(ser):
    #ser.write("M400\n".encode())  # Disable endstop
    #Received(ser)
    Received(ser)
    #a = ser.readline().decode()
    #print(a)
    print('movement finished')
    return




#####################################################################################
# Trata o comando recebido para executar a respectiva função
# Recebe: 
# vetor de float com as coordenadas phi, theta, alpha
# string com comando
def move(ser,coordinate_in, input_com):

    thread = threading.Thread(target=g_wait)

    # start_serial(port)
    # global coordinate_in, input_comv
    if(input_com == "stop"):
        EMERGENCY_PARSER(ser)
    elif(input_com == "reset"):
        Send_Reset(ser)
    elif(input_com == "homing"):
        Homing_Send(ser)
    elif(input_com == "homing_x"):
        Homing_x(ser)
    elif(input_com == "homing_y"):
        Homing_y(ser)
    elif(input_com == "homing_z"):
        Homing_z(ser)
    elif(input_com == "on_off_motor"):
        On_Off_Steper(ser,0)
    elif(input_com == "send_gcode"):
        Send_Gcode(ser,Gcode_G1(coordinate_in))
        # thread.start()
        # thread.join()
    elif(input_com == "set_ref"):
        Set_Reference(ser)
    else:
        print("Invalid command!")

#####################################################################################
