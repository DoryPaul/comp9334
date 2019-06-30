import matplotlib
from matplotlib import pyplot as plt
p1 = 0.25
array1 = []
array2 = []
minnum = 100
minlist = []
for i in range(249):
    p1 += 0.001
    p2 = 1-p1
    
    e1 = p1/(10*(1-(20*p1/10)))
    e2 = p2/(15*(1-(20*p2/15)))
    
    e = e1+e2
    array1.append(p1)
    array2.append(e)

for j in range(len(array1)):
    if min(array2) == array2[j]:
        print(array1[j],array2[j])
plt.plot(array1,array2)
plt.show()
