import numpy as np
import matplotlib.pyplot as plt

def trend(fname ,skip):
    dt =np.loadtxt(fname,skiprows=skip,delimiter=',')
    S,C = dt[:,0], dt[:,1] 

    plt.plot(S,label=u"Server"+fname)
    #plt.plot(C,color= 'darkorange',label=u"Client Side")



skip = 1000
cut = 20000
single = ('fps1.txt','fps2.txt','fps3.txt')
multi = ('fpsA.txt','fpsB.txt','fpsC.txt')
base =('S1.txt','S2.txt','S3.txt')

plt.title(u"fps trend")
plt.xlabel(u"Frame")
plt.ylabel(u"fps")
#compareFps(single,multi,base,skip,cut)
#trend("A0.txt",100)
#trend("C1.txt",100)
#trend("C2.txt",100)
#trend("C3.txt",100)
#trend("D1.txt",100)
#trend("D2.txt",100)
trend("SMC1.txt",100)
trend("SMC2.txt",100)
trend("SMC3.txt",100)

plt.legend()
plt.show()