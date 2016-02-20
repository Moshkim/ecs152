
"""
***Event.py***
"""

import math
import random
from queue import *

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

    #miu = 1 packet/second

    packet_drop = 0
    current_time = 0
    q = Queue.Queue()
    length = Queue.qsize()
    GEL = DoubleList()
    transmission_Time = 0

    '''the first arrival event'''
    GEL.add((current_time + neg_exp_dist_time(arrival_rate)),True)

    for i in range(0, 100000):
        current_node = GEL.remove()
        current_time = current_node.getTime()
        if current_node.arrival == True:
            '''Process an arrival Event'''
            newpacket = Packet(neg_exp_dist_time(1))
            GEL.add((current_time + neg_exp_dist_time(arrival_rate)),True)

            if MAXBUFFER > 0:
                if q.empty():
                #transmission_time = newpacket.getTime()
                 #Insert the departure event at the right place in GEL
                    length += 1
                    GEL.add(current_time + newpacket.getTime(),False)

                elif length-1<MAXBUFFER:
                    q.put(newpacket)
                    length += 1

                else:
                    packet_drop += 1

            elif MAXBUFFER == -1:
                if q.empty():
                    length += 1
                    GEL.add(current_time + newpacket.getTime(),False)
                else:
                    q.put(newpacket)
                    length += 1

        elif current_node.arrival == False:
            transmission_Time += current_node.arrival.getTime()

            length -= 1
            if length == 0:
                continue
            elif length > 0:
                departure_node =  q.get()
                GEL.add(current_time + departure_node.getTime())

            #1. get the first event from the GEL;
            #2. If the event is an arrival then process-arrival-event;
            #3. Otherwise it must be a departure event and hence
            #process-service-completion;

            #output-statistics;
    print("current_time is: ",current_time)
    print("The number of the packet dropped is: ", packet_drop)
    print("Untilization time is: ",transmission_Time/current_time)




def neg_exp_dist_time(rate):
     u = random.uniform(0,1);
     return ((-1/rate)*math.log(1-u));


'''Packet Class'''
class Packet:
    def __init__(self,time):
        self.time = time
        return time
    def getTime():
        return time



'''Event-node Class'''
class E_node(object):

    def __init__(self, time, prev, next, bool):
        self.time = time
        self.prev = prev
        self.next = next
        self.arrival = bool
        return self

    def getTime():
        return time


class DoubleList(object):

    head = None
    tail = None

    def add(self, time):
        newnode = E_node(time,None,None)
        node = self.tail

        if self.head is None:
            self.head = self.tail = newnode
            return self
        if self.tail.time < newnode.time:
            newnode.prev = self.tail
            newnode.next = None
            self.tail.next = newnode
            self.tail = newnode
            return self
        else:
            while node.time > newnode.time:
                node = node.prev
            if node.time < newnode.time:
                newnode.next = node.next
                node.next.prev = newnode
                node.next = newnode
                newnode.prev = node

    def remove(self):
        current_node = self.head
        prev_node = self.head
        current_node = current_node.next
        current_node.prev = None
        current_node.prev.next = None
        return prev_node


    def printing_data(self):
        print("printing all the time in sorted ordered:")
        current_node = self.head
        while current_node.next is not None:
            print(current_node.time)
            current_node = current_node.next

        print("End of the list, GEL")
