import serial
from datetime import datetime
from pynput.keyboard import Key, Listener
import re

# Global variables
sensor_data = {}
timestamps = []
is_plotting = False
p = re.compile(r'^S\d{2}-M-\d+')
maxNumberInGraf = 5

gerarCsv = True

def editarPrimeiraLinha(dictData):
    lista = ["tempo"]
    nLista = list(dictData.keys())
    lista = lista + nLista
    novaLinha = ",".join(str(item) for item in lista)
    with open("arquivo.csv","r+") as arquivo:
        arquivo.seek(0)
        arquivo.write(novaLinha+"\n")

def adicionarNovaLinha(lista):
    listaF = ",".join(str(item) for item in lista)
    with open("arquivo.csv","a") as arquivo:
        arquivo.write(listaF+'\n')

def pad_arrays(arrays):
    max_length = max(len(array) for array in arrays)
    padded_arrays = [[None] * (max_length - len(array)) + array for array in arrays]
    return padded_arrays

def read_serial():
    global sensor_data, timestamps, p, maxNumberInGraf
    ser = serial.Serial('COM5', 115200)  # Replace COM3 with your serial port
    while True:
        line = ser.readline().decode().strip()
        val = p.match(line)
        if val:
            if line:
                sensor, value = line.split("-M-")
                timestamp = datetime.now().strftime("%M:%S.%f3")[:-4]
                if sensor not in sensor_data:
                    sensor_data[sensor] = []
                    if gerarCsv:
                        editarPrimeiraLinha(sensor_data)
                for ss in sensor_data.keys():
                    if ss == sensor:
                        sensor_data[sensor].append(int(value))
                    else:
                        sensor_data[ss].append(sensor_data[ss][-1])
                
                timestamps.append(timestamp)                    
                if gerarCsv:
                    listaParaCsv = [timestamp]
                    for ss in sensor_data.keys():
                        listaParaCsv.append(sensor_data[ss][-1])
                    adicionarNovaLinha(listaParaCsv)
                else:
                    plot_graph()
        else:
            print("Line error")
            
        if is_plotting:
            break
    ser.close()

def plot_graph():
    global sensor_data, timestamps
    newArrayDarray = []
    for x in sensor_data.keys():
        newArrayDarray.append(sensor_data[x])
    
    newArrayDarray.append(timestamps)
    
    newArrays = pad_arrays(newArrayDarray)
    cont = 0
    for x in sensor_data.keys():
        sensor_data[x] = newArrays[cont]
        cont = cont +1
        

def on_press(key):
    global is_plotting
    try:
        if key == Key.f2:
            is_plotting = True
            
    except AttributeError:
        pass

def setup_keyboard_listener():
    listener = Listener(on_press=on_press)
    listener.start()
    return listener

def main():
    global sensor_data, timestamps
    sensor_data = {}
    timestamps = []
    listener = setup_keyboard_listener()

    try:
        # Start reading serial data continuously
        read_serial()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping...")
    finally:
        listener.stop()

if __name__ == '__main__':
    main()