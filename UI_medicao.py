# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'D:\Onedrive\AUTOTRAC\TEST_AUTOMATION\medicao.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
#
#
#
# REF: https://www.youtube.com/watch?v=ksW59gYEl6Q

# QT_DEBUG_PLUGINS=1
# QT_QPA_PLATFORM=wayland


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

# from UI_calwindow import calwindow

import pyqtgraph as pg

from PYTHON_VC_TEST_AUTOMATION import start_measurement, reset
from pointing_system import move, Send_Reset, start_serial, disconnect
import infos

from UI_cal import Ui_calWindow
from UI_meas_config import Ui_Config

import csv

from scan_ports import serial_ports
import threading

global freq_mode
global connected

connected=False


class Ui_MainWindow(object):

    # --------------------secondary windows--------------------

    
    #abre a janela de calibração

    def openCalWindow(self):
        phi_center, theta_center, alpha_center = infos.load_cal() #getting centers information
        centers=[phi_center, theta_center, alpha_center]
        freq=self.lineEdit_freq_center.text()
        port = self.comboBox_port.currentText()

        speed_meas=self.lineEdit_speed.text()
        meas_equip=self.lineEdit_ce_filename.text()

        print("cal window")

        self.window = QtWidgets.QMainWindow()
        Cal = QtWidgets.QDialog()
        self.ui = Ui_calWindow()
        self.ui.setupUi(Cal,port,freq,centers, meas_equip, speed_meas)
        Cal.setWindowTitle('Calibração')
        Cal.show()
        Cal.exec()

    # abre a janela de configurações

    def config_meas(self):
        print("Config Meas")
        Config = QtWidgets.QDialog()
        self.conf_m = Ui_Config()
        self.conf_m.setupUi(Config)
        Config.setWindowTitle('Configurações de medição')
        Config.show()
        Config.exec()


