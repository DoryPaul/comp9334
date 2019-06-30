import random
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import stats

def simulation(mode, arrival, service, network, fogTimeLimit, fogTimeToCloudTime, time_end, num,seed_list):
    mrt_list = []
    if mode == 'trace':
        arrival_time_at_fog = arrival[0]
        temp_arrival = arrival.copy()[1:]

        next_arrival_at_fog = arrival_time_at_fog
        next_departure_from_fog_without_cloud = 99999999
        next_departure_from_fog_with_cloud = 99999999
        next_departure_from_network = 99999999
        next_departure_from_cloud = 99999999

        job_list_at_fog = []
        job_list_at_network = []
        job_dict_at_network = {}
        job_list_at_cloud = []
        job_dict_at_cloud = {}
        fog_departure = []
        network_departure = []
        cloud_departure = []
        master_clock = 0
        totalResponseTime = 0
        totalNumberOfJobsCompleted = 0
        x_list = []
        y_list = []
        while min(next_arrival_at_fog, next_departure_from_fog_without_cloud, next_departure_from_fog_with_cloud,
                  next_departure_from_network, next_departure_from_cloud) != 99999999:
            master_clock_previous = master_clock
            master_clock = min(next_arrival_at_fog, next_departure_from_fog_without_cloud,
                               next_departure_from_fog_with_cloud,
                               next_departure_from_network, next_departure_from_cloud)
            if master_clock == next_arrival_at_fog:
                remaining_travel_time = 0
                remaining_service_time_at_cloud = 0
                for i in range(len(job_list_at_fog)):
                    job_list_at_fog[i][1] = round(
                        job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog), 6)
                if len(temp_arrival) !=0:
                    next_arrival_at_fog = temp_arrival[0]
                    temp_arrival = temp_arrival.copy()[1:]
                else:
                    next_arrival_at_fog = 99999999
                if len(service) != 0:
                    remaining_service_time_at_fog = service[0]
                    service = service.copy()[1:]
                else:
                    remaining_service_time_at_fog = 99999999
                if remaining_service_time_at_fog > fogTimeLimit:
                    job_list_at_fog.append([master_clock, fogTimeLimit, True])
                    if len(network) != 0:
                        remaining_travel_time = network[0]
                        network = network.copy()[1:]
                    else:
                        remaining_travel_time = 99999999
                    remaining_service_time_at_cloud = round(
                        fogTimeToCloudTime * (remaining_service_time_at_fog - fogTimeLimit), 6)
                else:
                    job_list_at_fog.append([master_clock, remaining_service_time_at_fog, False])
                    network = network[1:]
                min_time1 = 99999999
                min_time2 = 99999999
                for i in range(len(job_list_at_fog)):
                    if job_list_at_fog[i][1] < min_time1 and job_list_at_fog[i][2] == True:
                        min_time1 = job_list_at_fog[i][1]
                    if job_list_at_fog[i][1] < min_time2 and job_list_at_fog[i][2] == False:
                        min_time2 = job_list_at_fog[i][1]
                if round(master_clock + min_time1 * len(job_list_at_fog), 6) < 99999999:
                    next_departure_from_fog_with_cloud = round(master_clock + min_time1 * len(job_list_at_fog), 6)
                if round(master_clock + min_time2 * len(job_list_at_fog), 6) < 99999999:
                    next_departure_from_fog_without_cloud = round(master_clock + min_time2 * len(job_list_at_fog),
                                                                  6)
                job_dict_at_network[master_clock] = remaining_travel_time
                job_dict_at_cloud[master_clock] = remaining_service_time_at_cloud

                if len(job_list_at_network) != 0:
                    for i in range(len(job_list_at_network)):
                        job_list_at_network[i][1] = round(
                            job_list_at_network[i][1] - (master_clock - master_clock_previous), 6)
                if len(job_list_at_cloud) != 0:
                    for i in range(len(job_list_at_cloud)):
                        job_list_at_cloud[i][1] = round(
                            job_list_at_cloud[i][1] - (master_clock - master_clock_previous) / len(
                                job_list_at_cloud),
                            6)
            if master_clock == next_departure_from_fog_without_cloud:
                flag = False
                next_departure_from_fog_without_cloud = 99999999
                temp_job_list_at_fog = []
                for i in range(len(job_list_at_fog)):
                    if round(job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog),
                             6) > 0:
                        job_list_at_fog[i][1] = round(
                            job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog),
                            6)
                        temp_job_list_at_fog.append(job_list_at_fog[i])
                    else:

                        fog_departure.append([job_list_at_fog[i][0], master_clock])
                        totalResponseTime += master_clock - job_list_at_fog[i][0]
                job_list_at_fog = temp_job_list_at_fog
                for j in range(len(job_list_at_network)):
                    job_list_at_network[j][1] = round(
                        job_list_at_network[j][1] - (master_clock - master_clock_previous), 6)
                for n in range(len(job_list_at_cloud)):
                    job_list_at_cloud[n][1] = round(
                        job_list_at_cloud[n][1] - (master_clock - master_clock_previous) / len(job_list_at_cloud),
                        6)

                min_time = 999999
                for i in range(len(job_list_at_fog)):
                    if job_list_at_fog[i][1] < min_time:
                        min_time = job_list_at_fog[i][1]
                        flag = job_list_at_fog[i][2]
                if flag == True:
                    next_departure_from_fog_with_cloud = round(master_clock + min_time * len(job_list_at_fog), 6)
                elif flag == False and len(job_list_at_fog) != 0:
                    next_departure_from_fog_without_cloud = round(master_clock + min_time * len(job_list_at_fog), 6)

                totalNumberOfJobsCompleted += 1
            if master_clock == next_departure_from_fog_with_cloud:
                flag = False
                next_departure_from_fog_with_cloud = 99999999
                for j in range(len(job_list_at_network)):
                    job_list_at_network[j][1] = round(
                        job_list_at_network[j][1] - (master_clock - master_clock_previous), 6)
                for n in range(len(job_list_at_cloud)):
                    job_list_at_cloud[n][1] = round(
                        job_list_at_cloud[n][1] - (master_clock - master_clock_previous) / len(job_list_at_cloud),
                        6)
                temp_job_list_at_fog = []
                for i in range(len(job_list_at_fog)):
                    if round(job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog),
                             6) > 0:
                        job_list_at_fog[i][1] = round(
                            job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog),
                            6)
                        temp_job_list_at_fog.append(job_list_at_fog[i])
                    else:
                        job_list_at_network.append(
                            [job_list_at_fog[i][0], job_dict_at_network[job_list_at_fog[i][0]]])
                        fog_departure.append([job_list_at_fog[i][0], master_clock])
                job_list_at_fog = temp_job_list_at_fog
                min_time = 999999
                for i in range(len(job_list_at_fog)):
                    if job_list_at_fog[i][1] < min_time:
                        min_time = job_list_at_fog[i][1]
                        flag = job_list_at_fog[i][2]
                if flag == True:
                    next_departure_from_fog_with_cloud = round(master_clock + min_time * len(job_list_at_fog), 6)
                elif flag == False and len(job_list_at_fog) != 0:
                    next_departure_from_fog_without_cloud = round(master_clock + min_time * len(job_list_at_fog), 6)
                min_network_time = 999999
                for i in range(len(job_list_at_network)):
                    if job_list_at_network[i][1] < min_network_time:
                        min_network_time = job_list_at_network[i][1]
                next_departure_from_network = round(master_clock + min_network_time, 6)
            if master_clock == next_departure_from_network:
                next_departure_from_network = 99999999
                for i in range(len(job_list_at_fog)):
                    job_list_at_fog[i][1] = round(
                        job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog), 6)
                for n in range(len(job_list_at_cloud)):
                    job_list_at_cloud[n][1] = round(
                        job_list_at_cloud[n][1] - (master_clock - master_clock_previous) / len(job_list_at_cloud),
                        6)
                temp_job_list_at_network = []
                min_network_time = 99999999
                for j in range(len(job_list_at_network)):
                    if round(job_list_at_network[j][1] - (master_clock - master_clock_previous), 6) > 0:
                        job_list_at_network[j][1] = round(
                            job_list_at_network[j][1] - (master_clock - master_clock_previous), 6)
                        temp_job_list_at_network.append(job_list_at_network[j])
                        if job_list_at_network[j][1] < min_network_time:
                            min_network_time = job_list_at_network[j][1]
                    else:
                        network_departure.append([job_list_at_network[j][0], master_clock])
                        job_list_at_cloud.append(
                            [job_list_at_network[j][0], job_dict_at_cloud[job_list_at_network[j][0]]])
                job_list_at_network = temp_job_list_at_network
                next_departure_from_network = round(master_clock + min_network_time, 6)
                min_cloud_time = 999999
                for i in range(len(job_list_at_cloud)):
                    if job_list_at_cloud[i][1] < min_cloud_time:
                        min_cloud_time = job_list_at_cloud[i][1]
                if len(job_list_at_cloud) != 0:
                    next_departure_from_cloud = round(master_clock + min_cloud_time * len(job_list_at_cloud), 6)
            if master_clock == next_departure_from_cloud:
                next_departure_from_cloud = 99999999
                for i in range(len(job_list_at_fog)):
                    job_list_at_fog[i][1] = round(
                        job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog), 6)
                for j in range(len(job_list_at_network)):
                    job_list_at_network[j][1] = round(
                        job_list_at_network[j][1] - (master_clock - master_clock_previous), 6)
                temp_job_list_at_cloud = []
                min_cloud_time = 99999999
                for n in range(len(job_list_at_cloud)):
                    if round(job_list_at_cloud[n][1] - (master_clock - master_clock_previous) / len(
                            job_list_at_cloud),
                             6) > 0:
                        job_list_at_cloud[n][1] = round(
                            job_list_at_cloud[n][1] - (master_clock - master_clock_previous) / len(
                                job_list_at_cloud),
                            6)
                        temp_job_list_at_cloud.append(job_list_at_cloud[n])
                        if job_list_at_cloud[n][1] < min_cloud_time:
                            min_cloud_time = job_list_at_cloud[n][1]
                    else:
                        cloud_departure.append([job_list_at_cloud[n][0], master_clock])

                        totalResponseTime += master_clock - job_list_at_cloud[n][0]
                        totalNumberOfJobsCompleted += 1
                job_list_at_cloud = temp_job_list_at_cloud
                if len(job_list_at_cloud) != 0:
                    next_departure_from_cloud = round(master_clock + min_cloud_time * len(job_list_at_cloud), 6)
            #print(master_clock, next_arrival_at_fog, next_departure_from_fog_with_cloud,
                #next_departure_from_fog_without_cloud,
                #next_departure_from_network, next_departure_from_cloud, job_list_at_fog, job_list_at_network,
                #job_list_at_cloud)
        if totalNumberOfJobsCompleted != 0:
            mean_response_time = round(totalResponseTime / totalNumberOfJobsCompleted, 4)
        else:
            mean_response_time = 0
        print(mean_response_time)



        f = open('fog_dep_' + str(num) + '.txt', 'w')
        fog_departure_list = sorted(fog_departure, key=lambda x: x[0])
        for key in fog_departure_list:
            f.write(str(round(key[0], 4)) + "\t" + str(round(key[1], 4)) + '\n')

        f1 = open('net_dep_' + str(num)  + '.txt', 'w')
        network_departure_list = sorted(network_departure, key=lambda x: x[0])
        for key in network_departure_list:
            f1.write(str(round(key[0], 4)) + "\t" + str(round(key[1], 4)) + '\n')

        f2 = open('cloud_dep_' + str(num)  + '.txt', 'w')
        cloud_departure_list = sorted(cloud_departure, key=lambda x: x[0])
        for key in cloud_departure_list:
            f2.write(str(round(key[0], 4)) + "\t" + str(round(key[1], 4)) + '\n')

        f4 = open('mrt_' + str(num)  + '.txt', 'w')
        f4.write(str(mean_response_time) + '\n')
    else:
        for seed_i in range(len(seed_list)):
            random.seed(seed_list[seed_i])
            lamda = arrival[0]
            a1 = service[0]
            a2 = service[1]
            beta = service[2]
            v1 = network[0]
            v2 = network[1]
            gama = (1 - beta) / ((a2 ** (1 - beta)) - (a1 ** (1 - beta)))

            #arrival_time_at_fog = round(random.expovariate(lamda), 6)
            u = random.expovariate(lamda)
            arrival_time_at_fog = round(u, 6)
            

            next_arrival_at_fog = arrival_time_at_fog
            next_departure_from_fog_without_cloud = 99999999
            next_departure_from_fog_with_cloud = 99999999
            next_departure_from_network = 99999999
            next_departure_from_cloud = 99999999

            job_list_at_fog = []
            job_list_at_network = []
            job_dict_at_network = {}
            job_list_at_cloud = []
            job_dict_at_cloud = {}
            fog_departure = []
            network_departure = []
            cloud_departure = []
            master_clock = 0
            totalResponseTime = 0
            totalNumberOfJobsCompleted = 0
            x_list = []
            y_list = []
            
            while min(next_arrival_at_fog, next_departure_from_fog_without_cloud, next_departure_from_fog_with_cloud,
                      next_departure_from_network, next_departure_from_cloud) <= time_end:
                master_clock_previous = master_clock
                master_clock = min(next_arrival_at_fog, next_departure_from_fog_without_cloud,
                                   next_departure_from_fog_with_cloud,
                                   next_departure_from_network, next_departure_from_cloud)
                if master_clock == next_arrival_at_fog:
                    remaining_travel_time = 0
                    remaining_service_time_at_cloud = 0
                    for i in range(len(job_list_at_fog)):
                        job_list_at_fog[i][1] = round(
                            job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog), 6)
                    
                    prob = random.uniform(0, 1)
                    remaining_service_time_at_fog = round((prob * (1 - beta) / gama + a1 ** (1 - beta)) ** (1 / (1 - beta)),
                                                          6)

                    if remaining_service_time_at_fog > fogTimeLimit:
                        job_list_at_fog.append([master_clock, fogTimeLimit, True])
                        remaining_travel_time = round(random.uniform(v1, v2), 6)
                        remaining_service_time_at_cloud = round(
                            fogTimeToCloudTime * (remaining_service_time_at_fog - fogTimeLimit), 6)
                    else:
                        job_list_at_fog.append([master_clock, remaining_service_time_at_fog, False])
                    min_time1 = 99999999
                    min_time2 = 99999999
                    for i in range(len(job_list_at_fog)):
                        if job_list_at_fog[i][1] < min_time1 and job_list_at_fog[i][2] == True:
                            min_time1 = job_list_at_fog[i][1]
                        if job_list_at_fog[i][1] < min_time2 and job_list_at_fog[i][2] == False:
                            min_time2 = job_list_at_fog[i][1]
                    if round(master_clock + min_time1 * len(job_list_at_fog), 6) < 99999999:
                        next_departure_from_fog_with_cloud = round(master_clock + min_time1 * len(job_list_at_fog), 6)
                    if round(master_clock + min_time2 * len(job_list_at_fog), 6) < 99999999:
                        next_departure_from_fog_without_cloud = round(master_clock + min_time2 * len(job_list_at_fog), 6)
                    job_dict_at_network[master_clock] = remaining_travel_time
                    job_dict_at_cloud[master_clock] = remaining_service_time_at_cloud
                    u = random.expovariate(lamda)
                    random_num = round(u, 6)
                    #random_num = random.expovariate(lamda)
                    next_arrival_at_fog = round(master_clock + random_num, 6)

                    if len(job_list_at_network) != 0:
                        for i in range(len(job_list_at_network)):
                            job_list_at_network[i][1] = round(
                                job_list_at_network[i][1] - (master_clock - master_clock_previous), 6)
                    if len(job_list_at_cloud) != 0:
                        for i in range(len(job_list_at_cloud)):
                            job_list_at_cloud[i][1] = round(
                                job_list_at_cloud[i][1] - (master_clock - master_clock_previous) / len(job_list_at_cloud),
                                6)
                if master_clock == next_departure_from_fog_without_cloud:
                    flag = False
                    next_departure_from_fog_without_cloud = 99999999
                    temp_job_list_at_fog = []
                    for i in range(len(job_list_at_fog)):
                        if round(job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog),
                                 6) > 0:
                            job_list_at_fog[i][1] = round(
                                job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog), 6)
                            temp_job_list_at_fog.append(job_list_at_fog[i])
                        else:
                           
                            fog_departure.append([job_list_at_fog[i][0], master_clock])
                            totalResponseTime += master_clock - job_list_at_fog[i][0]
                    job_list_at_fog = temp_job_list_at_fog
                    for j in range(len(job_list_at_network)):
                        job_list_at_network[j][1] = round(
                            job_list_at_network[j][1] - (master_clock - master_clock_previous), 6)
                    for n in range(len(job_list_at_cloud)):
                        job_list_at_cloud[n][1] = round(
                            job_list_at_cloud[n][1] - (master_clock - master_clock_previous) / len(job_list_at_cloud), 6)

                    min_time = 999999
                    for i in range(len(job_list_at_fog)):
                        if job_list_at_fog[i][1] < min_time:
                            min_time = job_list_at_fog[i][1]
                            flag = job_list_at_fog[i][2]
                    if flag == True:
                        next_departure_from_fog_with_cloud = round(master_clock + min_time * len(job_list_at_fog), 6)
                    elif flag == False and len(job_list_at_fog) != 0:
                        next_departure_from_fog_without_cloud = round(master_clock + min_time * len(job_list_at_fog), 6)
                    
                    totalNumberOfJobsCompleted += 1
                if master_clock == next_departure_from_fog_with_cloud:
                    flag = False
                    next_departure_from_fog_with_cloud = 99999999
                    for j in range(len(job_list_at_network)):
                        job_list_at_network[j][1] = round(
                            job_list_at_network[j][1] - (master_clock - master_clock_previous), 6)
                    for n in range(len(job_list_at_cloud)):
                        job_list_at_cloud[n][1] = round(
                            job_list_at_cloud[n][1] - (master_clock - master_clock_previous) / len(job_list_at_cloud), 6)
                    temp_job_list_at_fog = []
                    for i in range(len(job_list_at_fog)):
                        if round(job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog),
                                 6) > 0:
                            job_list_at_fog[i][1] = round(
                                job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog), 6)
                            temp_job_list_at_fog.append(job_list_at_fog[i])
                        else:
                            job_list_at_network.append([job_list_at_fog[i][0], job_dict_at_network[job_list_at_fog[i][0]]])
                            fog_departure.append([job_list_at_fog[i][0], master_clock])
                    job_list_at_fog = temp_job_list_at_fog
                    min_time = 999999
                    for i in range(len(job_list_at_fog)):
                        if job_list_at_fog[i][1] < min_time:
                            min_time = job_list_at_fog[i][1]
                            flag = job_list_at_fog[i][2]
                    if flag == True:
                        next_departure_from_fog_with_cloud = round(master_clock + min_time * len(job_list_at_fog), 6)
                    elif flag == False and len(job_list_at_fog) != 0:
                        next_departure_from_fog_without_cloud = round(master_clock + min_time * len(job_list_at_fog), 6)
                    min_network_time = 999999
                    for i in range(len(job_list_at_network)):
                        if job_list_at_network[i][1] < min_network_time:
                            min_network_time = job_list_at_network[i][1]
                    next_departure_from_network = round(master_clock + min_network_time, 6)
                if master_clock == next_departure_from_network:
                    next_departure_from_network = 99999999
                    for i in range(len(job_list_at_fog)):
                        job_list_at_fog[i][1] = round(
                            job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog), 6)
                    for n in range(len(job_list_at_cloud)):
                        job_list_at_cloud[n][1] = round(
                            job_list_at_cloud[n][1] - (master_clock - master_clock_previous) / len(job_list_at_cloud), 6)
                    temp_job_list_at_network = []
                    min_network_time = 99999999
                    for j in range(len(job_list_at_network)):
                        if round(job_list_at_network[j][1] - (master_clock - master_clock_previous), 6) > 0:
                            job_list_at_network[j][1] = round(
                                job_list_at_network[j][1] - (master_clock - master_clock_previous), 6)
                            temp_job_list_at_network.append(job_list_at_network[j])
                            if job_list_at_network[j][1] < min_network_time:
                                min_network_time = job_list_at_network[j][1]
                        else:
                            network_departure.append([job_list_at_network[j][0], master_clock])
                            job_list_at_cloud.append(
                                [job_list_at_network[j][0], job_dict_at_cloud[job_list_at_network[j][0]]])
                    job_list_at_network = temp_job_list_at_network
                    next_departure_from_network = round(master_clock + min_network_time, 6)
                    min_cloud_time = 999999
                    for i in range(len(job_list_at_cloud)):
                        if job_list_at_cloud[i][1] < min_cloud_time:
                            min_cloud_time = job_list_at_cloud[i][1]
                    if len(job_list_at_cloud) != 0:
                        next_departure_from_cloud = round(master_clock + min_cloud_time * len(job_list_at_cloud), 6)
                if master_clock == next_departure_from_cloud:
                    next_departure_from_cloud = 99999999
                    for i in range(len(job_list_at_fog)):
                        job_list_at_fog[i][1] = round(
                            job_list_at_fog[i][1] - (master_clock - master_clock_previous) / len(job_list_at_fog), 6)
                    for j in range(len(job_list_at_network)):
                        job_list_at_network[j][1] = round(
                            job_list_at_network[j][1] - (master_clock - master_clock_previous), 6)
                    temp_job_list_at_cloud = []
                    min_cloud_time = 99999999
                    for n in range(len(job_list_at_cloud)):
                        if round(job_list_at_cloud[n][1] - (master_clock - master_clock_previous) / len(job_list_at_cloud),
                                 6) > 0:
                            job_list_at_cloud[n][1] = round(
                                job_list_at_cloud[n][1] - (master_clock - master_clock_previous) / len(job_list_at_cloud),
                                6)
                            temp_job_list_at_cloud.append(job_list_at_cloud[n])
                            if job_list_at_cloud[n][1] < min_cloud_time:
                                min_cloud_time = job_list_at_cloud[n][1]
                        else:
                            cloud_departure.append([job_list_at_cloud[n][0], master_clock])
                            
                            totalResponseTime += master_clock - job_list_at_cloud[n][0]
                            totalNumberOfJobsCompleted += 1
                    job_list_at_cloud = temp_job_list_at_cloud
                    if len(job_list_at_cloud) != 0:
                        next_departure_from_cloud = round(master_clock + min_cloud_time * len(job_list_at_cloud), 6)
                #print(master_clock, next_arrival_at_fog, next_departure_from_fog_with_cloud,
                      #next_departure_from_fog_without_cloud,
                      #next_departure_from_network, next_departure_from_cloud, job_list_at_fog, job_list_at_network,
                      #job_list_at_cloud)
            mean_response_time = round(totalResponseTime / totalNumberOfJobsCompleted,4)
            print(mean_response_time)
            f = open('fog_dep_' + str(num)+'_'+str(seed_i+1)+'.txt', 'w')
            fog_departure_list = sorted(fog_departure, key=lambda x: x[0])
            for key in fog_departure_list:
                f.write(str(round(key[0],4)) + "\t" + str(round(key[1],4)) + '\n')

            f1 = open('net_dep_' + str(num) + '_'+str(seed_i+1)+'.txt', 'w')
            network_departure_list = sorted(network_departure, key=lambda x: x[0])
            for key in network_departure_list:
                f1.write(str(round(key[0],4)) + "\t" + str(round(key[1],4)) + '\n')

            f2 = open('cloud_dep_' + str(num) +'_'+str(seed_i+1)+'.txt', 'w')
            cloud_departure_list = sorted(cloud_departure, key=lambda x: x[0])
            for key in cloud_departure_list:
                f2.write(str(round(key[0],4)) + "\t" + str(round(key[1],4)) + '\n')

            f4 = open('mrt_' + str(num) + '_'+str(seed_i+1)+'.txt', 'w')
            f4.write(str(mean_response_time) + '\n')   
    


arrival = [9.720]
service = [0.01, 0.3, 0.86]
network = [1.2, 1.47]
fogTimeLimit = 0.1
fogTimeToCloudTime = 0.6
time_end = 1000
seed_list = [123,12346,2346,32,4667,3642,6678,4321,87664,66843]
#simulation('random', arrival, service, network, fogTimeLimit, fogTimeToCloudTime, time_end, 0,129498)
