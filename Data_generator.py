# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 11:42:46 2018

@author: Sateesh

"""
number_of_samples = 100
urban_rural = 'urban'
#%% 
'''Caller Data Generation'''

import random 
from datetime import datetime, date, time
import pandas as pd

random.seed(1)  # Set Random Seed

dat = [datetime(2018,7,12).date()]*number_of_samples
start_time = [time(8,21,0)]*int(number_of_samples*0.5) +  [time(8,22,0)]*int(number_of_samples*0.5 )
end_time_range1 = pd.date_range('08:21:00', periods=90, freq='T').time
end_time_range2 = pd.date_range('08:22:00', periods=90, freq='T').time
end_time1 = [random.choice(end_time_range1) for i in range(int(number_of_samples*0.5))]
end_time2 = [random.choice(end_time_range2) for i in range(int(number_of_samples*0.5))]
end_time = end_time1 + end_time2

duration = [(datetime.combine(date.min,end_time[i]) -datetime.combine(date.min,start_time[i])).seconds/60 for i in range(number_of_samples)]

cell = [(random.randint(12000, 33000))]*number_of_samples
cond = [random.choice([0]*90 + [1]*10)]*number_of_samples
land = [random.randint(0,1)]*number_of_samples

imei  = [str(random.randint(100000000000000, 999999999999999)) for i in range(number_of_samples)]  # IMEI generation

humidity = [random.randint(70, 85)]*number_of_samples  # Humidity

if urban_rural == 'urban':
    traffic = [random.randint(100,500)]*number_of_samples  # Traffic handled by BTS
else:
    traffic = [random.randint(50,300)]*number_of_samples  # Traffic handled by BTS
    
elevation =  [random.randint(-20,40) for i in range(number_of_samples)]  # Elevation of caller wrt BTS
distance = [random.randint(20, 1020) for i in range(number_of_samples)] # Distance of caller from BTS

change_choice = [0]*76 + [1]*24  # Change Of Cell 
change = [random.choice(change_choice) for i in range(number_of_samples)]


signal_choice = [0]*10 + [1]*number_of_samples + [2]*30 + [3]*number_of_samples + [4]*10  # Signal Strength
signal = [random.choice(signal_choice) for i in range(number_of_samples)]

# Expiry Date
begin_date, end_date = datetime(2018, 7, 12), datetime(2019, 7, 12)
dates = pd.date_range(begin_date, end_date)
exp_date = [random.choice(dates).date() for i in range(number_of_samples)] 
    
#Expiry time
times = pd.date_range('00:00:00', periods=1440, freq='T').time
exp_time = [random.choice(times) for i in range(number_of_samples)]

internet = [random.randint(0,1) for i in range(number_of_samples)]  # Internet being used or not
sms_options = [1]*10 + [0]*90
sms = [random.choice(sms_options) for i in range(number_of_samples)]  # sms received/ not received

if urban_rural == 'urban':
    rlt = [(random.choice(list(range(20,36, 4))))]*number_of_samples  # radio link timeout
else:
    rlt = [(random.choice(list(range(36,64, 4))))]*number_of_samples
    
ta_lim_choice = [21,22,23,24,25,30,32,35,38,43,44,55,56]
ta_lim = [random.choice(ta_lim_choice)]*number_of_samples

ta_choice = list(range(20,ta_lim[0]+2))
ta = [random.choice(ta_choice) for i in range(number_of_samples)]  # Timing advance

#%%
''' Receiver Data Generation'''

random.seed(22)  # Set Random Seed

rec_cond_choice = [1]*10 + [0]*90  # Assuming 10% in bad condition 
rec_cond = [random.choice(rec_cond_choice) for i in range(number_of_samples)] # receiver BTS condition
rec_land = [random.randint(0,1) for i in range(0,number_of_samples)] # landscape

rec_imei  = [str(random.randint(100000000000000, 999999999999999)) for i in range(number_of_samples)] # IMEI

rec_humidity = [random.randint(70, 85) for i in range(number_of_samples)] # Humidity
rec_traffic = [random.randint(100,500) for i in range(number_of_samples)] # Traffic   
rec_elevation = [random.randint(-20,40) for i in range(number_of_samples)] # Elevation
rec_distance = [random.randint(20,1020) for i in range(number_of_samples)] # distance from BTS
rec_change = [random.choice(change_choice) for i in range(number_of_samples)] # change of cell  

rec_signal = [random.choice(signal_choice) for i in range(number_of_samples)]

# Expiry Date
rec_exp_date = [random.choice(dates).date() for i in range(number_of_samples)] 

#Expiry time
rec_exp_time = [random.choice(times) for i in range(number_of_samples)]

rec_internet = [random.randint(0,1) for i in range(number_of_samples)] # internet
rec_sms = [random.choice(sms_options) for i in range(number_of_samples)] # sms

rec_rlt = [random.choice(list(range(20,64,4))) for i in range(number_of_samples)] # Radio Link Timeout 

rec_cell = [random.randint(12000, 33000) for i in range(number_of_samples)]  # Cell_id of the receiver 

rec_ta_lim_choice = [21,22,23,24,25,30,32,35,38,43,44,55,56]
rec_ta_lim = [random.choice(ta_lim_choice) for i in range(number_of_samples)]


rec_ta = [random.choice(list(range(20,rec_ta_lim[i]+2))) for i in range(number_of_samples)]  # Timing advance

#%% 
'''Create Dataframe'''

import pandas as pd
from collections import OrderedDict

df = pd.DataFrame(OrderedDict((('Cell_id(caller)', cell),
                    ('BTS Condition(Caller)', cond),
                    ('Traffic(caller)', traffic),
                    ('BTS Condition(Receiver)', rec_cond),
                    ('Traffic(receiver)', rec_traffic),
                    ('Date', dat),
                    ('Start_Time', start_time),
                    ('End_Time', end_time),
                    ('IMEI (Caller)', imei),
                    ('Cell_id(receiver)', rec_cell),
                    ('IMEI (Receiver)', rec_imei),
                    ('Landscape(Caller)', land),    
                    ('Landscape(receiver)', rec_land),
                    ('Humidity(caller)', humidity),
                    ('Humidity(receiver)', rec_humidity),
                    ('Elevation(caller)', elevation),
                    ('Elevation(receiver)', rec_elevation),
                    ('Call Duration', duration),
                    ('Distance(caller)', distance),
                    ('Distance(receiver)', rec_distance),
                    ('Signal Strength(caller)', signal),
                    ('Signal Strength(receiver)',rec_signal),
                    ('Change Of Cell(caller)',change),
                    ('Change Of Cell(receiver)',rec_change),
                    ('Expiry Date(caller)', exp_date),
                    ('Expiry Date(receiver)', rec_exp_date),
                    ('Expiry Time(caller)', exp_time),
                    ('Expiry Time(receiver)', rec_exp_time),
                    ('Internet(Caller)', internet),
                    ('Internet(receiver)', rec_internet),
                    ('SMS(caller)', sms),
                    ('SMS(receiver)', rec_sms),
                    ('RLT(caller)', rlt), 
                    ('RLT(receiver)', rec_rlt),
                    ('TA(caller)', ta),
                    ('TA(receiver)', rec_ta),
                    ('TALIM(caller)', ta_lim),
                    ('TALIM(receiver)', rec_ta_lim)
                        )))

df.to_excel('dataset.xlsx', index = False)