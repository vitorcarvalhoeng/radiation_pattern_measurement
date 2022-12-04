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

# WORKING HOME

import serial
import time

import threading
import csv


def start_serial(port,ui_window):
    global ser
    ui=ui_window

    try:
        # #ser.write(b're01,') #Prefixo b necessary if using Python 3.X
        ser = serial.Serial(port, 115200, timeout=2)
        ui.listWidget_progress.addItem('Conectado!')
        ui.refresh_text_box()
        ui.listWidget_progress.scrollToBottom()
        return True
    except:
        print('Could not connect')
        ui.listWidget_progress.addItem('Erro ao conectar')
        ui.refresh_text_box()
        ui.listWidget_progress.scrollToBottom()
        return False

def disconnect():
        ser.close()


    
    #ser = serial.Serial(port, 115200, timeout=2)

    # arduinoData = serial.Serial(port,115200) #Creates the arduino object and establishes the connection with the port

    # ser.write("M117 Conected")

    # For testx
    # coordinate_in= [13,2,3,4] # Send sequence: coordinate X, Y e Z and speed F
    # input_com = "reset"

#####################################################################################


def Gcode_G1(coordinate):  # Convert coordinete to string Gcode

    # physical limit of axil respectively X,Y and Z
    x,y,z=get_limits()
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


'''def Recived():  # Treatment of inputs recived from Arduino
    global ser
    while (True):
        if("ok" == ser.readline()):
        if True:
            # time.sleep(5)
            print("Recived")
            return "ok"
        else:
            return "Miss: Don't recived Gcode"'''


def Recived():  # Treatment of inputs recived from Arduino
    if (True):
        while True:
            '''rec = ser.readline().decode()
            print(rec)
            if(rec.endswith('ok\n')):
                # time.sleep(5)
                print("Recived")
                return "ok"'''
            return "ok"
    else:
        return "Miss: Don't recived Gcode"

#####################################################################################


def Send_Gcode(send_coord):
    global ser
    print("Sending Gcode")
    #ser.write("M121\n".encode())  # Disable endstop
    print("M121")
    #ser.write(send_coord.encode())
    #ser.write("M400\n".encode())
    print(send_coord)

    return Recived()
#####################################################################################


def Homing_Send():
    global ser
    #ser.write("G28\n".encode())
    print("........")
    print("Sending axis to Homing")
    print("G28")
    print("........")

    return Recived()


def Homing_x():
    global ser
    #ser.write("G28 X\n".encode())
    print("........")
    print("Sending axis to Homing")
    print("G28 X")
    print("........")

    return Recived()


def Homing_y():
    global ser
    #ser.write("G28 Y\n".encode())
    print("........")
    print("Sending axis to Homing")
    print("G28 Y")
    print("........")

    return Recived()


def Homing_z():
    global ser
    #ser.write("G28 Z\n".encode())
    print("........")
    print("Sending axis to Homing")
    print("G28 Z")
    print("........")

    return Recived()
#####################################################################################


def EMERGENCY_PARSER():  # Emergency Stop
    global ser
    #ser.write("M112\n".encode())
    print("M112")
#####################################################################################


def On_Off_Steper(state):  # On or Off Steper Motor
    global ser
    if(state == 1):

        #ser.write("M17\n".encode())
        print("M17")
        print("Enable power on all steper motors ")

        return Recived()
    elif(state == 0):

        #ser.write("M18\n".encode())
        print("M18")
        print("Disable all stepers")

        return Recived()
    else:
        print("Invalid command")
#####################################################################################


def Send_Reset():  # Reset to mast
    global ser
    #ser.write("M999\n".encode())
    print("M999")
#####################################################################################


def Set_Reference():
    global ser
    print("........")
    print("Setting current pointing as reference")

    #ser.write("M206\n".encode())  # Disable endstop
    #ser.write("G92 X0 Y0 Z0\n".encode())
    print("G92 X0 Y0 Z0")
    print("........")


def g_wait():
    #ser.write("M400\n".encode())  # Disable endstop
    Recived()
    Recived()
    #a = ser.readline().decode()
    a="ok"
    print(a)
    print('movement finished')
    return

def get_limits():
        cal_file="limit_config.csv"
        with open(cal_file, mode='r', newline='') as cal_set:  # reading centers info from file
            cal_info = csv.reader(cal_set, delimiter=',',
                                  quotechar='"', quoting=csv.QUOTE_MINIMAL)
            line_count = 0
            for row in cal_info:
                if line_count == 0:
                    print(', '.join(row))
                    line_count += 1
                else:
                    x = int(row[0])
                    y = int(row[1])
                    z = int(row[2])
        cal_set.close()  # closing file

        return x,y,z

#####################################################################################
def move(coordinate_in, input_com, port):
    global ser

    thread = threading.Thread(target=g_wait)

    # start_serial(port)
    # global coordinate_in, input_comv
    if(input_com == "stop"):
        EMERGENCY_PARSER()
    elif(input_com == "reset"):
        Send_Reset()
    elif(input_com == "homing"):
        Homing_Send()
        thread.start()
        thread.join()
    elif(input_com == "homing_x"):
        Homing_x()
    elif(input_com == "homing_y"):
        Homing_y()
    elif(input_com == "homing_z"):
        Homing_z()
    elif(input_com == "on_off_motor"):
        On_Off_Steper(0)
    elif(input_com == "send_gcode"):
        Send_Gcode(Gcode_G1(coordinate_in))
        thread.start()
        thread.join()
    elif(input_com == "set_ref"):
        Set_Reference()
    else:
        print("Invalid command!")




#####################################################################################

# main()
