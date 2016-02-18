
"""***
	Event.py
***"""
import math
import random

time = 0;

def nega_exp_dist_time(rate):
     u = random.uniform(0,1);
     return ((-1/rate)*math.log(1-u));


class wow:
