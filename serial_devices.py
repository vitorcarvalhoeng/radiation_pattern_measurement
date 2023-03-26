
# project functions
from pointing_system import move, start_serial, disconnect


#definindo equipamentos

class equipment:
    def __init__(self, name):
        self.name = name #nome do instrumento (livre)
    
    def connect(self,mode, addr,baud): #conecta-se ao instrumento. Input: modo (modo de conexão): TCPIP, GPIB / addr (endereço do equipamento): IP, GPIB address 

        match mode:
            case "serial":
                self.ser = start_serial(addr,baud)
            case _: #error
                return -1

    def SCPI_present(self):
        pass 

    def status(self):
        pass

    def disconnect_equip(self):
        disconnect(self.ser)


class positioner(equipment):

    def home(self):
        move(self.ser, 0, "homing")

    def set_position(self, phi, theta, alpha):
        self.phi = phi
        self.theta = theta
        self.alpha = alpha
        move(self.ser, [self.phi, self.theta, self.alpha, self.speed],"send_gcode")

    def set_speed(self, speed):
        self.speed = speed

    def set_ref(self):
        move(self.ser,0,"set_ref")
        
    def stop(self):
        move(self.ser, 0, "stop")

