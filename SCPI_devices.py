import pyvisa as visa

def list_resources(sim): # "sim" flag enables listing of the devices described in the devices_mock.yaml file
    if (sim):
        rm = visa.ResourceManager('devices_mock.yaml@sim')  
    else:
        rm = visa.ResourceManager()

    print(rm.list_resources())
    
#defining equipments

class equipment:
    def __init__(self, name):
        self.name = name # instrument name (free)
    
    def connect(self,mode, addr): #connects to an instrument. Input: mode (connextion mode) [string]: TCPIP, GPIB, sim / addr (equipment address) [int]: IP or GPIB address
        match mode:
            case "TCPIP":
                rm = visa.ResourceManager()
                print("Connecting to" + "TCPIP0::" + str(addr)+ "::inst0::INSTR")
                self.inst = rm.open_resource('TCPIP0::'+str(addr)+'::inst0::INSTR', read_termination='\n', write_termination='\n')
                self.SCPI_present()
            case "GPIB":
                rm = visa.ResourceManager()
                print("Connecting to" + "GPIB0::" + str(addr)+ "::inst0::INSTR")
                self.inst = rm.open_resource('GPIB0::' +str(addr)+ '::INSTR', read_termination='\n',write_termination='\n') 
                self.SCPI_present()
            case "sim": #simulated mode
                rm_sim = visa.ResourceManager('devices_mock.yaml@sim')
                self.inst = rm_sim.open_resource('GPIB0::'+str(addr)+'::INSTR', read_termination='\n',write_termination='\n')
                self.SCPI_present()
            case _: #error
                return -1

    def SCPI_present(self): # instrument self identification
        self.equip_id = self.inst.query("*IDN?") #query ID
        print(f"Device Connected. ID: {self.equip_id}")    

    def status(self):
        pass

    def disconnect_equip(self):
        self.inst.close()

class spectrum_analyser(equipment):
        
    def set_freq(self, freq):
        self.inst.write(':SENSe:FREQuency:CENTer %.2f' % (freq))
        
    def set_span(self, freq_span):
        self.inst.write(':SENSe:FREQuency:SPAN %.2f' % (freq_span))

    def set_BW(self,bw):
        self.inst.write(':SENSe:BANDwidth:RESolution %.2f' % (bw))

    def peak_search(self):
        self.inst.write(':CALCulate:MARKer:PEAK:SEARch:MODE %s' % ('MAXimum')) # equivalent to pressing "peak search" key
        self.inst.write(':CALCulate:MARKer:Y?') # returns the value of the peak search
        return self.inst.read()


class RF_generator(equipment):
    
    def set_freq(self, freq):
        self.inst.write(':SENSe:FREQuency:CENTer %.2f' % (freq))
        
    def RF_on(self):
        self.inst.write(':OUTPut:STATe %d' % (1)) 

    def RF_off(self):
        self.inst.write(':OUTPut:STATe %d' % (0))

    def MOD_on(self):
        self.inst.write(':OUTPut:MODulation:STATe %d' % (1))

    def MOD_off(self):
        self.inst.write(':OUTPut:MODulation:STATe %d' % (0))

    def set_power(self,power): # output power in dBm
        self.inst.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude %.2f DBM' % (power)) 


class osciloscope(equipment):
    def measure_amplitude_scope(self,channel):
        channel_str = "CHANNEL" + str(channel)
        temp_values = self.inst.query_ascii_values(':MEASure:VAMPlitude? %s' % (channel_str))
        amplitude = temp_values[0]
        return amplitude

    def reset_statistics(self):
        self.inst.write(':MEASure:STATistics:RESet')