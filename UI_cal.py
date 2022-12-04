# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Onedrive\AUTOTRAC\TEST_AUTOMATION\cal_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from pointing_system import move
from PYTHON_VC_TEST_AUTOMATION import search_max

import infos
import csv


class Ui_calWindow(object):

    # configuração da UI
    def setupUi(self, Dialog,port_dev, freq_center, centers, meas_equip, speed_meas):
        global port
        global freq
        global equipment
        global speed

        speed=speed_meas
        equipment=meas_equip
        freq = freq_center
        port = port_dev


###################################################################

        Dialog.setObjectName("Dialog")
        Dialog.resize(412, 367)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(120, 70, 160, 85))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalSlider_phi = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider_phi.setStatusTip("")
        self.horizontalSlider_phi.setMaximum(360)
        self.horizontalSlider_phi.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_phi.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.horizontalSlider_phi.setTickInterval(10)
        self.horizontalSlider_phi.setObjectName("horizontalSlider_phi")
        self.verticalLayout.addWidget(self.horizontalSlider_phi)
        self.horizontalSlider_theta = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider_theta.setMaximum(100)
        self.horizontalSlider_theta.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_theta.setObjectName("horizontalSlider_theta")
        self.verticalLayout.addWidget(self.horizontalSlider_theta)
        self.horizontalSlider_alpha = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider_alpha.setMaximum(360)
        self.horizontalSlider_alpha.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_alpha.setObjectName("horizontalSlider_alpha")
        self.verticalLayout.addWidget(self.horizontalSlider_alpha)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(290, 70, 56, 81))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.spinBox_phi = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        self.spinBox_phi.setMaximum(360)
        self.spinBox_phi.setSingleStep(1)
        self.spinBox_phi.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.spinBox_phi.setObjectName("spinBox_phi")
        self.verticalLayout_2.addWidget(self.spinBox_phi)
        self.spinBox_theta = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        self.spinBox_theta.setMaximum(180)
        self.spinBox_theta.setObjectName("spinBox_theta")
        self.verticalLayout_2.addWidget(self.spinBox_theta)
        self.spinBox_alpha = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        self.spinBox_alpha.setMaximum(360)
        self.spinBox_alpha.setObjectName("spinBox_alpha")
        self.verticalLayout_2.addWidget(self.spinBox_alpha)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(70, 70, 41, 80))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.pushButton_search_ref = QtWidgets.QPushButton(Dialog)
        self.pushButton_search_ref.setGeometry(QtCore.QRect(20, 40, 81, 23))
        self.pushButton_search_ref.setObjectName("pushButton_search_ref")
        self.pushButton_set_0 = QtWidgets.QPushButton(Dialog)
        self.pushButton_set_0.setGeometry(QtCore.QRect(190, 180, 131, 23))
        self.pushButton_set_0.setObjectName("pushButton_set_0")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(20, 70, 77, 83))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton_home_phi = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButton_home_phi.setObjectName("pushButton_home_phi")
        self.verticalLayout_4.addWidget(self.pushButton_home_phi)
        self.pushButton_home_theta = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButton_home_theta.setObjectName("pushButton_home_theta")
        self.verticalLayout_4.addWidget(self.pushButton_home_theta)
        self.pushButton_home_alpha = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButton_home_alpha.setObjectName("pushButton_home_alpha")
        self.verticalLayout_4.addWidget(self.pushButton_home_alpha)
        self.pushButton_search_max = QtWidgets.QPushButton(Dialog)
        self.pushButton_search_max.setGeometry(QtCore.QRect(40, 320, 111, 23))
        self.pushButton_search_max.setObjectName("pushButton_search_max")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(170, 320, 176, 22))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_phi_max = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_phi_max.setReadOnly(True)
        self.lineEdit_phi_max.setObjectName("lineEdit_phi_max")
        self.horizontalLayout.addWidget(self.lineEdit_phi_max)
        self.lineEdit_theta_max = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_theta_max.setReadOnly(True)
        self.lineEdit_theta_max.setObjectName("lineEdit_theta_max")
        self.horizontalLayout.addWidget(self.lineEdit_theta_max)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout.addWidget(self.lineEdit_3)
        self.pushButton_move = QtWidgets.QPushButton(Dialog)
        self.pushButton_move.setGeometry(QtCore.QRect(80, 180, 61, 23))
        self.pushButton_move.setObjectName("pushButton_move")
        self.label_message = QtWidgets.QLabel(Dialog)
        self.label_message.setGeometry(QtCore.QRect(100, 10, 211, 20))
        self.label_message.setObjectName("label_message")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(10, 260, 361, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.layoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.layoutWidget_3.setGeometry(QtCore.QRect(160, 220, 176, 22))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lineEdit_phi_ref = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.lineEdit_phi_ref.setReadOnly(True)
        self.lineEdit_phi_ref.setObjectName("lineEdit_phi_ref")
        self.horizontalLayout_6.addWidget(self.lineEdit_phi_ref)
        self.lineEdit_theta_ref = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.lineEdit_theta_ref.setReadOnly(True)
        self.lineEdit_theta_ref.setObjectName("lineEdit_theta_ref")
        self.horizontalLayout_6.addWidget(self.lineEdit_theta_ref)
        self.lineEdit_alpha_ref = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.lineEdit_alpha_ref.setReadOnly(True)
        self.lineEdit_alpha_ref.setObjectName("lineEdit_alpha_ref")
        self.horizontalLayout_6.addWidget(self.lineEdit_alpha_ref)
        self.label_message_2 = QtWidgets.QLabel(Dialog)
        self.label_message_2.setGeometry(QtCore.QRect(50, 220, 101, 20))
        self.label_message_2.setObjectName("label_message_2")
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(210, 300, 80, 15))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(350, 70, 45, 81))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.spinBox_phi_dec = QtWidgets.QSpinBox(self.verticalLayoutWidget_5)
        self.spinBox_phi_dec.setMaximum(360)
        self.spinBox_phi_dec.setSingleStep(1)
        self.spinBox_phi_dec.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.spinBox_phi_dec.setObjectName("spinBox_phi_dec")
        self.verticalLayout_5.addWidget(self.spinBox_phi_dec)
        self.spinBox_theta_dec = QtWidgets.QSpinBox(self.verticalLayoutWidget_5)
        self.spinBox_theta_dec.setMaximum(180)
        self.spinBox_theta_dec.setObjectName("spinBox_theta_dec")
        self.verticalLayout_5.addWidget(self.spinBox_theta_dec)
        self.spinBox_alpha_dec = QtWidgets.QSpinBox(self.verticalLayoutWidget_5)
        self.spinBox_alpha_dec.setMaximum(360)
        self.spinBox_alpha_dec.setObjectName("spinBox_alpha_dec")
        self.verticalLayout_5.addWidget(self.spinBox_alpha_dec)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(350, 50, 47, 13))
        self.label_7.setObjectName("label_7")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


        # --------------------buttons--------------------

        self.pushButton_search_ref.clicked.connect(self.home_all)
        self.pushButton_set_0.clicked.connect(self.set_0)



        self.spinBox_phi.editingFinished.connect(self.spinBox_changed)
        self.spinBox_theta.editingFinished.connect(self.spinBox_changed)
        self.spinBox_alpha.editingFinished.connect(self.spinBox_changed)


        self.horizontalSlider_phi.valueChanged.connect(self.slider_changed)
        self.horizontalSlider_theta.valueChanged.connect(self.slider_changed)
        self.horizontalSlider_alpha.valueChanged.connect(self.slider_changed)


        self.pushButton_home_phi.clicked.connect(self.home_phi)
        self.pushButton_home_theta.clicked.connect(self.home_theta)
        self.pushButton_home_alpha.clicked.connect(self.home_alpha)

        self.pushButton_search_max.clicked.connect(self.max_cal)
        self.pushButton_move.clicked.connect(self.move_cal)


        # --------------------default values--------------------

        self.horizontalSlider_phi.setValue(centers[0])
        self.horizontalSlider_theta.setValue(centers[1])
        self.horizontalSlider_alpha.setValue(centers[2])

        self.spinBox_phi.setValue(centers[0])
        self.spinBox_theta.setValue(centers[1])
        self.spinBox_alpha.setValue(centers[2])

        self.label_message.setVisible(True)

        # ----- verify homming ------
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


        if not calibrated:
            self.horizontalSlider_phi.setEnabled(False)
            self.horizontalSlider_theta.setEnabled(False)
            self.horizontalSlider_alpha.setEnabled(False)
            
            self.spinBox_phi.setEnabled(False)
            self.spinBox_theta.setEnabled(False)
            self.spinBox_alpha.setEnabled(False)        

            self.pushButton_move.setEnabled(False)
        else:
            self.horizontalSlider_phi.setEnabled(True)
            self.horizontalSlider_theta.setEnabled(True)
            self.horizontalSlider_alpha.setEnabled(True)
            
            self.spinBox_phi.setEnabled(True)
            self.spinBox_theta.setEnabled(True)
            self.spinBox_alpha.setEnabled(True)        

            self.pushButton_move.setEnabled(True)

