import random
import numpy as np

class TCPTahoe:
    def __init__(self):
        self.window_size = 1
        self.packets_sent = 0
        self.packets_received = 0
        self.packet_send_times = {} # Created dictionary to store send times of packets
        self.retransmissions = 0
    
    def send_packet(self):
        self.packets_sent += 1
        self.packet_send_times[self.packets_sent] = random.uniform(0, 1)
    
    def receive_ack(self):
        self.packets_received += 1
        if self.packets_received % self.window_size == 0:
            self.window_size += 1
    
    def handle_packet_loss(self):
        self.retransmissions += 1
    
    def handle_timeout(self):
        self.retransmissions += 1
        self.window_size = 1

    def handle_dup_ack(self):
        if self.packets_received % self.window_size == 0:
            self.handle_packet_loss()
            self.ssthresh = max(self.window_size / 2, 1) #Halve ssthresh
            self.window_size = 1 
            self.fast_recovery = False #Transition to slow start
    
    def calculate_delay(self, ack_number):
        send_time = self.packet_send_times.get(ack_number, 0)
        if send_time:
            return random.uniform(0, 1) - send_time
        return 0

class TCPReno:
    def __init__(self):
        self.window_size = 1
        self.packets_sent = 0
        self.packets_received = 0
        self.packet_send_times = {}
        self.retransmissions = 0
        self.fast_recovery = False
    
    def send_packet(self): 
        self.packets_sent += 1
        self.packet_send_times[self.packets_sent] = random.uniform(0, 1)
    
    def receive_ack(self):
        self.packets_received += 1
        if self.packets_received % self.window_size == 0:
            self.window_size += 1
        else:
            self.window_size *= 0.5
    
    def handle_packet_loss(self):
        self.retransmissions += 1
    
    def handle_timeout(self):
        self.retransmissions += 1
        self.window_size = 1

    def handle_dup_ack(self):
        if self.packets_received % self.window_size == 0:
            self.handle_packet_loss()
            if not self.fast_recovery:
                self.ssthresh = max(self.window_size / 2, 1)  # Halve the ssthresh value
                self.window_size = max(self.window_size / 2, 1)  # Set cwnd to half of the previous value
                self.fast_recovery = True
            else:
                # Increase cwnd for each additional duplicate ACK
                self.window_size += 1
    
    def calculate_delay(self, ack_number):
        send_time = self.packet_send_times.get(ack_number, 0)
        if send_time:
            return random.uniform(0, 1) - send_time 
        return 0

class TCPCubic:
    def __init__(self):
        self.window_size = 1
        self.packets_sent = 0
        self.packets_received = 0
        self.packet_send_times = {}
        self.retransmissions = 0
        self.ssthresh = float('inf') 
        self.cwnd_reduction_factor = 0.5
        self.fast_convergence_factor = 0.7
        self.beta = 0.2 
        self.last_congestion_event_time = 0

    def send_packet(self):
        self.packets_sent += 1
        self.packet_send_times[self.packets_sent] = random.uniform(0, 1)

    def receive_ack(self):
        self.packets_received += 1
        if self.packets_received <= self.ssthresh: 
            self.window_size *= 2
        else: 
            elapsed_time = random.uniform(0, 1) - self.last_congestion_event_time
            self.window_size += (3 * self.beta * (elapsed_time ** 2)) / self.window_size
        self.last_congestion_event_time = random.uniform(0, 1)

    def handle_packet_loss(self):
        self.retransmissions += 1
        self.ssthresh *= self.cwnd_reduction_factor
        self.window_size *= self.fast_convergence_factor
        if self.window_size < 1:
            self.window_size = 1
        self.last_congestion_event_time = random.uniform(0, 1)


    def handle_timeout(self):
        self.retransmissions += 1
        self.ssthresh *= self.cwnd_reduction_factor
        self.window_size = 1
        self.last_congestion_event_time = random.uniform(0, 1)

    def handle_dup_ack(self):
        self.retransmissions += 1

    def calculate_delay(self, ack_number):
        send_time = self.packet_send_times.get(ack_number, 0)
        if send_time:
            return random.uniform(0, 1) - send_time
        return 0

def simulate_network(tcp_type, packet_loss_prob, num_packets):
    tcp = tcp_type()
    packets_lost = 0
    for i in range(num_packets):
        tcp.send_packet()
        if random.random() < packet_loss_prob:
            packets_lost += 1
            tcp.handle_packet_loss() #All tcp types, instead of each one
        else:
            tcp.receive_ack()
    return tcp, packets_lost

