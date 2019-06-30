from scipy.optimize import fsolve

def func(i):
     x, y, z ,m,n,o= i[0], i[1], i[2],i[3],i[4],i[5]
     a = 1/600
     b = 1/60
     c = 1/90
     return [
             #4*a*x - c*y - b*o,
             -4*a*x + (c+3*a)*y - b*z,
             -3*a*y +(b+c+2*a)*z -(b+c)*m - 3*a*o,
             -2*a*z + (a+b+c)*m - (b+c)*n,
             -a*m +(b+c)*n,
             -c*z + (3*a+b)*o,
             x+y+z+m+n+o-1
            
            ]

r = fsolve(func,[0, 0, 0,0,0,0])
print ('P(0,0,0):{},\nP(1,0,1):{},\nP(2,1,1):{},\nP(3,1,1):{},\nP(4,1,1):{},\nP(1,1,0):{}'.format(r[0],r[1],r[2],r[3],r[4],r[5]))
