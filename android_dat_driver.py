# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 14:47:58 2023

@author: nabil
"""

# driver script
from utils.AndroidDat import AndroidDat
from utils.utils_class import read_dat
import pandas as pd

# global variables
#
fname = "data\week_1.csv"
start_date = pd.to_datetime('2023-06-05')
end_date = pd.to_datetime('2023-06-25')
target_count = 2500

# get the filtered dat
#
dat = read_dat(fname, start_date, end_date, target_count)
print(dat.filtered_df.head())
# plot and save the daily step target met chart
#
# figure = dat.plot_step_target()
# figure.write_image("step_target.png",  width=400, height=400, scale=3)
# figure.write_image("step_target.svg",  width=400, height=400, scale=3)

# 