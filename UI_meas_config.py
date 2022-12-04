# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Onedrive\AUTOTRAC\TEST_AUTOMATION\meas_config.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import csv
import infos


class Ui_Config(object):

    # configuração da UI
    def setupUi(self, Config):
        Config.setObjectName("Config")
        Config.resize(278, 272)
        self.pushButton_ok = QtWidgets.QPushButton(Config)
        self.pushButton_ok.setGeometry(QtCore.QRect(110, 240, 75, 23))
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.label_4 = QtWidgets.QLabel(Config)
        self.label_4.setGeometry(QtCore.QRect(80, 20, 161, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.layoutWidget = QtWidgets.QWidget(Config)
        self.layoutWidget.setGeometry(QtCore.QRect(200, 60, 56, 126))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_num_samples = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_num_samples.setObjectName("lineEdit_num_samples")
        self.verticalLayout.addWidget(self.lineEdit_num_samples)
        self.lineEdit_time_phi = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_time_phi.setObjectName("lineEdit_time_phi")
        self.verticalLayout.addWidget(self.lineEdit_time_phi)
        self.lineEdit_time_all = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_time_all.setObjectName("lineEdit_time_all")
        self.verticalLayout.addWidget(self.lineEdit_time_all)
        self.lineEdit_margin_max = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_margin_max.setObjectName("lineEdit_margin_max")
        self.verticalLayout.addWidget(self.lineEdit_margin_max)
        self.lineEdit_margin_step = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_margin_step.setObjectName("lineEdit_margin_step")
        self.verticalLayout.addWidget(self.lineEdit_margin_step)
        self.layoutWidget1 = QtWidgets.QWidget(Config)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 60, 176, 131))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.label_6 = QtWidgets.QLabel(Config)
        self.label_6.setGeometry(QtCore.QRect(50, 210, 121, 20))
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Config)
        QtCore.QMetaObject.connectSlotsByName(Config)


        ############

        self.pushButton_ok.clicked.connect(self.apply_config)
        num_samples, time_phi, time_all, margin_max, margin_step = infos.load_config()



        self.lineEdit_num_samples.setText(str(num_samples))
        self.lineEdit_time_phi.setText(str(time_phi))
        self.lineEdit_time_all.setText(str(time_all))
        self.lineEdit_margin_max.setText(str(margin_max))
        self.lineEdit_margin_step.setText(str(margin_step))
        

    ################################

    # aplica as configurações definidas pelo usuário
    # salva no arquivo "meas_config.csv" as respectivas informações
    def apply_config(self):
        cal_file="meas_config.csv"
        with open(cal_file, mode='w', newline='') as cal_set: #saving centers info in file
            wr = csv.writer(cal_set, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            wr.writerow(["num_samples", "time_phi", "time_all","margin_max","margin_step"])
            wr.writerow([self.lineEdit_num_samples.text(),self.lineEdit_time_phi.text(), self.lineEdit_time_all.text(), self.lineEdit_margin_max.text(), self.lineEdit_margin_step.text()])
        cal_set.close() #closing file
        print('Config Applied!')



    ################################

    # Reescreve as labes da UI
    def retranslateUi(self, Config):
        _translate = QtCore.QCoreApplication.translate
        Config.setWindowTitle(_translate("Config", "Dialog"))
        self.pushButton_ok.setText(_translate("Config", "OK"))
        self.label_4.setText(_translate("Config", "Configurações de medida"))
        self.label.setText(_translate("Config", "Numero de amostras"))
        self.label_3.setText(_translate("Config", "Tempo de espera Phi (s)"))
        self.label_2.setText(_translate("Config", "Tempo de espera geral (s)"))
        self.label_5.setText(_translate("Config", "Margem de varredura de máximo (°)"))
        self.label_7.setText(_translate("Config", "Passo de varredura de máximo (°)"))
        self.label_6.setText(_translate("Config", "Procura em +/- margem"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Config = QtWidgets.QDialog()
    ui = Ui_Config()
    ui.setupUi(Config)
    Config.show()
    Config.setWindowTitle('Configurações de medição')
    sys.exit(app.exec_())