def calculate_throughput(packets_sent, packets_lost, simulation_time):
    good_packets = packets_sent - packets_lost
    return good_packets / simulation_time

def calculate_goodput(packets_sent, packets_lost):
    return (packets_sent - packets_lost) / packets_sent

def calculate_average_delay(tcp):
    total_delay = 0
    num_valid_delays = 0
    for i in range(1, tcp.packets_received + 1):
        delay = tcp.calculate_delay(i)
        if delay >= 0:
            total_delay += delay
            num_valid_delays += 1
    if num_valid_delays > 0:
        return total_delay / num_valid_delays
    else:
        return 0

def calculate_delay_jitter(tcp):
    delays = []
    for i in range(1, tcp.packets_received + 1):
        delays.append(tcp.calculate_delay(i))
    return np.var(delays)

#Parameters
packet_loss_probability = [0.1, 0.3, 0.5, 0.7, 0.9]
num_packets = 1000
simulation_time = 10    # in seconds

#Tahoe
tahoe_throughputs = []
tahoe_goodputs = []
tahoe_avg_delays = []
tahoe_delay_jitters = []
tahoe_retransmissions = []

#Reno
reno_throughputs = []
reno_goodputs = []
reno_avg_delays = []
reno_delay_jitters = []
reno_retransmissions = []

#Cubic
cubic_throughputs = []
cubic_goodputs = []
cubic_avg_delays = []
cubic_delay_jitters=[]
cubic_retransmissions = []

for loss_prob in packet_loss_probability:
    tahoe_tcp, packets_lost = simulate_network(TCPTahoe, loss_prob, num_packets)
    tahoe_throughputs.append(calculate_throughput(tahoe_tcp.packets_sent, packets_lost, simulation_time))
    tahoe_goodputs.append(calculate_goodput(tahoe_tcp.packets_sent, packets_lost))
    tahoe_avg_delays.append(round(calculate_average_delay(tahoe_tcp), 3))
    tahoe_delay_jitters.append(round(calculate_delay_jitter(tahoe_tcp), 3))
    tahoe_retransmissions.append(tahoe_tcp.retransmissions)

    reno_tcp, packets_lost = simulate_network(TCPReno, loss_prob, num_packets)
    reno_throughputs.append(calculate_throughput(reno_tcp.packets_sent, packets_lost, simulation_time))
    reno_goodputs.append(calculate_goodput(reno_tcp.packets_sent, packets_lost))
    reno_avg_delays.append(round(calculate_average_delay(reno_tcp), 3))
    reno_delay_jitters.append(round(calculate_delay_jitter(reno_tcp), 3))
    reno_retransmissions.append(reno_tcp.retransmissions)

    cubic_tcp, packets_lost = simulate_network(TCPCubic, loss_prob, num_packets)
    cubic_throughputs.append(calculate_throughput(cubic_tcp.packets_sent, packets_lost, simulation_time))
    cubic_goodputs.append(calculate_goodput(cubic_tcp.packets_sent, packets_lost))
    cubic_avg_delays.append(round(calculate_average_delay(cubic_tcp), 3))
    cubic_delay_jitters.append(round(calculate_delay_jitter(cubic_tcp), 3))
    cubic_retransmissions.append(cubic_tcp.retransmissions)


# Print section
for i, loss_prob in enumerate(packet_loss_probability):
    print(f"Packet Loss Probability: {loss_prob}")
    print("TCP Tahoe:")
    print(f"  Throughput: {tahoe_throughputs[i]}")
    print(f"  Goodput: {tahoe_goodputs[i]}")
    print(f"  Average Delay: {tahoe_avg_delays[i]}")
    print(f"  Delay Jitter: {tahoe_delay_jitters[i]}")
    print(f"  Retranmissions: {tahoe_retransmissions[i]}")
    print("TCP Reno:")
    print(f"  Throughput: {reno_throughputs[i]}")
    print(f"  Goodput: {reno_goodputs[i]}")
    print(f"  Average Delay: {reno_avg_delays[i]}")
    print(f"  Delay Jitter: {reno_delay_jitters[i]}")
    print(f"  Retranmissions: {reno_retransmissions[i]}")
    print("TCP Cubic:")
    print(f"  Throughput: {cubic_throughputs[i]}")
    print(f"  Goodput: {cubic_goodputs[i]}")
    print(f"  Average Delay: {cubic_avg_delays[i]}")
    print(f"  Delay Jitter: {cubic_delay_jitters[i]}")
    print(f"  Retranmissions: {cubic_retransmissions[i]}")