# equip

        equip=infos.load_equip()
        if equip=='PI2':
            self.spinBox_theta.setMaximum(100)
            self.horizontalSlider_theta.setMaximum(100)
            if calibrated:
                self.horizontalSlider_alpha.setEnabled(True)
                self.spinBox_alpha.setEnabled(True)
                self.spinBox_alpha_dec.setEnabled(True)
        elif equip=='rotor':
            self.spinBox_theta.setMaximum(180)
            self.horizontalSlider_theta.setMaximum(180)
            self.horizontalSlider_alpha.setEnabled(False)
            self.spinBox_alpha.setEnabled(False)
            self.spinBox_alpha_dec.setEnabled(False)
            


        phi_0,theta_0,alpha_0=infos.load_cal()

        self.lineEdit_phi_ref.setText(str(phi_0))
        self.lineEdit_theta_ref.setText(str(theta_0))
        self.lineEdit_alpha_ref.setText(str(alpha_0))
    
            
#-------------------FUNCTIONS-------------------

    # realiza a movimentação do equipamento apontador para as posições definidas pelo usuário nas caixas de texto correspondentes
    def move_cal(self):
        global speed
        global port

        phi=float(self.spinBox_phi.value())
        theta=float(self.spinBox_theta.value())
        alpha=float(self.spinBox_alpha.value())

        phi+=float(self.spinBox_phi_dec.value()*0.1)
        theta+=float(self.spinBox_theta_dec.value()*0.1)
        alpha+=float(self.spinBox_alpha_dec.value()*0.1)

        coordinate_in=[phi, theta, alpha, speed]
        move(coordinate_in, "send_gcode",port)


    # realiza a busca pelo apontamento de máximo ganho nas imediações do ângulo apontado pelo usuário
    def max_cal(self):
        global port, freq
        global equipment

        print("Search Max")

        global speed

        phi0=self.spinBox_phi.text()
        theta0=self.spinBox_theta.text()
        alpha0=self.spinBox_alpha.text()
        phi_max,theta_max=search_max(phi0,theta0, alpha0, speed, float(freq)*1e9, port, equipment)
        self.lineEdit_phi_max.setText(str(phi_max))
        self.lineEdit_theta_max.setText(str(theta_max))
        

    # define como 0,0,0 os ângulos absolutos fornecidos pelo usuário nas caixas correspondentes
    # a janela principal trabalha com os ângulos relativos a essa referência
    # todos os campos da janela de calibração trabalham com o ângulos absolutos
    def set_0(self):
        print('set new 0')
        
        phi=self.spinBox_phi.value()
        theta=self.spinBox_theta.value()
        alpha=self.spinBox_alpha.value()
        
        centers=[str(phi),str(theta),str(alpha)]
        cal_file="calibration_settings.csv"
        with open(cal_file, mode='w', newline='') as cal_set: #saving centers info in file
            wr = csv.writer(cal_set, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wr.writerow(["phi","theta","alpha"])
            wr.writerow(centers)
        cal_set.close() #closing file

        self.lineEdit_phi_ref.setText(str(phi))
        self.lineEdit_theta_ref.setText(str(theta))
        self.lineEdit_alpha_ref.setText(str(alpha))


   #-------------------Homing------------------- 

    # envia todos os eixos para a origem absoluta
    # no braço de 3 eixos, procura os sensores fim de curso
    # no rotor de 2 eixos vai para 0,0
    def home_all(self):
        global ser
        global port

        print('home all')
        speed=10000
        coordinate_in=[0, 0, 0, speed]
        move(coordinate_in, "homing",port)

        self.horizontalSlider_phi.setEnabled(True)
        self.horizontalSlider_theta.setEnabled(True)
        self.horizontalSlider_alpha.setEnabled(True)
        
        self.spinBox_phi.setEnabled(True)
        self.spinBox_theta.setEnabled(True)
        self.spinBox_alpha.setEnabled(True)        

        self.pushButton_move.setEnabled(True)

        cal_file="calibration_status.csv"
        with open(cal_file, mode='w', newline='') as cal_set: #saving centers info in file
            wr = csv.writer(cal_set, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wr.writerow(["calibrated"])
            wr.writerow('1')
        cal_set.close() #closing file
        
    # envia o eixo phi para a origem absoluta
    # no braço de 3 eixos, procura o sensor fim de curso
    # no rotor de 2 eixos vai para 0
    def home_phi(self):
        global ser
        global port

        print('home all')
        speed=10000
        coordinate_in=[0, 0, 0, speed]
        move(coordinate_in, "homing_x",port)

    # envia o eixo theta para a origem absoluta
    # no braço de 3 eixos, procura o sensor fim de curso
    # no rotor de 2 eixos vai para 0
    def home_theta(self):
        global ser
        global port

        speed=10000
        coordinate_in=[0, 0, 0, speed]
        move(coordinate_in, "homing_y",port)

    # envia o eixo alpha para a origem absoluta
    # no braço de 3 eixos, procura o sensor fim de curso
    # no rotor de 2 eixos vai para 0
    def home_alpha(self):
        global ser
        global port

        print('home all')
        speed=10000
        coordinate_in=[0, 0, 0, speed]
        move(coordinate_in, "homing_z",port)

    #-------------Updates-----------------------------


    # Atualiza a posição dos sliders baseada na informação inserida nas spinbox
    def spinBox_changed(self):
        #movement
        global port
        phi=self.spinBox_phi.value()
        theta=self.spinBox_theta.value()
        alpha=self.spinBox_alpha.value()


        #update slider
        self.horizontalSlider_phi.setValue(self.spinBox_phi.value())
        self.horizontalSlider_theta.setValue(self.spinBox_theta.value())
        self.horizontalSlider_alpha.setValue(self.spinBox_alpha.value())
        
    # Atualiza o número das spinbox baseado na movimentação dos sliders pelo usuário
    def slider_changed(self):
        #movement
        global port
        phi=self.spinBox_phi.value()
        theta=self.spinBox_theta.value()
        alpha=self.spinBox_alpha.value()

        #update box
        self.spinBox_phi.setValue(self.horizontalSlider_phi.value())
        self.spinBox_theta.setValue(self.horizontalSlider_theta.value())
        self.spinBox_alpha.setValue(self.horizontalSlider_alpha.value())



    

    #------------------------------------------

    # Reescreve as labels da UI
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "phi"))
        self.label_2.setText(_translate("Dialog", "theta"))
        self.label_3.setText(_translate("Dialog", "alpha"))
        self.pushButton_search_ref.setText(_translate("Dialog", "Home Geral"))
        self.pushButton_set_0.setText(_translate("Dialog", "Definir como 0,0,0"))
        self.pushButton_home_phi.setText(_translate("Dialog", "Home"))
        self.pushButton_home_theta.setText(_translate("Dialog", "Home"))
        self.pushButton_home_alpha.setText(_translate("Dialog", "Home"))
        self.pushButton_search_max.setText(_translate("Dialog", "Procurar máximo"))
        self.pushButton_move.setText(_translate("Dialog", "Mover"))
        self.label_message.setText(_translate("Dialog", "Realizar operação \'Home\' para liberar eixos"))
        self.label_message_2.setText(_translate("Dialog", "Referência definida"))
        self.label_4.setText(_translate("Dialog", "phi"))
        self.label_5.setText(_translate("Dialog", "theta"))
        self.label_6.setText(_translate("Dialog", "alpha"))
        self.label_7.setText(_translate("Dialog", "Decimal"))

if __name__ == "__main__":
    port='COM12'
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_calWindow()
    ui.setupUi(Dialog,port)
    Dialog.setWindowTitle('Calibração')
    Dialog.show()
    sys.exit(app.exec_())
