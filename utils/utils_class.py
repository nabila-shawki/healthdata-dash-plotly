# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 11:43:14 2023

@author: nabil
"""

from utils.AndroidDat import AndroidDat

# read and filter the data for further processing
#
def read_dat(fname, start_date, end_date, target_count):
    
    android_dat = AndroidDat(fname)
    android_dat.read_dat()
    android_dat.filter_dates(start_date, end_date)
    android_dat.drop_nan_columns()
    android_dat.remove_zero_columns()
    android_dat.convert_units()
    android_dat.assign_week_num()
    android_dat.find_target_met(target_count)
    
    return android_dat   
#
# end of method

