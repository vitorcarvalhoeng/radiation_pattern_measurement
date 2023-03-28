
# project functions
from pointing_system import move, start_serial, disconnect

from mock_serial import MockSerial
from serial import Serial




#definindo equipamentos

class equipment(object):
    def __init__(self, name):
        self.name = name #nome do instrumento (livre)

    connection_mode = 'r' # 'r' = real, 's' = simulated
    
    def connect(self,mode, addr,baud): #conecta-se ao instrumento. Input: modo (modo de conexão): TCPIP, GPIB / addr (endereço do equipamento): IP, GPIB address 

        match mode:
            case "serial":
                self.ser = start_serial(addr,baud)
                self.connection_mode = 'r'
            case "serial_mock": #simulated device
                self.device_mock = MockSerial()
                stub = self.device_mock.stub(
                    receive_bytes=b'G28\n',
                    send_bytes=b'ok\n'
                )

                self.device_mock.open()
                self.ser = Serial(self.device_mock.port)
                self.connection_mode = 's'
                print("Serial mock device connected.")

                
            case _: #error
                return -1

    def SCPI_present(self):
        pass 

    def status(self):
        pass

    def disconnect_equip(self):
        if self.connection_mode == 'r':
            disconnect(self.ser)
        elif self.connection_mode == 's':    
            self.ser.close()
            self.device_mock.close()
            print("Serial mock device disconnected.")


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

