
import random
import math

######################
## Global Variables ##
######################
g_max_buffer = float("inf")
g_arrival_rates1 = [.1,.25,.4,.55,.65,.80,.90]
g_arrival_rate = 0
g_service_rate = 1

g_arrival_rates2 = [.2,.4,.6,.8,.9]
g_max_buffers = [1,20,50]

g_GEL = []
g_fifo = []
g_server_is_free = True

g_time = 0

g_test = 0

g_server_busy_time = 0
g_buffer_length = []
g_num_packets_dropped = 0

######################
###### Classes #######
######################
class Event:
    def __init__(self, e_time = -1, e_type = "", e_next = None, e_prev = None):
        self.e_time = e_time
        self.e_type = e_type
        self.e_next = e_next
        self.e_prev = e_prev

######################
##### Functions ######
######################
def process_arrival_event(event, arrival_distribution):
    global g_time
    global g_buffer_length
    global g_GEL
    global g_fifo
    global g_num_packets_dropped
    global g_server_busy_time
    global g_server_is_free
    
    delta_time = event.e_time - g_time
    g_time = event.e_time
    
    random_arrival_time = arrival_distribution(g_arrival_rate)
    next_arrival_time = g_time + random_arrival_time
    
    random_service_time = negative_exponentially_distributed_time(g_service_rate)
    
    new_arrival_event = Event(e_time = next_arrival_time, e_type = "Arrival")
    g_GEL.append(new_arrival_event)
    g_GEL.sort(key=lambda event: event.e_time)
    
    if g_server_is_free:
        g_server_is_free = False
        new_departure_event = Event(e_time = g_time + random_service_time, e_type = "Departure")
        g_GEL.append(new_departure_event)
        g_GEL.sort(key=lambda event: event.e_time)
    else:
        if len(g_fifo) < g_max_buffer:
            g_fifo.append(new_arrival_event)
        else:
            g_num_packets_dropped += 1
    g_server_busy_time += random_service_time

    g_buffer_length.append(len(g_fifo)*delta_time)

def process_departure_event(event):
    global g_time
    global g_buffer_length
    global g_GEL
    global g_server_busy_time
    global g_server_is_free
    global g_fifo
    
    delta_time = event.e_time - g_time
    g_time = event.e_time
    
    g_server_is_free = True
    if len(g_fifo) > 0:
        g_server_is_free = False
        
        popped_event = g_fifo.pop(0)
        random_service_time = negative_exponentially_distributed_time(g_service_rate)
        new_departure_event = Event(e_time = g_time + random_service_time, e_type = "Departure")
        g_GEL.append(new_departure_event)
        g_GEL.sort(key=lambda event: event.e_time)
        g_buffer_length.append(len(g_fifo)*delta_time)
    else:
        g_buffer_length.append(0)


def output_simulated_statistics():
    global g_time
    global g_server_busy_time
    global g_max_buffer
    
    mean_queue_length = sum(g_buffer_length)/g_time
    utilization = g_server_busy_time/g_time
    
    print
    print "###### SIM STATS#######"
    
    if g_max_buffer == float("inf"):
        print "SIM_utilization =", utilization
        print "SIM_mean_queue_length =", mean_queue_length
    print "SIM_number_packets_dropped =",g_num_packets_dropped
    print

def output_mathematical_statistics():
    utilization = g_arrival_rate/g_service_rate
    
    mean_queue_length = pow(utilization,2)/(1-utilization)
    print "###### MATH STATS#######"
    print "MATH_utilization =", utilization
    print "MATH_mean_queue_length =", mean_queue_length
    print "MATH_number_packets_dropped =",g_num_packets_dropped

def negative_exponentially_distributed_time(rate):
    return ((-1/rate)*math.log(1-random.random()))

# x_m * e^y where x_m is .1 * 1/rate and y is negative exponential distribution(1)
def pareto_distribution(rate):
    pareto = (.1 * (1/rate * math.pow(math.e,negative_exponentially_distributed_time(1))))
    return pareto

def initialize(arrival_distribution):
    global g_GEL
    global g_time
    
    first_event = Event(e_type = "Arrival")
    random_arrival_time = arrival_distribution(g_arrival_rate)
    first_event.e_time = g_time + random_arrival_time
    g_GEL.append(first_event)

def reset_globals():
    global g_time
    global g_buffer_length
    global g_GEL
    global g_fifo
    global g_num_packets_dropped
    global g_server_busy_time
    global g_server_is_free
    
    g_GEL = []
    g_fifo = []
    g_server_is_free = True
    
    g_time = 0
    
    g_server_busy_time = 0
    g_buffer_length = []
    g_num_packets_dropped = 0

def print_headers():
    print "MAX_BUFFER_SIZE =", g_max_buffer
    print "arrival rate = ", g_arrival_rate
    print "---------------------------------"

def run_simulation(rate, arrival_distribution, max_buffer):
    global g_arrival_rate
    global g_max_buffer
    g_arrival_rate = rate
    g_max_buffer = max_buffer
    initialize(arrival_distribution)
    for i in range(0,100000):
        if len(g_GEL):
            popped_event = g_GEL.pop(0)
            if popped_event.e_type == "Arrival":
                process_arrival_event(popped_event, arrival_distribution)
            else:
                process_departure_event(popped_event)
    print_headers()
    output_simulated_statistics()

if g_max_buffer == float("inf"):
    output_mathematical_statistics()
    reset_globals()

def run_all_simulations(arrival_distribution):
    print "======================================="
    print arrival_distribution.__name__
    print "======================================="
    for rate in g_arrival_rates1:
        run_simulation(rate, arrival_distribution, float("inf"))
    for max_buffer in g_max_buffers:
        for rate in g_arrival_rates2:
            run_simulation(rate, arrival_distribution, max_buffer)

######################
######## MAIN ########
######################
def main():
    run_all_simulations(negative_exponentially_distributed_time)
    run_all_simulations(pareto_distribution)

if __name__ == '__main__':
    main()



