
"""***
    Event.py
***"""
import math
import random
import Queue


def main():

    '''initializing length = # of packets in the queue'''
    '''time is the current time'''

    current_time
    length = 0
    transmit_time = 0

    arrival_event = Event()
    #departure_event = Event()


    current_time = arrival_event.getTime()


    q = Queue.Queue()



    for i in range():
        q.put(i)

    length = Queue.qsize()

    def tracking_queue_length():
        if length == 0:
        elif length > 0:
            q.pop()
            #new departure event!
            departure_event= Event(current_time + transmit_time)
            #Insert the event at the right place in GEL



    #queue in here!




class Event:

    time
    def __init__(self, time):
        self.time = time
        return self

    def getTime()
        return time

def nega_exp_dist_time(rate):
     u = random.uniform(0,1);
     return ((-1/rate)*math.log(1-u));
