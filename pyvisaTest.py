import pyvisa
import sched, time
import winsound

def do_something(scheduler): 
    hora_atual = time.localtime()
    
rm = pyvisa.ResourceManager()
#rm.list_resources()
inst = rm.open_resource('USB0::0x049F::0x505E::CN2236029029753::0::INSTR')
sumData1 = 0
sumData2 = 0
msStart = time.time_ns()
for _ in range(10):
    data1 = inst.query("MEASure:CHANnel1:ITEM? VMAX")
    data2 = inst.query("MEASure:CHANnel2:ITEM? VMAX")
    sumData1 += float(data1[:5])
    sumData2 += float(data2[:5])
    
msTotal = time.time_ns()-msStart
print(sumData1/10)
print(sumData2/10)
print(msTotal)
rm.close()