import pyvisa
import sched, time
import winsound

def do_something(scheduler): 
    hora_atual = time.localtime()
    rm = pyvisa.ResourceManager()
    vezes = 1
    #rm.list_resources()
    inst = rm.open_resource('USB0::0x049F::0x505E::CN2236029029753::0::INSTR')
    sumData1 = 0
    sumData2 = 0
    noget = False
    #for _ in range(vezes):
    try:
        data1 = inst.query("MEASure:CHANnel1:ITEM? VMAX")
        data2 = inst.query("MEASure:CHANnel2:ITEM? VMAX")
    except:
        noget = True
    
    if noget == False:
        sumData1 = sumData1+float(data1[:5])
        sumData2 = sumData2+float(data2[:5])
        
        current = ((sumData1/vezes)-(sumData2/vezes))/1.3

        if float(data2[:5]) <= 2.8:
            while(1):
                for _ in range(12):
                    winsound.Beep(2500, 200)
                time.sleep(1)
                
        f = open("relatorio2.csv","a")
        dataRec = time.strftime("%H:%M:%S", hora_atual)+","+str(round(sumData1/vezes,3))+","+str(round(sumData2/vezes,3))+","+str(round(current,3))+"\n"
        f.write(dataRec)
        print(time.strftime("%H:%M:%S", hora_atual)+","+str(round(sumData1/vezes,3))+","+str(round(sumData2/vezes,3))+","+str(round(current,3)))
        f.close()
    rm.close()
    repetir()

def repetir():
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(30, 0, do_something, (my_scheduler,))
    my_scheduler.run()

if __name__ == "__main__":
    repetir()