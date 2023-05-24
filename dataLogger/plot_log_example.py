

import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import dateutil.parser
import glob


log_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(log_dir)

header = 'center_freq_power' # When the data file's name are such as center_freq_power-20180407-213401.csv
start_date = 20180406
end_date = 20180408


log_file_list = glob.glob(header+'*')
data_file_list = []


for each_name in log_file_list:
    date = int(each_name[len(header)+1:len(header)+1+8])
    if (start_date <= date) and (date <= end_date):
        data_file_list.append(each_name)

data = []
for each_file in data_file_list:
    with open(each_file, 'r') as f:
        reader = csv.reader(f)
        new_data = list(reader)
    #print(new_data, '\n\n')

    # del new_data[0] # In case the first line is a header
    if (len(new_data[0]) != 3): # In case the parsed result of first list has different number of elements
        print('The first line of %s will be removed: %s' % (each_file, new_data[0]))
        del new_data[0]
    else:
        try:
            dateutil.parser.parse(new_data[0][0]) # Check if the first element is date and time information
        except ValueError:
            print('The first line of %s will be removed: %s' % (each_file, new_data[0]))
            del new_data[0]
        
    data += new_data



print ("Total data:", len(data))

# Transpose the data
temp = list(map(list, zip(*data)))

date_list = list(map(dateutil.parser.parse, temp[0]))
freq_list = list(map(float, temp[1]))
power_list = list(map(float, temp[2]))

plt.rcParams.update({'figure.autolayout': True})


##################################################################
# Example for multiple plots (heterogeneous-type data)
##################################################################
fig = plt.figure(67)
freq_axes = fig.add_subplot(2, 1, 1)
power_axes = fig.add_subplot(2, 1, 2)

# Subplot for center frequency
freq_axes.cla() # In case the previous plot still remains in the given axes. Especially when the figure with the same fig_number is used
freq_axes.plot(date_list, freq_list)
freq_axes.set(xlabel='Time', ylabel='Frequency (THz)',
       title='Drift of center frequency')
labels = freq_axes.get_xticklabels()
plt.setp(labels, rotation=45, horizontalalignment='right')

# Subplot for maximum power
power_axes.cla() # In case the previous plot still remains in the given axes. Especially when the figure with the same fig_number is used
power_axes.plot(date_list, power_list)
power_axes.set(xlabel='Time', ylabel='Power (dBm)',
       title='Change of maximum power')
labels = power_axes.get_xticklabels()
plt.setp(labels, rotation=45, horizontalalignment='right')
##################################################################




##################################################################
# Example for multi-channel data (homogeneous type)
##################################################################
data_list = [freq_list, power_list]
label_list = ('Center frequency', 'Power')

fig = plt.figure(68)
axes = fig.add_subplot(1, 1, 1)
axes.cla() # In case the previous plot still remains in the given axes. Especially when the figure with the same fig_number is used

l=[]
for i in range(len(label_list)):
    l.append(axes.plot(date_list, data_list[i], label= label_list[i]))
axes.legend()
labels = axes.get_xticklabels()
plt.setp(labels, rotation=45, horizontalalignment='right')

axes.set(xlabel='Time', ylabel='Power (dBm) and center frequency (THz)',
       title='Drift of peak')

#fig.legend(handles=[l[0], l[1], l[2], l[3], l[4], l[5]], labels=['ch0', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5'])#, 'upper right')
#axes.set_yticks(range(0, 221, 10))
#axes.set_ylim([25,100])
axes.grid()
##################################################################


