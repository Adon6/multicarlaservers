import numpy as np
import matplotlib.pyplot as plt
def compareFps(single,multi,base,skip,cut):
    s1name,s2name,s3name = single
    m1name,m2name,m3name = multi
    b1n,b2n,b3n = base
    s1 = np.loadtxt(s1name,skiprows=skip,delimiter=',')
    s2 = np.loadtxt(s2name,skiprows=skip,delimiter=',')
    s3 = np.loadtxt(s3name,skiprows=skip,delimiter=',')
    m1 = np.loadtxt(m1name,skiprows=skip,delimiter=',')
    m2 = np.loadtxt(m2name,skiprows=skip,delimiter=',')
    m3 = np.loadtxt(m3name,skiprows=skip,delimiter=',')
    b1 = np.loadtxt(b1n,skiprows=skip,delimiter=',')
    b2 = np.loadtxt(b2n,skiprows=skip,delimiter=',')
    b3 = np.loadtxt(b3n,skiprows=skip,delimiter=',')
    col0 =(slice(0,cut),0)
    col1 =(slice(0,cut),1)
    avg_s = (s1[col0]+s2[col0]+s3[col0])/3
    avg_m = (m1[col0]+m2[col0]+m3[col0])/3
    und_s = (s1[col1]+s2[col1]+s3[col1])/3
    und_m = (m1[col1]+m2[col1]+m3[col1])/3
    base_se = (b1[col0]+b2[col0]+b3[col0])/3
    base_cl = (b1[col1]+b2[col1]+b3[col1])/3
    Smult =np.mean(avg_m)
    Ssing =np.mean(avg_s)
    Cmult =np.mean(und_m)
    Csing =np.mean(und_s)
    Bs =np.mean(base_se)
    Bm =np.mean(base_cl)
    print("S mult:{} sing:{}; \n C mult:{} sing:{} \n B mult:{} sing:{}".format(Smult,Ssing,Cmult,Csing,Bm,Bs))
    ll = np.linspace(0,cut,cut)
    l2 = np.linspace(30,30,cut)
    l1 = np.linspace(1,1,cut)
    plt.subplot(2,1,1)
    plt.title(u"fps on server side")
    plt.xlabel(u"Frame")
    plt.ylabel(u"fps")
    plt.plot(base_se,color='g',label=u"Base line")
    plt.plot(avg_m,color = 'c',label=u"Three Server")
    plt.plot(avg_s,color= 'darkorange',label=u"One Servers")
    plt.fill_between(ll,0,avg_m,avg_s<avg_m,color='c')
    plt.fill_between(ll,0,avg_s,avg_m<avg_s,color='darkorange')
    plt.legend()
    #plt.fill_between(ll,0,l1,avg_m==avg_s,color='white')
    plt.subplot(2,1,2)
    plt.title(u"fps on client side")
    plt.xlabel(u"Frame")
    plt.ylabel(u"fps")
    plt.plot(base_cl,color='g',label=u"Base line")
    plt.plot(und_s,color='tomato',label=u"One Server")
    plt.plot(und_m,color='deepskyblue',label=u"Three Servers")
    plt.fill_between(ll,0,und_m,und_s< und_m,color='deepskyblue')
    plt.fill_between(ll,0,und_s,und_m< und_s,color='tomato')
    #plt.fill_between(ll,0,l2,und_m==und_s,color='white')
    plt.legend()
    plt.show()

skip = 1000
cut = 20000
single = ('fps1.txt','fps2.txt','fps3.txt')
multi = ('fpsA.txt','fpsB.txt','fpsC.txt')
base =('S1.txt','S2.txt','S3.txt')

compareFps(single,multi,base,skip,cut)