
"""***
    Event.py
***"""
import math
import random
import Queue
import simpy

#MAXBUFFEE[2] = [1,20,50]

def main():

    '''initializing length = # of packets in the queue'''
    '''time is the current time'''

    #rate[6] =[0.1,0.25,0.4,0.55,0.65,0.8,0.9]

    print("Enter the rate?")
    arrival_rate = raw_input()
    print("Enter the MAXBUFFER size?(-1 for infinite)")
    MAXBUFFER = raw_input()

    #lamda = [0.1,0.25,0.4,0.55,0.65,0.8,0.9] when the buffer size is infinite
    #lamda = [0.2, 0.4, 0.6, 0.8, 0.9] when MAXBUFFER = 1, 20, and 50
    arrival_Interval = neg_exp_dist_time(arrival_rate)

    #miu = 1 packet/second

    packet_drop = 0
    env = simpy.Environment()
    current_time = env.now

    arrival_event = Event(current_time)  #first arrival event
    next_arrival_time = current_time + arrival_Interval

    newpacket = Packet(neg_exp_dist_time(1))
    #Insert the event into the event list.



    #arrival_event = Event()
    #departure_event = Event()

    q = Queue.Queue()


    '''
    for i in range():
        q.put(i)
    '''
    length = Queue.qsize()


    if MAXBUFFER > 0:
        if q.empty():
            #transmission_time = newpacket.getTime()
            departure_event= Event(current_time + newpacket.getTime())
             #Insert the event at the right place in GEL
        elif length-1<MAXBUFFER:
            q.put(newpacket)
        else:
            packet_drop += 1
    else:
        if q.empty():
            #transmission_time = newpacket.getTime()
            departure_event= Event(current_time + newpacket.getTime())
             #Insert the event at the right place in GEL
        else:
            q.put(newpacket)
    #queue in here!



'''Packet Class'''
class Packet:
    def __init__(self,time):
        self.time = time
        return time
    def getTime():
        return time


'''Event Class'''
class Event:
    def __init__(self, time):
        self.time = time
        return self

    def getTime():
        return time




def departure_event(length):
    if length == 0:

    elif length > 0:
        q.get()
        #new departure event!
        departure_event= Event(current_time + transmission_time)
        #Insert the event at the right place in GEL

def neg_exp_dist_time(rate):
     u = random.uniform(0,1);
     return ((-1/rate)*math.log(1-u));
