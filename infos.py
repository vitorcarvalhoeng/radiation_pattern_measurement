import csv


#Lê informações do arquivo last_ip.csv
#Retorna uma string com o último IP do analisador de espectro utilizado

def load_last_IP():
    cal_file="last_ip.csv"
    with open(cal_file, mode='r', newline='') as cal_set:  # reading centers info from file
        cal_info = csv.reader(cal_set, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        line_count = 0
        for row in cal_info:
            if line_count == 0:
                print(', '.join(row))
                line_count += 1
            else:
                ip = row[0]
    cal_set.close()  # closing file

    return ip

#Lê informações do arquivo equip_config.csv
#Retorna uma string com o equipamento apontador a ser utilizado (configurado na UI)
# Valores possíveis: 'PI2', 'rotor'

def load_equip():
    cal_file="equip_config.csv"
    with open(cal_file, mode='r', newline='') as cal_set:  # reading centers info from file
        cal_info = csv.reader(cal_set, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        line_count = 0
        for row in cal_info:
            if line_count == 0:
                print(', '.join(row))
                line_count += 1
            else:
                equip = row[0]
    cal_set.close()  # closing file

    return equip

#Lê informações do arquivo meas_config.csv
#Retorna um vetor contendo as informações de configurações na ordem:
# numero de amostras para realizar média, 
# tempo de espera em phi, 
# tempo de espera em todos os eixos,
# margem angular para procura da direção de máximo ganho (+- margem), 
# passo angular da procura pelo apontamento de ganho máximo

def load_config():
    cal_file="meas_config.csv"
    with open(cal_file, mode='r', newline='') as cal_set:  # reading centers info from file
        cal_info = csv.reader(cal_set, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        line_count = 0
        for row in cal_info:
            if line_count == 0:
                print(', '.join(row))
                line_count += 1
            else:
                num_samples = int(row[0])
                time_phi = int(row[1])
                time_all = int(row[2])
                margin_max = int(row[3])
                margin_step = float(row[4])
    cal_set.close()  # closing file


    return num_samples, time_phi, time_all, margin_max, margin_step

#Lê informações do arquivo calibration_settings.csv
#Retorna um vetor contendo as informações de calibração (0,0,0) na ordem:
# phi, theta, alpha

def load_cal():
    cal_file="calibration_settings.csv"
    with open(cal_file, mode='r', newline='') as cal_set: #reading centers info from file
        cal_info = csv.reader(cal_set, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        line_count=0
        for row in cal_info:
            if line_count ==0:
                print(', '.join(row))
                line_count+=1
            else:
                phi_center=int(row[0])
                theta_center=int(row[1])
                alpha_center=int(row[2])
    cal_set.close() #closing file

    return phi_center, theta_center, alpha_center

# Carrega os limites superiores do equipamento apontador definido
def load_limits():
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