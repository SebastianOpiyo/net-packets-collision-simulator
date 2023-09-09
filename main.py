# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import time

# Constants
NUM_COMPUTERS = 5

SIMULATION_TIME = 3600  # Time in seconds
COLLISION_THRESHOLD = 2  # Number of packets before collision

# Data structures to store computer information
computers = [{"packets_received": 0, "total_delay": 0.0, "collisions": 0, "last_packet_time": 0.0} for _ in
             range(NUM_COMPUTERS)]


# Function to simulate packet transmission with collisions
def simulate_packet_transmission(packet_size: int, packet_rate_per_computer: int):
    """
    Simulates packet transmission with collisions and computes collision detection.

    Args:
        packet_size (int): The size of each packet in bytes.
        packet_rate_per_computer (int): The rate of packet transmission per computer in packets per second.
    """
    for _ in range(SIMULATION_TIME):
        for computer_id in range(NUM_COMPUTERS):
            # Calculate the time elapsed since the last packet transmission
            time_since_last_packet = _ - computers[computer_id]["last_packet_time"]

            # Generate packets with the given rate
            if time_since_last_packet >= 1.0 / packet_rate_per_computer:
                # Simulate packet transmission with a random delay (1-10 ms)
                delay = np.random.uniform(1.0, 10.0)
                computers[computer_id]["packets_received"] += 1
                computers[computer_id]["total_delay"] += delay
                computers[computer_id]["last_packet_time"] = _  # Update last packet time

                # Check for collision (if more than COLLISION_THRESHOLD packets are transmitted)
                if computers[computer_id]["packets_received"] > COLLISION_THRESHOLD:
                    colliding_nodes = [i for i, comp in enumerate(computers) if
                                       comp["packets_received"] > COLLISION_THRESHOLD]
                    print(f"Collision detected at computer {computer_id}")
                    print(f"Nodes in connection: {colliding_nodes}")
                    for node in colliding_nodes:
                        if computers[node]["packets_received"] > COLLISION_THRESHOLD:
                            computers[node]["collisions"] += 1
                            computers[node]["packets_received"] = 0  # Reset packet count
                            computers[node]["total_delay"] = 0.0  # Reset delay

        time.sleep(1)  # Simulate 1-second time intervals


# Add this function to calculate network throughput
def calculate_network_throughput(computers, packet_size, packet_rate_per_computer):
    """
    Calculates network throughput in bytes per second.

    Args:
        computers (list): List of computer data structures.
        packet_size (int): The size of each packet in bytes.
        packet_rate_per_computer (int): The rate of packet transmission per computer in packets per second.

    Returns:
        float: Network throughput in bytes per second.
    """
    total_bytes_transmitted = sum([computer["packets_received"] * packet_size for computer in computers])
    network_throughput = total_bytes_transmitted / SIMULATION_TIME
    return network_throughput


# Add this function to calculate packet loss rate
def calculate_packet_loss_rate(computers, packet_rate_per_computer):
    """
    Calculates packet loss rates for each computer.

    Args:
        computers (list): List of computer data structures.
        packet_rate_per_computer (int): The rate of packet transmission per computer in packets per second.

    Returns:
        list: List of packet loss rates for each computer.
    """
    packet_loss_rates = [1.0 - (computer["packets_received"] / (SIMULATION_TIME * packet_rate_per_computer)) for
                         computer in computers]
    return packet_loss_rates


# Plot the packet interval time per computer
def plot_packet_interval_time(computers, packet_rate_per_computer):
    """
    Plots the packet interval time per computer.

    Args:
        computers (list): List of computer data structures.
        packet_rate_per_computer (int): The rate of packet transmission per computer in packets per second.
    """
    computer_ids = range(NUM_COMPUTERS)
    packet_interval_times = [1.0 / packet_rate_per_computer if computer["packets_received"] > 0 else 0 for computer in
                             computers]

    plt.figure(figsize=(10, 5))
    plt.plot(computer_ids, packet_interval_times, marker='o')
    plt.xlabel("Computer ID")
    plt.ylabel("Packet Interval Time (seconds)")
    plt.title("Packet Interval Time per Computer")
    plt.grid(True)
    plt.show()


# Plot the number of packet collisions per computer
def plot_packet_collisions_per_computer(computers):
    """
    Plots the number of packet collisions detected per computer.

    Args:
        computers (list): List of computer data structures.
    """
    computer_ids = range(NUM_COMPUTERS)
    collision_counts = [computer["collisions"] for computer in computers]

    plt.figure(figsize=(10, 5))
    plt.bar(computer_ids, collision_counts, tick_label=computer_ids)
    plt.xlabel("Computer ID")
    plt.ylabel("Collisions Detected")
    plt.title("Number of Packet Collisions Detected per Computer")
    plt.show()


# Plot the number of packets per computer
def plot_packets_per_computer(computers):
    """
    Plots the number of packets received per computer.

    Args:
        computers (list): List of computer data structures.
    """
    computer_ids = range(NUM_COMPUTERS)
    packets_received = [computer["packets_received"] for computer in computers]

    plt.figure(figsize=(10, 5))
    plt.bar(computer_ids, packets_received, tick_label=computer_ids)
    plt.xlabel("Computer ID")
    plt.ylabel("Packets Received")
    plt.title("Number of Packets per Computer")
    plt.show()


# Plot the average packet delay per computer
def plot_average_packet_delay(computers):
    """
    Plots the average packet delay per computer.

    Args:
        computers (list): List of computer data structures.
    """
    computer_ids = range(NUM_COMPUTERS)
    avg_delays = [computer["total_delay"] / computer["packets_received"] if computer["packets_received"] > 0 else 0 for
                  computer in computers]

    plt.figure(figsize=(10, 5))
    plt.plot(computer_ids, avg_delays, marker='o')
    plt.xlabel("Computer ID")
    plt.ylabel("Average Delay (ms)")
    plt.title("Average Packet Delay per Computer")
    plt.grid(True)
    plt.show()


def main():
    # Set your packet size and packet rate per computer
    packet_size = 100  # bytes
    packet_rate_per_computer = 5  # packets per second

    # Simulate packet transmission with collisions
    simulate_packet_transmission(packet_size, packet_rate_per_computer)

    # Plot the graphs
    plot_packet_collisions_per_computer(computers)
    plot_packets_per_computer(computers)
    plot_average_packet_delay(computers)

    # Calculate and print network throughput
    network_throughput = calculate_network_throughput(computers, packet_size, packet_rate_per_computer)
    print("Network Throughput (bytes/second):", network_throughput)

    # Calculate and print packet loss rates
    packet_loss_rates = calculate_packet_loss_rate(computers, packet_rate_per_computer)
    print("Packet Loss Rates per Computer:", packet_loss_rates)

    # Plot packet interval time per computer
    plot_packet_interval_time(computers, packet_rate_per_computer)


if __name__ == "__main__":
    main()
