'''
Author: Sonal Ranjit

This script transforms a give time series to the frequency domain using the method of
Least Squares. The main concept here is to determine the coefficients of a sum of
sine and cosines functions that best fit the given time series.

The function to fit in the problem is: p(w_j) = c1*sin(2piw_jt)+c2*cos(2piw_jt).
The Least Squares solution to this is simply defined as:
c = inv(A'*A)*A'*l.
Where A is the first design matrix, which consists of partial derivatives of the
function model with respect to the unknowns, in this case they are c1 and c2.
l is the observation vector.
The coefficients are determined for every frequency spanning the time series.
So there are different coefficients c1 and c2 for every corresponding frequency w_j.
So the least squares solution has to be determined j times for each frequency.
Once all the functions are determined for every frequency spanning the time series.
They can be transformed into the frequency domain. The way this is done is by projecting
the vector of the newly determined p(w_j) onto the original time series. An orthogonal
projection of p onto l gives a measure of how much of p is contained in l. The better the
fit of p to the corresponding w, the higher the contribution is to the original time
series for that frequency.
The projection can be defined as s(w_j) = f'p/(f'f)
'''
from math import *
import numpy as np
import matplotlib.pyplot as plt

'''#test
t = np.linspace(0.001,0.119,200)
fq = np.linspace(1/min(t),1/max(t),1000)

y1 = 9.8*np.cos(2*pi*200*t[:]+0)
y2 = 7.6*np.cos((2*pi*145*t[:])+(30*(pi/180)))
y3 = 5.4*np.cos((2*pi*93*t[:])+(70*(pi/180)))
y4 = 3.2*np.cos((2*pi*58*t[:])+(160*(pi/180)))
y5 = np.cos((2*pi*35*t[:])+(320*(pi/180)))

l = y1+y2+y3+y4+y5'''

data = np.loadtxt('ALBH.dat')
t = np.array(data[:, 0])
l = np.array(data[:, 1])
fq = np.linspace(1/min(t), 1/max(t), len(t))
s = np.empty([len(fq), 1])
for i in range(len(fq)):
    A = []
    for j in t:
        a1 = sin(2*pi*fq[i]*j)
        a2 = cos(2*pi*fq[i]*j)
        amat = [a1, a2]
        A.append(amat)

    xhat = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A), A)), np.transpose(A)), l)
    lhat = np.dot(A, xhat)
    s1 = np.dot(np.transpose(l), lhat)
    s2 = 1/np.dot(np.transpose(l), l)
    ss = pow(np.dot(s1, s2), 2)
    s[i] = ss    
plt.figure(1)
plt.plot(fq, s, 'yo-')
plt.show()