# -------------------------FUNCTIONS---------------------------------------
    # --------------------Routine commands----------------------------------

    # inicia o processo de Medição
    # antes de iniciar, salva no arquivo csv 'last_ip.csv' a informação do IP do SA utilizado

    def start_process(self):
        cal_file="last_ip.csv"
        with open(cal_file, mode='w', newline='') as cal_set: #saving centers info in file
            wr = csv.writer(cal_set, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wr.writerow(["ip"])
            wr.writerow([str(self.lineEdit_ce_filename.text())])
        cal_set.close() #closing file

        self.start_routine()
        
    # inicia o processo de Medição 
    # função separada em duas porque assim é possível realizar operações prévias à medição mais organizadamente
    # utiliza variáveis globais
    
    def start_routine(self):
        global freq_mode
        global port

        port = self.comboBox_port.currentText()

        if self.check():
            print('Error')
            return

        self.listWidget_progress.scrollToBottom()
        axis_mode, angles, axis_options1, axis_options2 = self.get_sweep_options(
            self)
        if freq_mode == "single":
            freq_opts = [float(self.lineEdit_freq_center.text()), 0, 0]
        else:
            freq_opts = [float(self.lineEdit_freq_center.text()),
                float(self.lineEdit_freq_span.text()),
                float(self.lineEdit_freq_step.text())]
        speed = int(self.lineEdit_speed.text())
        output_filename = self.lineEdit_output_filename.text()

        '''print("Searching reference")
        self.listWidget_progress.addItem('Procurando referências')
        self.listWidget_progress.scrollToBottom()
        move([0,0,0,0], 'homing', port) # search references'''
        
        print("OK. Ready")
        self.listWidget_progress.addItem('Referências encotradas')
        self.listWidget_progress.addItem('Iniciando medição')
        self.listWidget_progress.scrollToBottom()
        

        mag, phi, theta, alpha, pointing_angle = start_measurement(
            axis_options1, axis_options2, axis_mode, angles, freq_mode, freq_opts, speed, output_filename,
            self, port)
        self.textBrowser_pointing_angle_phi.setText(str(pointing_angle[0]))
        self.textBrowser_pointing_angle_theta.setText(str(pointing_angle[1]))
        self.textBrowser_pointing_angle_alpha.setText(str(pointing_angle[2]))
        self.textBrowser_freq_max_gain.setText(str(pointing_angle[3]/1e9))

    
    # comandos de reset dos valores

    def reset_routine(self):
        self.textBrowser_pointing_angle_phi.setText(' ')
        self.textBrowser_pointing_angle_theta.setText(' ')
        self.textBrowser_pointing_angle_alpha.setText(' ')

        reset()

        self.progressBar_total.setValue(0)
        self.progressBar_partial.setValue(0)
        self.listWidget_progress.addItem('.......................')
        self.listWidget_progress.addItem('Aguardando início')
        self.listWidget_progress.scrollToBottom()
        print('.........................')
    
    # comando para limpar o gráfico

    def reset_plot_routine(self):
        self.graphicsView_diagram.clear() #clear figure

    # comando para resetar o braço de 3 eixos

    def reset_pointing_system(self):
        print("...Reseting pointing system...")
        Send_Reset()

    #OBS: as funções com poucas linhas acima foram definidas por que é necessário associar o click dos botões a uma função,
    # que executa os comandos desejados
    
    # --------------------Get information----------------------------------


    # catpa e organiza nas variáveis as informações de sweep configuradas na UI
    # argumento 'a' foi adicionado para livrar bug, não é utilizado
    # retorna um vetor de inteiros: axis_mode, angles, axis_options1, axis_options2,
    # correspondentes a, respectivamente: 
    #   quantos eixos serão varridos, as informações de inicio, fim e passo de cada eixo, opção do eixo 1, opção do eixo 2 
    #   (opções ignoradas caso tenham sidos selecionados todos os eixos)

    def get_sweep_options(self, a):
        axis_mode = 0
        if self.checkBox_phi.isChecked():
            axis_mode += 1

        if self.checkBox_theta.isChecked():
            axis_mode += 2

        if self.checkBox_alpha.isChecked():
            axis_mode += 4

        axis_options1 = 1
        axis_options2 = 2

        if axis_mode == 1:  # 1 axis
            axis_options1 = 1
        elif axis_mode == 2:
            axis_mode = 1
            axis_options1 = 2
        elif axis_mode == 4:
            axis_mode = 1
            axis_options1 = 3
        elif axis_mode == 3:  # 2 axis
            axis_mode = 2
            axis_options1 = 1
            axis_options2 = 2
        elif axis_mode == 5:  # 2 axis
            axis_mode = 2
            axis_options1 = 1
            axis_options2 = 3
        elif axis_mode == 6:
            axis_mode = 2
            axis_options1 = 2
            axis_options2 = 3
        elif axis_mode == 7:  # 3 axis
            axis_mode = 3
            axis_options1 = 1
            axis_options2 = 2

        phi_start = float(self.lineEdit_phistart.text())
        phi_stop = float(self.lineEdit_phistop.text())
        phi_step = float(self.lineEdit_phistep.text())

        theta_start = float(self.lineEdit_thetastart.text())
        theta_stop = float(self.lineEdit_thetastop.text())
        theta_step = float(self.lineEdit_thetastep.text())

        alpha_start = float(self.lineEdit_alphastart.text())
        alpha_stop = float(self.lineEdit_alphastop.text())
        alpha_step = float(self.lineEdit_alphastep.text())
        # remaping angles from center calibration

        phi_center, theta_center, alpha_center = infos.load_cal()

        phi_start = phi_start+phi_center
        theta_start = theta_start+theta_center
        alpha_start = alpha_start+alpha_center

        phi_stop = phi_stop+phi_center
        theta_stop = theta_stop+theta_center
        alpha_stop = alpha_stop+alpha_center

        # ..........

        angles = [phi_start, phi_stop, phi_step, theta_start,
                  theta_stop, theta_step, alpha_start, alpha_stop, alpha_step]

        return axis_mode, angles, axis_options1, axis_options2



    # Atualiza a lista de portas seriais disponiveis

    def port_update(self):
        self.pushButton_refresh_ports.setText('Aguarde')
        ports = serial_ports()
        self.comboBox_port.clear()
        for i in range(0,len(ports)):
            self.comboBox_port.addItem(ports[i])
        self.pushButton_refresh_ports.setText('Atualizar')



    # --------------------Move----------------------------------

    # Move o equipamento apontador para a posição inserida nos campos 'start' de cada eixo
    # Apontamento é corrigido pela calibração

    def move_start(self):
        global port

        port = self.comboBox_port.currentText()

        phi_center, theta_center, alpha_center = infos.load_cal()

        phi_start = int(self.lineEdit_phistart.text())
        theta_start = int(self.lineEdit_thetastart.text())
        alpha_start = int(self.lineEdit_alphastart.text())
        speed = int(self.lineEdit_speed.text())

        phi_start = phi_start+phi_center
        theta_start = theta_start+theta_center
        alpha_start = alpha_start+alpha_center

        move([phi_start, theta_start, alpha_start, speed], "send_gcode",port)

    # Move o equipamento apontador para a posição 0,0,0
    # Apontamento é corrigido pela calibração

    def move_0(self):
        global port
        port = self.comboBox_port.currentText()

        phi_center, theta_center, alpha_center = infos.load_cal()
        speed = int(self.lineEdit_speed.text())

        move([phi_center, theta_center, alpha_center, speed], "send_gcode", port)

    # --------------------File dialog----------------------------------

    # Abre a janela de diálogo para selecionar o caminho e arquivo de saída

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(
            None, "Output file", "", "CSV files (*.csv)", options=options)
        self.lineEdit_output_filename.setText(filename)

    # Abre a janela de diálogo para selecionar o caminho e arquivo da sequência Command Expert controladora do SA

    def chooseCEfile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            None, "Keisight CE file", "", "Keysight CE files (*.iseqx)", options=options)
        self.lineEdit_ce_filename.setText(filename)   



    # --------------------Verification----------------------------------

    # Exibe mensagem de erro e bloqueia ação de inicio do processo de medição

    def error(self,msg):
        self.pushButton_start.setEnabled(False)
        self.label_error_defina_arquivo.setText(msg)
        self.label_error_defina_arquivo.setVisible(True)

        pixmap = QtGui.QPixmap('x_mark.png')
        pixmap = pixmap.scaled(self.mark_image.width(
        ), self.mark_image.height(), QtCore.Qt.KeepAspectRatio)
        self.mark_image.setPixmap(pixmap)

    # Verifica se as configurações estão de acordo com o esperado para o pleno funcionamento da aplicação
    # Retorna True para erro, e False caso tudo esteja correto

    def check(self):


        if not(len(self.lineEdit_ce_filename.text()) > 0):
            self.error("Defina o equipamento de medição")
            return True

        if not(len(self.lineEdit_output_filename.text()) > 0):
            self.error("Defina o arquivo de saída")
            return True

        if not (self.checkBox_phi.isChecked() or self.checkBox_theta.isChecked() or self.checkBox_alpha.isChecked()):
            self.error("Defina a varredura angular")
            return True

        if (self.checkBox_phi.isChecked() and float(self.lineEdit_phistep.text())==0 or 
            self.checkBox_theta.isChecked() and float(self.lineEdit_thetastep.text())==0 or
            self.checkBox_alpha.isChecked() and float(self.lineEdit_alphastep.text())==0):
            self.error("Defina um passo diferente de 0")
            return True

        if not(self.radioButton_singlefreq.isChecked() or (not self.radioButton_singlefreq.isChecked() and len(self.lineEdit_freq_span.text())>0 and len(self.lineEdit_freq_step.text())>0)):
            self.error("Defina a varredura de frequência")
            return True

        if not connected:
            self.error("Conecte-se ao braço mecânico")
            return True


        cal_file = "calibration_status.csv"
        with open(cal_file, mode='r', newline='') as cal_set:  # reading centers info from file
            cal_info = csv.reader(cal_set, delimiter=',',
                                  quotechar='"', quoting=csv.QUOTE_MINIMAL)
            line_count = 0
            for row in cal_info:
                if line_count == 0:
                    print(', '.join(row))
                    line_count += 1
                else:
                    calibrated = bool(int(row[0]))
                    print(calibrated)
        cal_set.close()  # closing file



        if (not calibrated) and (self.radioButton_equip_PI2.isChecked()):
            self.error("Calibre o braço")
            return True


        self.pushButton_start.setEnabled(True)
        self.label_error_defina_arquivo.setVisible(False)

        pixmap = QtGui.QPixmap('ok_mark.png')
        pixmap = pixmap.scaled(self.mark_image.width(
        ), self.mark_image.height(), QtCore.Qt.KeepAspectRatio)
        self.mark_image.setPixmap(pixmap)
                

        return False

    # Realiza a conexão serial com o equipamento apontador

    def test_port(self):
        global connected
        port = self.comboBox_port.currentText()            

        if connected:
            disconnect()
            print('Disconnected')
            self.commandLinkButton_cal.setEnabled(False)
            self.pushButton_test_port.setText('Conectar')
            self.listWidget_progress.addItem('Desconectado')
            self.listWidget_progress.scrollToBottom()
            connected=False
        else:
            connected=start_serial(port,self)
            if connected:
                self.commandLinkButton_cal.setEnabled(True)
                print('Connected')
                self.pushButton_test_port.setText('Desconectar')




    # --------------------Updates----------------------------------

    # Atualiza os elementos dinâmicos da UI. Utilizado pelo código PYTHON_VC_TEST_AUTOMATION.py para atualizar
    # log, plot e barra de progresso enquanto as operações são realizadas
    
    def refresh_text_box(self):
        QtGui.QApplication.processEvents()  # update gui for pyqt


    # atualiza a caixa de texto dos 'pontos' de frequência, baseado no cálculo entre os limites e o passo
    def update_points(self):
        global freq_mode

        if self.lineEdit_freq_step.text() != "0" and len(self.lineEdit_freq_step.text()) > 0:

            if freq_mode == 'start-stop':
                pts=float(self.lineEdit_freq_span.text())-float(self.lineEdit_freq_center.text())
                pts=pts/float(self.lineEdit_freq_step.text())+1
                self.lineEdit_freq_points.setText(str(int(pts)))
            elif freq_mode=='center-span':
                pts=float(self.lineEdit_freq_span.text())
                pts=pts/float(self.lineEdit_freq_step.text())+1
                self.lineEdit_freq_points.setText(str(int(pts)))
    

    # atualiza a caixa de texto do 'passo' de frequência, baseado no cálculo entre os limites e o numero de pontos
    def update_step(self):
        global freq_mode
        if self.lineEdit_freq_points.text() != "0" and len(self.lineEdit_freq_points.text()) > 0:
            
            if freq_mode == 'start-stop':
                step=float(self.lineEdit_freq_span.text())-float(self.lineEdit_freq_center.text())
                step=step/(float(self.lineEdit_freq_points.text())-1)
                self.lineEdit_freq_step.setText(str(step))
                
            elif freq_mode=='center-span':
                step=float(self.lineEdit_freq_span.text())
                step=step/(float(self.lineEdit_freq_points.text())-1)
                self.lineEdit_freq_step.setText(str(step))

    # Configura o modo de frequência para 'single point' e atualiza o estado dos elementos da UI
    def single_freq(self):
        global freq_mode
        self.lineEdit_freq_span.setEnabled(False)
        self.lineEdit_freq_step.setEnabled(False)
        self.lineEdit_freq_points.setEnabled(False)
        freq_mode='single'

    # Configura o modo de frequência para 'center-span' e atualiza o estado dos elementos da UI
    def sweep_freq_cs(self):
        global freq_mode
        self.lineEdit_freq_span.setEnabled(True)
        self.lineEdit_freq_step.setEnabled(True)
        self.lineEdit_freq_points.setEnabled(True)

        self.label_6.setText("Frequência central")
        self.label_27.setText("Largura de banda")
        freq_mode='center-span'
 
    # Configura o modo de frequência para 'start-stop' e atualiza o estado dos elementos da UI
    def sweep_freq_ss(self):
        global freq_mode
        self.lineEdit_freq_span.setEnabled(True)
        self.lineEdit_freq_step.setEnabled(True)
        self.lineEdit_freq_points.setEnabled(True)

        self.label_6.setText("Frequência inicial")
        self.label_27.setText("Frequência final")
        freq_mode='start-stop'

    # Configura o equipamento apontador para o braço de 3 eixos  e atualiza o estado dos elementos da UI
    def config_PI2(self):
        print("Selected: PI2")
        cal_file="equip_config.csv"
        with open(cal_file, mode='w', newline='') as cal_set: #saving centers info in file
            wr = csv.writer(cal_set, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wr.writerow(["equip_num"])
            wr.writerow(['PI2'])
        cal_set.close() #closing file

        cal_file="limit_config.csv"
        with open(cal_file, mode='w', newline='') as cal_set: #saving centers info in file
            wr = csv.writer(cal_set, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wr.writerow(["x","y","z"])
            wr.writerow([360, 100, 360])
        cal_set.close() #closing file

        self.checkBox_alpha.setEnabled(True)
        self.lineEdit_alphastart.setEnabled(True)
        self.lineEdit_alphastop.setEnabled(True)
        self.lineEdit_alphastep.setEnabled(True)

        cal_file="calibration_status.csv"
        with open(cal_file, mode='w', newline='') as cal_set: #saving centers info in file
            wr = csv.writer(cal_set, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wr.writerow(["calibrated"])
            wr.writerow('0')
        cal_set.close() #closing file

    # Configura o equipamento apontador para o rotor de 2 eixos  e atualiza o estado dos elementos da UI
    def config_rotor(self):
        print("Selected: Rotor")
        cal_file="equip_config.csv"
        with open(cal_file, mode='w', newline='') as cal_set: #saving centers info in file
            wr = csv.writer(cal_set, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wr.writerow(["equip_num"])
            wr.writerow(['rotor'])
        cal_set.close() #closing file

        cal_file="calibration_status.csv"
        with open(cal_file, mode='w', newline='') as cal_set: #saving centers info in file
            wr = csv.writer(cal_set, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wr.writerow(["calibrated"])
            wr.writerow('1')
        cal_set.close() #closing file

        cal_file="limit_config.csv"
        with open(cal_file, mode='w', newline='') as cal_set: #saving centers info in file
            wr = csv.writer(cal_set, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wr.writerow(["x","y","z"])
            wr.writerow([360, 180, 360])
        cal_set.close() #closing file

        self.checkBox_alpha.setEnabled(False)
        self.lineEdit_alphastart.setEnabled(False)
        self.lineEdit_alphastop.setEnabled(False)
        self.lineEdit_alphastep.setEnabled(False)


# --------------------WINDOW SETUP--------------------

    # definições da UI
    def setupUi(self, MainWindow):

        self.graphicsView_diagram = pg.PlotWidget(MainWindow)
        self.graphicsView_diagram.setGeometry(QtCore.QRect(620, 425, 291, 221))
        self.graphicsView_diagram.setObjectName("graphicsView_diagram")



        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(972, 681)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(460, 70, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(370, 420, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(0, 30, 961, 20))
        self.line_4.setLineWidth(3)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.pushButton_reset = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reset.setGeometry(QtCore.QRect(360, 590, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_reset.setFont(font)
        self.pushButton_reset.setObjectName("pushButton_reset")


        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(420, 189, 131, 20))
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(410, 40, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_move_to_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_move_to_start.setGeometry(QtCore.QRect(770, 170, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_move_to_start.setFont(font)
        self.pushButton_move_to_start.setObjectName("pushButton_move_to_start")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 370, 971, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.lineEdit_output_filename = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_output_filename.setGeometry(QtCore.QRect(720, 80, 131, 20))
        self.lineEdit_output_filename.setObjectName("lineEdit_output_filename")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(350, 40, 20, 331))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(660, 150, 41, 20))
        self.label_10.setObjectName("label_10")
        self.checkBox_theta = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_theta.setGeometry(QtCore.QRect(370, 120, 70, 17))
        self.checkBox_theta.setObjectName("checkBox_theta")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(430, 480, 31, 16))
        self.label_21.setObjectName("label_21")
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25.setGeometry(QtCore.QRect(5, 5, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(180, 260, 31, 20))
        self.label_7.setObjectName("label_7")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(590, 70, 47, 13))
        self.label_4.setObjectName("label_4")
        self.lineEdit_speed = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_speed.setGeometry(QtCore.QRect(550, 189, 61, 20))
        self.lineEdit_speed.setObjectName("lineEdit_speed")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(660, 120, 41, 20))
        self.label_9.setObjectName("label_9")
        self.lineEdit_thetastop = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_thetastop.setGeometry(QtCore.QRect(510, 120, 61, 20))
        self.lineEdit_thetastop.setObjectName("lineEdit_thetastop")
        self.ref_image = QtWidgets.QLabel(self.centralwidget)
        self.ref_image.setGeometry(QtCore.QRect(440, 219, 191, 151))
        self.ref_image.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ref_image.setText("")
        self.ref_image.setObjectName("ref_image")
        self.lineEdit_thetastart = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_thetastart.setGeometry(QtCore.QRect(440, 120, 61, 20))
        self.lineEdit_thetastart.setObjectName("lineEdit_thetastart")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(20, 590, 91, 16))
        self.label_14.setObjectName("label_14")
        self.lineEdit_phistep = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_phistep.setGeometry(QtCore.QRect(580, 90, 61, 20))
        self.lineEdit_phistep.setObjectName("lineEdit_phistep")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(660, 90, 41, 20))
        self.label_8.setObjectName("label_8")
        self.lineEdit_freq_center = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_freq_center.setGeometry(QtCore.QRect(110, 260, 61, 20))
        self.lineEdit_freq_center.setObjectName("lineEdit_freq_center")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(550, 460, 41, 16))
        self.label_18.setObjectName("label_18")
        self.progressBar_partial = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_partial.setGeometry(QtCore.QRect(110, 589, 201, 16))
        self.progressBar_partial.setProperty("value", 24)
        self.progressBar_partial.setObjectName("progressBar_partial")
        self.textBrowser_pointing_angle_theta = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_pointing_angle_theta.setGeometry(QtCore.QRect(410, 450, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setKerning(True)
        self.textBrowser_pointing_angle_theta.setFont(font)
        self.textBrowser_pointing_angle_theta.setAcceptDrops(True)
        self.textBrowser_pointing_angle_theta.setAcceptRichText(True)
        self.textBrowser_pointing_angle_theta.setObjectName("textBrowser_pointing_angle_theta")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(500, 480, 31, 16))
        self.label_22.setObjectName("label_22")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(30, 620, 81, 16))
        self.label_15.setObjectName("label_15")
        self.pushButton_output_file_browse = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_output_file_browse.setGeometry(QtCore.QRect(860, 80, 101, 23))
        self.pushButton_output_file_browse.setObjectName("pushButton_output_file_browse")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(530, 70, 47, 13))
        self.label_3.setObjectName("label_3")
        self.lineEdit_thetastep = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_thetastep.setGeometry(QtCore.QRect(580, 120, 61, 20))
        self.lineEdit_thetastep.setObjectName("lineEdit_thetastep")
        self.textBrowser_pointing_angle_phi = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_pointing_angle_phi.setGeometry(QtCore.QRect(340, 450, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setKerning(True)
        self.textBrowser_pointing_angle_phi.setFont(font)
        self.textBrowser_pointing_angle_phi.setAcceptDrops(True)
        self.textBrowser_pointing_angle_phi.setAcceptRichText(True)
        self.textBrowser_pointing_angle_phi.setObjectName("textBrowser_pointing_angle_phi")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 260, 91, 20))
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(410, 380, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.lineEdit_phistop = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_phistop.setGeometry(QtCore.QRect(510, 90, 61, 20))
        self.lineEdit_phistop.setObjectName("lineEdit_phistop")
        self.lineEdit_phistart = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_phistart.setGeometry(QtCore.QRect(440, 90, 61, 20))
        self.lineEdit_phistart.setObjectName("lineEdit_phistart")
        self.lineEdit_alphastep = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_alphastep.setGeometry(QtCore.QRect(580, 150, 61, 20))
        self.lineEdit_alphastep.setObjectName("lineEdit_alphastep")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(700, 380, 181, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.progressBar_total = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_total.setGeometry(QtCore.QRect(110, 619, 201, 16))
        self.progressBar_total.setProperty("value", 24)
        self.progressBar_total.setObjectName("progressBar_total")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(770, 40, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(150, 380, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.lineEdit_alphastart = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_alphastart.setGeometry(QtCore.QRect(440, 150, 61, 20))
        self.lineEdit_alphastart.setObjectName("lineEdit_alphastart")
        self.checkBox_phi = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_phi.setGeometry(QtCore.QRect(370, 90, 70, 17))
        self.checkBox_phi.setObjectName("checkBox_phi")
        self.lineEdit_alphastop = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_alphastop.setGeometry(QtCore.QRect(510, 150, 61, 20))
        self.lineEdit_alphastop.setObjectName("lineEdit_alphastop")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(770, 100, 47, 13))
        self.label_13.setObjectName("label_13")
        self.textBrowser_pointing_angle_alpha = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_pointing_angle_alpha.setGeometry(QtCore.QRect(480, 450, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setKerning(True)
        self.textBrowser_pointing_angle_alpha.setFont(font)
        self.textBrowser_pointing_angle_alpha.setAcceptDrops(True)
        self.textBrowser_pointing_angle_alpha.setAcceptRichText(True)
        self.textBrowser_pointing_angle_alpha.setObjectName("textBrowser_pointing_angle_alpha")
        self.listWidget_progress = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_progress.setGeometry(QtCore.QRect(30, 400, 256, 181))
        self.listWidget_progress.setObjectName("listWidget_progress")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(320, 0, 421, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(12)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(360, 480, 31, 16))
        self.label_20.setObjectName("label_20")
        self.checkBox_alpha = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_alpha.setGeometry(QtCore.QRect(370, 150, 70, 17))
        self.checkBox_alpha.setObjectName("checkBox_alpha")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(840, 260, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setObjectName("pushButton_start")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(930, 0, 41, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.lineEdit_freq_span = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_freq_span.setGeometry(QtCore.QRect(110, 290, 61, 20))
        self.lineEdit_freq_span.setObjectName("lineEdit_freq_span")
        self.label_26 = QtWidgets.QLabel(self.centralwidget)
        self.label_26.setGeometry(QtCore.QRect(180, 290, 31, 20))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.centralwidget)
        self.label_27.setGeometry(QtCore.QRect(0, 290, 101, 20))
        self.label_27.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(self.centralwidget)
        self.label_28.setGeometry(QtCore.QRect(140, 210, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.label_29 = QtWidgets.QLabel(self.centralwidget)
        self.label_29.setGeometry(QtCore.QRect(220, 260, 31, 20))
        self.label_29.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_29.setObjectName("label_29")
        self.label_30 = QtWidgets.QLabel(self.centralwidget)
        self.label_30.setGeometry(QtCore.QRect(330, 260, 31, 20))
        self.label_30.setObjectName("label_30")
        self.lineEdit_freq_step = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_freq_step.setGeometry(QtCore.QRect(260, 260, 61, 20))
        self.lineEdit_freq_step.setObjectName("lineEdit_freq_step")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(690, 40, 20, 331))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.label_31 = QtWidgets.QLabel(self.centralwidget)
        self.label_31.setGeometry(QtCore.QRect(210, 290, 41, 20))
        self.label_31.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_31.setObjectName("label_31")
        self.lineEdit_freq_points = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_freq_points.setGeometry(QtCore.QRect(260, 290, 61, 20))
        self.lineEdit_freq_points.setObjectName("lineEdit_freq_points")
        self.label_32 = QtWidgets.QLabel(self.centralwidget)
        self.label_32.setGeometry(QtCore.QRect(80, 40, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(self.centralwidget)
        self.label_33.setGeometry(QtCore.QRect(370, 500, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.textBrowser_freq_max_gain = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_freq_max_gain.setGeometry(QtCore.QRect(420, 520, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setKerning(True)
        self.textBrowser_freq_max_gain.setFont(font)
        self.textBrowser_freq_max_gain.setAcceptDrops(True)
        self.textBrowser_freq_max_gain.setAcceptRichText(True)
        self.textBrowser_freq_max_gain.setObjectName("textBrowser_freq_max_gain")
        self.label_34 = QtWidgets.QLabel(self.centralwidget)
        self.label_34.setGeometry(QtCore.QRect(490, 530, 41, 16))
        self.label_34.setObjectName("label_34")
        self.label_35 = QtWidgets.QLabel(self.centralwidget)
        self.label_35.setGeometry(QtCore.QRect(110, 170, 47, 13))
        self.label_35.setObjectName("label_35")
        self.lineEdit_ce_filename = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_ce_filename.setGeometry(QtCore.QRect(120, 160, 105, 20))
        self.lineEdit_ce_filename.setObjectName("lineEdit_ce_filename")
        self.pushButton_ce_file_browse = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ce_file_browse.setGeometry(QtCore.QRect(230, 150, 101, 23))
        self.pushButton_ce_file_browse.setObjectName("pushButton_ce_file_browse")
        self.label_36 = QtWidgets.QLabel(self.centralwidget)
        self.label_36.setGeometry(QtCore.QRect(75, 130, 331, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_36.setFont(font)
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self.centralwidget)
        self.label_37.setGeometry(QtCore.QRect(60, 180, 141, 16))
        self.label_37.setObjectName("label_37")
        self.pushButton_move_to_start_cal = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_move_to_start_cal.setGeometry(QtCore.QRect(720, 220, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_move_to_start_cal.setFont(font)
        self.pushButton_move_to_start_cal.setObjectName("pushButton_move_to_start_cal")
        self.label_error_defina_arquivo = QtWidgets.QLabel(self.centralwidget)
        self.label_error_defina_arquivo.setEnabled(True)
        self.label_error_defina_arquivo.setGeometry(QtCore.QRect(700, 290, 261, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.label_error_defina_arquivo.setPalette(palette)
        font = QtGui.QFont()
        font.setKerning(True)
        self.label_error_defina_arquivo.setFont(font)
        self.label_error_defina_arquivo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_error_defina_arquivo.setObjectName("label_error_defina_arquivo")
        self.commandLinkButton_cal = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton_cal.setGeometry(QtCore.QRect(830, 210, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.commandLinkButton_cal.setFont(font)
        self.commandLinkButton_cal.setObjectName("commandLinkButton_cal")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(700, 110, 261, 20))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.pushButton_check = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_check.setGeometry(QtCore.QRect(710, 260, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_check.setFont(font)
        self.pushButton_check.setObjectName("pushButton_check")
        self.mark_image = QtWidgets.QLabel(self.centralwidget)
        self.mark_image.setGeometry(QtCore.QRect(790, 260, 31, 31))
        self.mark_image.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mark_image.setText("")
        self.mark_image.setObjectName("mark_image")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 230, 249, 19))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton_singlefreq = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_singlefreq.setObjectName("radioButton_singlefreq")
        self.horizontalLayout.addWidget(self.radioButton_singlefreq)
        self.radioButton_sweepfreq_ss = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_sweepfreq_ss.setObjectName("radioButton_sweepfreq_ss")
        self.horizontalLayout.addWidget(self.radioButton_sweepfreq_ss)
        self.radioButton_sweepfreq_cs = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_sweepfreq_cs.setObjectName("radioButton_sweepfreq_cs")
        self.horizontalLayout.addWidget(self.radioButton_sweepfreq_cs)
        self.pushButton_reset_braco = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reset_braco.setGeometry(QtCore.QRect(890, 120, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton_reset_braco.setFont(font)
        self.pushButton_reset_braco.setObjectName("pushButton_reset_braco")
        self.comboBox_port = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_port.setGeometry(QtCore.QRect(160, 80, 61, 21))
        self.comboBox_port.setObjectName("comboBox_port")
        self.label_38 = QtWidgets.QLabel(self.centralwidget)
        self.label_38.setGeometry(QtCore.QRect(10, 80, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_38.setFont(font)
        self.label_38.setObjectName("label_38")
        self.pushButton_refresh_ports = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_refresh_ports.setGeometry(QtCore.QRect(230, 80, 51, 23))
        self.pushButton_refresh_ports.setObjectName("pushButton_refresh_ports")
        self.pushButton_test_port = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_test_port.setGeometry(QtCore.QRect(290, 80, 61, 23))
        self.pushButton_test_port.setObjectName("pushButton_test_port")
        self.pushButton_reset_plot = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reset_plot.setGeometry(QtCore.QRect(470, 590, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_reset_plot.setFont(font)
        self.pushButton_reset_plot.setObjectName("pushButton_reset_plot")
        self.label_39 = QtWidgets.QLabel(self.centralwidget)
        self.label_39.setGeometry(QtCore.QRect(20, 335, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_39.setFont(font)
        self.label_39.setObjectName("label_39")
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setGeometry(QtCore.QRect(0, 110, 361, 20))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.line_8 = QtWidgets.QFrame(self.centralwidget)
        self.line_8.setGeometry(QtCore.QRect(0, 190, 361, 20))
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.line_9 = QtWidgets.QFrame(self.centralwidget)
        self.line_9.setGeometry(QtCore.QRect(0, 310, 361, 20))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(240, 320, 90, 51))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton_equip_PI2 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_equip_PI2.setObjectName("radioButton_equip_PI2")
        self.verticalLayout.addWidget(self.radioButton_equip_PI2)
        self.radioButton_equip_rotor = QtWidgets.QRadioButton(self.widget)
        self.radioButton_equip_rotor.setObjectName("radioButton_equip_rotor")
        self.verticalLayout.addWidget(self.radioButton_equip_rotor)

        # --------------------menu_bar--------------------
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 972, 21))
        self.menubar.setObjectName("menubar")
        self.menuOpt = QtWidgets.QMenu(self.menubar)
        self.menuOpt.setObjectName("menuOpt")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionConfigMedida = QtWidgets.QAction(MainWindow)
        self.actionConfigMedida.setObjectName("actionConfigMedida")
        self.menuOpt.addAction(self.actionConfigMedida)
        self.menubar.addAction(self.menuOpt.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

# -------------------WINDOW_SETTINGS---------------
    #------------ cleaning cal status----------
        cal_file="calibration_status.csv"
        with open(cal_file, mode='w', newline='') as cal_set: #saving centers info in file
            wr = csv.writer(cal_set, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wr.writerow(["calibrated"])
            wr.writerow('0')
        cal_set.close() #closing file


    # -------------------- default values--------------------

        # angles
        self.lineEdit_phistart.setText('0')
        self.lineEdit_phistop.setText('180')
        self.lineEdit_phistep.setText('1')

        self.lineEdit_thetastart.setText('0')
        self.lineEdit_thetastop.setText('180')
        self.lineEdit_thetastep.setText('1')

        self.lineEdit_alphastart.setText('0')
        self.lineEdit_alphastop.setText('180')
        self.lineEdit_alphastep.setText('2')

        self.lineEdit_speed.setText('500')

        # freq
        self.lineEdit_freq_center.setText('14.25')

        self.radioButton_singlefreq.setChecked(True)

        self.lineEdit_freq_span.setEnabled(False)
        self.lineEdit_freq_step.setEnabled(False)
        self.lineEdit_freq_points.setEnabled(False)
        

        global freq_mode

        freq_mode="single"

        # progress
        self.progressBar_total.setValue(0)
        self.progressBar_partial.setValue(0)

        self.listWidget_progress.addItem('Aguardando início')

        # buttons
        self.pushButton_start.setEnabled(False)
        self.commandLinkButton_cal.setEnabled(False)

        self.pushButton_ce_file_browse.setVisible(False)
        self.label_35.setVisible(False)
        self.label_37.setVisible(False)

        # other
        last_IP=infos.load_last_IP()    
        self.lineEdit_ce_filename.setText(last_IP)    
        #self.lineEdit_ce_filename.setText("SA_AUTOTRAC_real.iseqx")
        #self.lineEdit_ce_filename.setText("SA_AUTOTRAC.iseqx")
        self.lineEdit_output_filename.setText("DIAGRAMA.csv")
        self.graphicsView_diagram.setBackground('w')

        self.radioButton_equip_PI2.setChecked(True)
        self.config_PI2()   

        # --------------------image--------------------
        pixmap = QtGui.QPixmap('axis_ref.png')
        pixmap = pixmap.scaled(self.ref_image.width(
        ), self.ref_image.height(), QtCore.Qt.KeepAspectRatio)
        self.ref_image.setPixmap(pixmap)

        # --------------------buttons--------------------
            # actions
        self.pushButton_start.clicked.connect(self.start_process)
        self.pushButton_reset.clicked.connect(self.reset_routine)
        self.pushButton_move_to_start.clicked.connect(self.move_start)
        self.pushButton_move_to_start_cal.clicked.connect(self.move_0)
        self.pushButton_check.clicked.connect(self.check)
        self.commandLinkButton_cal.clicked.connect(self.openCalWindow)

        self.pushButton_reset_plot.clicked.connect(self.reset_plot_routine)
        self.pushButton_reset_braco.clicked.connect(self.reset_pointing_system)
        self.pushButton_refresh_ports.clicked.connect(self.port_update)

        self.pushButton_test_port.clicked.connect(self.test_port)

            # menu bar

        self.actionConfigMedida.triggered.connect(self.config_meas)

            # browse file
        self.pushButton_output_file_browse.clicked.connect(self.saveFileDialog)
        self.pushButton_ce_file_browse.clicked.connect(self.chooseCEfile)

            # radio button
        self.radioButton_singlefreq.toggled.connect(self.single_freq)
        self.radioButton_sweepfreq_ss.toggled.connect(self.sweep_freq_ss)
        self.radioButton_sweepfreq_cs.toggled.connect(self.sweep_freq_cs)

        self.radioButton_equip_PI2.clicked.connect(self.config_PI2)
        self.radioButton_equip_rotor.clicked.connect(self.config_rotor)

        # --------------------other--------------------

        self.lineEdit_freq_step.editingFinished.connect(self.update_points)
        self.lineEdit_freq_points.editingFinished.connect(self.update_step)

    # ------------------------------------------------------


    # Reescreve os textos das labels da UI
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Start"))
        self.label_17.setText(_translate("MainWindow", "Ângulo de ganho máximo"))
        self.pushButton_reset.setText(_translate("MainWindow", "Limpar valores"))
        self.label_5.setText(_translate("MainWindow", "Velocidade de movimento"))
        self.label.setText(_translate("MainWindow", "Configurações de apontamento"))
        self.pushButton_move_to_start.setText(_translate("MainWindow", "Mover para \'Start\'"))
        self.label_10.setText(_translate("MainWindow", "Graus"))
        self.checkBox_theta.setText(_translate("MainWindow", "theta"))
        self.label_21.setText(_translate("MainWindow", "theta"))
        self.label_25.setText(_translate("MainWindow", "LabTelecom"))
        self.label_7.setText(_translate("MainWindow", "GHz"))
        self.label_4.setText(_translate("MainWindow", "Step"))
        self.label_9.setText(_translate("MainWindow", "Graus"))
        self.label_14.setText(_translate("MainWindow", "Progresso parcial"))
        self.label_8.setText(_translate("MainWindow", "Graus"))
        self.label_18.setText(_translate("MainWindow", "Graus"))
        self.label_22.setText(_translate("MainWindow", "alpha"))
        self.label_15.setText(_translate("MainWindow", "Progresso total"))
        self.pushButton_output_file_browse.setText(_translate("MainWindow", "Definir arquivo"))
        self.label_3.setText(_translate("MainWindow", "Stop"))
        self.label_6.setText(_translate("MainWindow", "Frequência central"))
        self.label_12.setText(_translate("MainWindow", "Resultados"))
        self.label_19.setText(_translate("MainWindow", "Diagrama de radiação"))
        self.label_11.setText(_translate("MainWindow", "Arquivo de saída"))
        self.label_16.setText(_translate("MainWindow", "Log"))
        self.checkBox_phi.setText(_translate("MainWindow", "phi"))
        self.label_13.setText(_translate("MainWindow", "(.csv)"))
        self.label_23.setText(_translate("MainWindow", "Medição de diagrama de radiação"))
        self.label_20.setText(_translate("MainWindow", "phi"))
        self.checkBox_alpha.setText(_translate("MainWindow", "alhpa"))
        self.pushButton_start.setText(_translate("MainWindow", "Iniciar Medição"))
        self.label_24.setText(_translate("MainWindow", "v1.3.0"))
        self.label_26.setText(_translate("MainWindow", "GHz"))
        self.label_27.setText(_translate("MainWindow", "Largura de banda"))
        self.label_28.setText(_translate("MainWindow", "Frequência"))
        self.label_29.setText(_translate("MainWindow", "Passo"))
        self.label_30.setText(_translate("MainWindow", "GHz"))
        self.label_31.setText(_translate("MainWindow", "Pontos"))
        self.label_32.setText(_translate("MainWindow", "Configurações de medição"))
        self.label_33.setText(_translate("MainWindow", "Frequência de ganho máximo"))
        self.label_34.setText(_translate("MainWindow", "GHz"))
        self.label_35.setText(_translate("MainWindow", "(.iseqx)"))
        self.pushButton_ce_file_browse.setText(_translate("MainWindow", "Definir arquivo"))
        self.label_36.setText(_translate("MainWindow", "IP do analisador de espectro"))
        self.label_37.setText(_translate("MainWindow", " (Keysight Command Expert)"))
        self.pushButton_move_to_start_cal.setText(_translate("MainWindow", "Mover para 0,0,0"))
        self.label_error_defina_arquivo.setText(_translate("MainWindow", "Verifique as configurações"))
        self.commandLinkButton_cal.setText(_translate("MainWindow", "Calibração"))
        self.pushButton_check.setText(_translate("MainWindow", "Verificar"))
        self.radioButton_singlefreq.setText(_translate("MainWindow", "Single point"))
        self.radioButton_sweepfreq_ss.setText(_translate("MainWindow", "Start-Stop"))
        self.radioButton_sweepfreq_cs.setText(_translate("MainWindow", "Center-Span"))
        self.pushButton_reset_braco.setText(_translate("MainWindow", "Reset braço"))
        self.label_38.setText(_translate("MainWindow", "Porta serial do braço mecânico"))
        self.pushButton_refresh_ports.setText(_translate("MainWindow", "Atualizar"))
        self.pushButton_test_port.setText(_translate("MainWindow", "Conectar"))
        self.pushButton_reset_plot.setText(_translate("MainWindow", "Limpar gráfico"))
        self.label_39.setText(_translate("MainWindow", "Equipamento apontador"))
        self.radioButton_equip_PI2.setText(_translate("MainWindow", "Braço 3 eixos"))
        self.radioButton_equip_rotor.setText(_translate("MainWindow", "Rotor 2 eixos"))
        self.menuOpt.setTitle(_translate("MainWindow", "Opções"))
        self.actionConfigMedida.setText(_translate("MainWindow", "Configuração de medida"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowTitle('Medição do diagrama de radiação')
    MainWindow.show()
    sys.exit(app.exec_())
