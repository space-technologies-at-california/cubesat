# variable input
# a?semi-long axi(m)
# e:ecentricity (0<e<1)
# i:inclination angle of orbit(rad)
# omega:big omega in the graph(rad)
# w:angle between ascending point and perigee, small omega in the graph(rad)
# T:t for a whole period(s)
# dt:time interval
#***********************

import numpy as np
import matplotlib.pyplot as plt
import pylab as py

def OrbitLiveCalculator(a,e,i,omega,w,T,dt):

    u=3.986005e14 #gravitational const
    n=np.sqrt(u/a**3) #average angular velocity of satelite
    w_e=7.292115e-5 #average angular velocity of earth
    t0=0 #initial time
    G0=107 #t0,Greenwich longtitude
    #you can use linspace get different points density
    t=np.arange(0,T,dt)
    N=len(t)
    tp=0 #assume satelite begins at perigee, you can also assume it at other time
    #********************

    #Newton's law of computation

    M=[n*(t-tp) for t in t]
    E=[]
    er=1e-8
    ee=1
    E0=1

    for i1 in range(N):

        while ee>er:

            E1=E0-(E0-e*np.sin(E0)-M[i1])/(1-e*np.cos(E0))
            ee=abs(E0-E1)
            E0=E1

        E.append(E1)

        ee=1
        E0=1


    #**********************
    f=[2*np.arctan(((1+e)/(1-e))**0.5*np.tan(E/2)) for E in E]

    # f=n*(t-tp)

    S= [a*(1-e**2)/(1+e*np.cos(f)) for f in f]

    Ax=[np.cos(omega)*np.cos(w+f)-np.sin(omega)*np.sin(w+f)*np.cos(i) for f in f]
    Ay=[np.sin(omega)*np.cos(w+f)+np.cos(omega)*np.sin(w+f)*np.cos(i) for f in f]
    Az=[np.sin(w+f)*np.sin(i) for f in f ]



    x=[S[a]*Ax[a] for a in range(len(S))]
    y=[S[a]*Ay[a] for a in range(len(S))]
    z=[S[a]*Az[a] for a in range(len(S))]

    #theta:right ascension
    #psi:right declination
    #lambda:longtitude
    #phi:latitude

    psi=[]
    theta=[]

    for j in range(N):

        if(x[j] != 0) and (y[j] != 0):
            psi.append((np.arctan(z[j]/np.sqrt(x[j]**2+y[j]**2)))/np.pi*180)
        elif ( z[j] > 0 ) and (x[j] == 0) and ( y[j] == 0 ) :
            psi.append(90)
        elif (z[j] < 0) and (x[j]==0) and (y[j] ==0) :
            psi.append(-90)

        if x[j]>0 :

            theta.append((np.arctan(y[j]/x[j]))/np.pi*180)

        elif (x[j]<0) and (y[j] >=0) :
            theta.append(180+(np.arctan(y[j]/x[j]))/np.pi*180)

        elif (x[j]<0) and (y[j]<=0) :
            theta.append(-180+(np.arctan(y[j]/x[j]))/np.pi*180)

        elif (x[j]==0) and (y[j]>0)  :
            theta.append(90)

        elif (x[j]==0) and (y[j]<0)  :
            theta.append(-90)


    phi=psi


    G = [G0 + (w_e*(t[c]-t0))/np.pi*180 for c in range(len(t))]  #time t, position of greenwich longtitude

    l = [theta[d] - G[d] for d in range(len(theta))]

    for i2 in range(N):
        while(l[i2] < -180):
            l[i2]=360+l[i2]

    h  = [np.sqrt(x[a]**2+y[a]**2+z[a]**2)-6370000 for a in range(len(y))]

    # output*************************************************
    #SatelliteOrbit:four rows, first row as t?second row as longtitude?third
    #row as latitude,forth row as height(distance between earth center minus
    #earth radius)

    #*********************************************************
    SatelliteOrbit = [t, l, phi, h]

    plt.figure()
    plt.plot(l, phi)
    plt.xlabel('l')
    plt.ylabel('p')
    plt.show()


x = OrbitLiveCalculator(1000000,0.4,57,12,48,60000,10)
