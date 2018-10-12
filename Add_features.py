# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 16:03:15 2018

@author: Sateesh
"""

import pandas as pd

dataset = pd.read_excel('dataset.xlsx')
#%%
''' Methods/ Engineered Features'''

def column_identifier(string):
    for i in range(len(dataset.columns)):
        if dataset.columns[i]== string:
            return i

def exp_date_match(row):
    curr_date = row[column_identifier('Date')]
    curr_time = row[column_identifier('End_Time')]
    caller_exp_date = row[column_identifier('Expiry Date(caller)')]
    caller_exp_time = row[column_identifier('Expiry Time(caller)')]
    receiver_exp_date = row[column_identifier('Expiry Date(receiver)')]
    receiver_exp_time = row[column_identifier('Expiry Time(receiver)')]
    
    return int((receiver_exp_time == curr_time and receiver_exp_date == curr_date) or (caller_exp_time == curr_time and caller_exp_date == curr_date))

        
def timing_advance(row):
    caller_ta = row[column_identifier('TA(caller)')]
    caller_talim = row[column_identifier('TALIM(caller)')]
    rec_ta = row[column_identifier('TA(receiver)')]
    rec_talim = row[column_identifier('TALIM(receiver)')]
    
    return int((caller_ta > caller_talim) or (rec_ta > rec_talim))

def duration_limit(row):
    dur = row[column_identifier('Call Duration')]
    
    return int(dur == 90)
    
def bts_condition_impact(row):
    cond_caller = row[column_identifier('BTS Condition(Caller)')]
    rec_caller = row[column_identifier('BTS Condition(Receiver)')]
    caller_sig_strength = row[column_identifier('Signal Strength(caller)')]
    rec_sig_strength = row[column_identifier('Signal Strength(receiver)')]
    caller_distance = row[column_identifier('Distance(caller)')]
    rec_distance = row[column_identifier('Distance(receiver)')]
    
    return int((cond_caller==1 and caller_sig_strength==4 and (caller_distance<300 or caller_distance>800)) or (rec_caller==1 and rec_sig_strength==4 and (rec_distance<300 or rec_distance>800)))

def handover_check(row):
    caller_sig_strength = row[column_identifier('Signal Strength(caller)')]
    rec_sig_strength = row[column_identifier('Signal Strength(receiver)')]
    caller_distance = row[column_identifier('Distance(caller)')]
    rec_distance = row[column_identifier('Distance(receiver)')]
    caller_cell_chg = row[column_identifier('Change Of Cell(caller)')]
    rec_cell_chg = row[column_identifier('Change Of Cell(receiver)')]
    
    return int((caller_cell_chg==0 and caller_sig_strength==4 and (caller_distance>900)) or (rec_cell_chg==0 and rec_sig_strength==4 and rec_distance>900))

def traffic_sms_int(row):
    caller_traffic = row[column_identifier('Traffic(caller)')]
    rec_traffic = row[column_identifier('Traffic(receiver)')]
    caller_internet = row[column_identifier('Internet(Caller)')]
    rec_internet = row[column_identifier('Internet(receiver)')]
    caller_sms = row[column_identifier('SMS(caller)')]
    rec_sms = row[column_identifier('SMS(receiver)')]
    
    return int((caller_traffic>400 and caller_internet==1 and caller_sms==1) or (rec_traffic>400 and rec_internet==1 and rec_sms==1))

def underground(row):
    caller_elev = row[column_identifier('Elevation(caller)')]
    rec_elev = row[column_identifier('Elevation(receiver)')]
    caller_sig = row[column_identifier('Signal Strength(caller)')]
    rec_sig = row[column_identifier('Signal Strength(receiver)')]
    
    return int((caller_elev<0 and caller_sig==4) or (rec_elev<0 and rec_sig==4))

def drop_status(row):
    if row[-7] == row[-6] == row[-5] == row[-4] == row[-3] == row[-2] == row[-1] == 0:
        return 'Normal'
    
    else:
        return 'Dropped'
#%%
'''Create feature columns'''

dataset['Expiry Match'] = dataset.apply(exp_date_match, axis = 1)
dataset['TALIM Exceeded'] = dataset.apply(timing_advance, axis = 1)
dataset['duration exceeded'] = dataset.apply(duration_limit, axis = 1)
dataset['Condition Impact'] = dataset.apply(bts_condition_impact, axis = 1)
dataset['Handover Check'] = dataset.apply(handover_check, axis = 1)
dataset['Traffic,sms,int'] = dataset.apply(traffic_sms_int, axis = 1)
dataset['Weak Underground'] = dataset.apply(underground, axis = 1)
    
dataset['Status'] = dataset.apply(drop_status, axis = 1)
#%%
dataset['Date'] = dataset['Date'].apply(lambda row: row.date())
dataset['Expiry Date(receiver)'] = dataset['Expiry Date(receiver)'].apply(lambda row: row.date())
dataset['Expiry Date(caller)'] = dataset['Expiry Date(caller)'].apply(lambda row: row.date())
dataset['IMEI (Caller)'] = dataset['IMEI (Caller)'].apply(lambda row: str(row))
dataset['IMEI (Receiver)'] = dataset['IMEI (Receiver)'].apply(lambda row: str(row))
#%%
dataset.to_excel('training_data.xlsx', index = False)