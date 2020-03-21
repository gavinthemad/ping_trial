import os, time, sys, concurrent.futures, re
import subprocess as sub
import numpy as np
from statistics import mean

avg_loss_list = []
avg_delay_list = []
avg_delay = 0
avg_loss = 0
loss_100 = 0

def ping(ip):
    ping_cmd = str('ping ' + str(ip) + ' -c 60 -q')
    stream = os.popen(ping_cmd)
    stream_as_string = stream.read()
    all_times_list = re.findall('[0-9.]+/[0-9.]+/[0-9.]+/[0-9.]+', stream_as_string)

    avg_times = []
    losses = []
    
    for times in all_times_list:
        avg_time_start_index = times.find('/') + 1
        avg_time_end_offset = times[avg_time_start_index:].find('/')
        avg_time_end_index = avg_time_start_index + avg_time_end_offset
        avg_times.append(float(times[avg_time_start_index:avg_time_end_index]))

    avg_delay_list.append(mean(avg_times))

    all_loss_list = re.findall('[0-9]+% packet loss', stream_as_string)
    print(all_loss_list)
    for loss in all_loss_list:
        loss_end_index = loss.find('%')
        losses.append(float(loss[:loss_end_index]))

    avg_loss_list.append(mean(losses))
        

    
traceroute_cmd = str('traceroute -n ' + str(sys.argv[1]))

stream = os.popen(traceroute_cmd)

ip_list = re.findall('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', stream.read())
ip_list = list(dict.fromkeys(ip_list))



with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(ping, ip_list)

 
#print('average loss: ' + str(mean(avg_loss_list)))
#print('average delay: ' + str(mean(avg_delay_list)))

print('average losses:')
print(*avg_loss_list, sep = "\n")
print('\naverage delay:')
print(*avg_delay_list, sep = "\n")
