import proj
import randommode
import random
import matplotlib.pyplot as plt
import confidenceinterval
f = open("num_tests.txt")
num_tests = 0
#seed_list = [80,100,150,200,250,300,350,600,1234,500]
#seed_list=[400]
random.seed(135)
seed_list = random.sample(range(100,5000),5)
for line in f.readlines():
    num_tests = int(line)

for i in range(num_tests):
    mode = ''
    fogTimeLimit = 0
    fogTimeToCloudTime = 0
    para_list = []
    arrival = []
    service = []
    network = []
    num = i+1
    time_end = 0
    
    f = open("mode_"+str(num)+".txt")
    for line in f.readlines():
        mode = line
        
    f1 = open("para_"+str(num)+".txt")
    for line in f1.readlines():
        para_list.append(line)
    fogTimeLimit = float(para_list[0])
    fogTimeToCloudTime = float(para_list[1])
    if mode == 'random':
        time_end = float(para_list[2])
    
    f2 = open("arrival_"+str(num)+".txt")
    for line in f2.readlines():
        arrival.append(float(line.strip('\n')))

    f3 = open("service_"+str(num)+".txt")
    for line in f3.readlines():
        service.append(float(line.strip('\n')))

    f4 = open("network_"+str(num)+".txt")
    for line in f4.readlines():
        network.append(float(line.strip('\n')))
    time_list = []
    mean_list = []
    con_list = []
    if mode == 'random':
        time_end = float(para_list[2])
        result = proj.simulation(mode,arrival,service,network,fogTimeLimit,fogTimeToCloudTime,time_end,num,seed_list)
    else:
        result = proj.simulation(mode,arrival,service,network,fogTimeLimit,fogTimeToCloudTime,time_end,num,seed_list)
    print()

###test for replications###
random.seed(10)
seed_list = random.sample(range(1000,5000),5)
arrival = [9.72]
service = [0.01,0.4,0.86]
network = [1.2,1.47]
fogTimeLimit = 0.1
fogTimeToCloudTime = 0.6
time_end = 1000
num = 100
###replications###
result = proj.simulation("random",arrival,service,network,fogTimeLimit,fogTimeToCloudTime,time_end,num,seed_list)


###draw the picture###
#result = randommode.simulation("random",arrival,service,network,fogTimeLimit,fogTimeToCloudTime,time_end,num,seed_list)


###calculate the confidence interval###
##start = 0.5
##for n in range(10):
##    fog = round(start+0.01*n,2)
##    result = confidenceinterval.simulation("random",arrival,service,network,fog,fogTimeToCloudTime,time_end,num,seed_list)

