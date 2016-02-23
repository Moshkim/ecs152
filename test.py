

from math import log
from random import random
import sys
import Queue
import heapq

class Event:
    def __init__(self, eventType, eventTime):
        validEvents = ['arrival', 'departure', 'dropped']
        self.type = eventType
        self.eventTime = eventTime
        if eventType not in validEvents:
            print "invalid event type: " + eventType + ';'
            exit(0)


class Packet:
    def __init__(self, arrivalTime, serviceTimeStart, serviceTime):
     self.arrivalTime      = arrivalTime 								# When packet gets in the queue
     self.serviceTimeStart = serviceTimeStart							# When packet actually starts getting processed
     self.serviceTime      = serviceTime 								# Time it takes to actually process the packet once its at head
     self.serviceTimeEnd   = self.serviceTimeStart + self.serviceTime 	# When Packet is fully processed
     self.waitTime         = self.serviceTimeStart - self.arrivalTime 	# Time spent waiting in queue (Before processed)

class GlobalEventList:
    def __init__(self, maxBuffer):
        self.heap = []
        self.maxBuffer = maxBuffer
    
    def put(self, event):
        heapq.heappush(self.heap, (event.eventTime, event)) # We push tuples because this thing doesnt support lammbdas
        if len(self.heap) >  maxBuffer:
            print "Buffer limit violated, crashing"
            exit(0)

def get(self):
    (eventTime, event) = heapq.heappop(self.heap)
    return event
    
    def report(self):
        for e in self.heap:
            print e[1].type + " : " + str(e[1].eventTime)

# Generate random service time (the time it takes to send the packet)
def genServiceTime(rate):
    rand = ((-1 / rate * log(1 - random())))
    return rand

# Generate random arrival time of packet
# Will be the time taken between the last one arriving.
def genPacketTime(rate):
    rand = ((-1 / rate * log(1 - random())))
    return rand

# Schedule an arrival event for the GEL
def schedulePacketArrival(globalEventList, packetRate, eventTime):
    arrivalEvent = Event('arrival', eventTime)
    globalEventList.put(arrivalEvent)

def generateStatistics(processedEventList, numDropped, processedPackets):
    
    # Sanity checks
    
    
    # Calculate utilization
    lastEventTime = 0
    timeUtilized = 0
    totalTimeUsed = processedEventList[-1][0].eventTime # The last even that we actually processed
    
    for event, bufferLength in processedEventList:
        currentEventTime = event.eventTime
        if bufferLength > 0:
            timeUtilized = timeUtilized + (currentEventTime - lastEventTime)
        lastEventTime = currentEventTime # For next iteration
    
    # Calculate average buffer length using a time weighted average
    lastEventTime = 0
    weightedBufferLength = 0
    for event, bufferLength in processedEventList:
        currentEventTime = event.eventTime
        weightedBufferLength = weightedBufferLength + ((currentEventTime - lastEventTime) * bufferLength)
        
        lastEventTime = currentEventTime # For next iteration
    averageBufferLength = weightedBufferLength / totalTimeUsed

    print 'statistics: '
    print 'total time: ' + str(totalTimeUsed)
    print 'time utilized: ' + str(timeUtilized)
    print 'percentage utilized: ' + str(timeUtilized / totalTimeUsed * 100)
    print 'averageBufferLength: ' + str(averageBufferLength)
    print 'actual num dropped   : ' + str(numDropped)
    print 'actual num processed : ' + str(len(processedPackets))





def runSimulation(packetRate, serviceRate, maxBuffer, targetTime):
    time = 0.0
    globalEventList = GlobalEventList(maxBuffer) # GEL
    processedEventList = [] # Not guaranteed to be in order
    packetBuffer = [] # the packet is not removed from the buffer until it has been served
    processedPackets = []
    numDropped = 0
    
    
    # Logic is poorly done here, we will overstep the target time
    schedulePacketArrival(globalEventList, packetRate, genPacketTime(packetRate)) # intitial packet arrival

    while True:
        print time
        print len(packetBuffer)
        
        currentEvent = globalEventList.get()
        lastEventTime = time
        time = currentEvent.eventTime
        
        if time > targetTime:
            break
    
        if currentEvent.type == 'arrival':
            # Handle an arriving packet
            
            if len(packetBuffer) >= maxBuffer and maxBuffer != -1: # Buffer full, drop packet. Check for infinite buffer with -1
                dropEvent = Event('dropped', time)
                processedEventList.append((dropEvent, len(packetBuffer))) # We don't actually need to process these, just record
                numDropped = numDropped + 1
        
            else:
                if len(packetBuffer) == 0: # If there are no packets in the buffer then we start serivicing now
                    newPacketServiceTimeStart = time
                else: # Otherwise we wait until the last one is done
                    newPacketServiceTimeStart = packetBuffer[-1].serviceTimeEnd # When the last packet in the buffer will be done
            
                newPacket = Packet(time, newPacketServiceTimeStart, genServiceTime(serviceRate))
                packetBuffer.append(newPacket)
                
                #Schedule when this packet will be departing
                departureEvent = Event('departure', newPacket.serviceTimeEnd)
                globalEventList.put(departureEvent)
        
        schedulePacketArrival(globalEventList, packetRate, time + genPacketTime(packetRate)) # We schedule another packet on each ARRIVAL
        
        
        if currentEvent.type == 'departure':
            # Handle departing packet
            if len(packetBuffer) <= 0:
                print "The buffer should not be empty, CRASHING"
            
            departingPacket = packetBuffer.pop(0)
            processedPackets.append(departingPacket)
    
    
        # Event processed, adding to the list of events processed
        # We also keep track of the number of packets that are in the buffer when this event was processed (use to calculate statistics)
        processedEventList.append((currentEvent, len(packetBuffer)))
        
        print '---------------------------------------------------'


# Generate the statistics!
    generateStatistics(processedEventList, numDropped, processedPackets)




# Infinite buffer denoted by -1
if __name__ == "__main__":
    (packetRate, serviceRate, maxBuffer, targetTime) = sys.argv[1:]
    
    print "packet rate: " + packetRate
    print "serviceRate: " + serviceRate
    print "maxBuffer  : " + maxBuffer
    print "targetTime : " + targetTime
    
    runSimulation(float(packetRate), float(serviceRate), int(maxBuffer), float(targetTime))


