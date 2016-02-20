
"""
***Event.py***
"""

import math
import random
import Queue

#MAXBUFFEE[2] = [1,20,50]

def neg_exp_dist_time(rate):
    u = random.uniform(0,1);
    return ((-1/rate)*math.log(1-u));


'''Packet Class'''
class Packet:
    def __init__(self,time):
        self.time = time
    def getTime(self):
        return self.time



'''Event-node Class'''
class E_node(object):
    
    def __init__(self, time, prev, next, bool):
        self.time = time
        self.prev = prev
        self.next = next
        self.arrival = bool
    
    def getTime(self):
        return self.time


class DoubleList(object):
    
    def __init__(self, head, tail): # Creates initial list w/ head and tail as None
        self.head = head
        self.tail = tail
    
    def add(self, time, bool):
        newnode = E_node(time,None,None,bool)
        print "add new node ", newnode.time
        #node = self.tail
        
        if self.head is None:
            self.head = self.tail = newnode
        
        elif self.tail.time < newnode.time:
            newnode.prev = self.tail
            newnode.next = None
            self.tail.next = newnode
            self.tail = newnode
       
        else:
            node = self.tail
            print "tail", node.getTime()
            while node.time > newnode.getTime():
                print "tail is greater than newnode", node.time
                if node.prev is None:
                    print "node.prev is None"
                    newnode.next = node
                    node.prev = newnode
                    self.head = newnode
                    break
                else:
                    node = node.prev
            if node.time < newnode.time:
                print "here", node.time
                newnode.next = node.next
                node.next.prev = newnode
                node.next = newnode
                newnode.prev = node
                print newnode.prev.time
                print newnode.next.time
        print "end of add"
    def remove(self):
        current_node = self.head
        if current_node.next is None:
            self.head = current_node.next
        else:
            self.head = current_node.next
            self.head.prev = None
        return current_node
    
    
    def printing_data(self):
        print("printing all the time in sorted ordered:")
        current_node = self.head
        while current_node.next is not None:
            print(current_node.time)
            current_node = current_node.next
        
        print("End of the list, GEL")

def main():

    '''initializing length = # of packets in the queue'''
    '''time is the current time'''

    #rate[6] =[0.1,0.25,0.4,0.55,0.65,0.8,0.9]


    arrival_rate = input("Enter the rate?: ")

    MAXBUFFER = input("Enter the MAXBUFFER size?(-1 for infinite): ")

    #lamda = [0.1,0.25,0.4,0.55,0.65,0.8,0.9] when the buffer size is infinite
    #lamda = [0.2, 0.4, 0.6, 0.8, 0.9] when MAXBUFFER = 1, 20, and 50

    #miu = 1 packet/second

    packet_drop = 0
    current_time = 0
    q = Queue.Queue()
    length = q.qsize()
    GEL = DoubleList(None,None)
    transmission_Time = 0

    '''the first arrival event'''
    GEL.add(current_time + neg_exp_dist_time(arrival_rate),True)

    for i in range(0, 100000):
        #print(GEL.head.time)
        current_node = GEL.remove()
        current_time = current_node.getTime()
        print current_node.arrival, " *************************"
        if current_node.arrival == True:
            '''Process an arrival Event'''
            newpacket = Packet(neg_exp_dist_time(1))
            GEL.add((current_time + neg_exp_dist_time(arrival_rate)),True)
            print "create next arrival event"
            if MAXBUFFER > 0:
                if length == 0:
                #transmission_time = newpacket.getTime()
                 #Insert the departure event at the right place in GEL
                    length += 1
                    GEL.add(current_time + newpacket.getTime(),False)
                    print "create departure event1"
                elif length-1<MAXBUFFER:
                    q.put(newpacket)
                    length += 1

                else:
                    packet_drop += 1

            elif MAXBUFFER == -1:
                if length == 0:
                    length += 1
                    GEL.add(current_time + newpacket.getTime(),False)
                    print "create departure event2"
                else:
                    q.put(newpacket)
                    print "put in the queue", q.empty(), "++++++++++++++++++++++++++"
                    length += 1

        elif current_node.arrival == False:
            transmission_Time += current_node.getTime()
            
            length -= 1
            if length == 0:
                continue
            elif length > 0:
                print " did I process departure?"
                print "stuck here", q.empty()
                departure_node =  q.get()
                print departure_node.time
                GEL.add(current_time + departure_node.getTime(),False)
                print "process departure event"

            #1. get the first event from the GEL;
            #2. If the event is an arrival then process-arrival-event;
            #3. Otherwise it must be a departure event and hence
            #process-service-completion;

            #output-statistics;
    print "current_time is: ",current_time
    print "The number of the packet dropped is: ", packet_drop
    print "Untilization fraction is: ", transmission_Time,current_time

if __name__ == '__main__': main()


