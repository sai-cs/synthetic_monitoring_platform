from prometheus_client import start_http_server, Gauge
from readYAML import load_yaml_file
from networkMonitor import get_ping_metrics, display_metrics
from prometheus_client import start_http_server, Summary
import yaml
import pingparsing
import time
import json

# Prometheus metrics to collect
RTT_MIN = Gauge('ping_rtt_min_seconds', 'Minimum RTT of ping requests', ['server'])
RTT_MAX = Gauge('ping_rtt_max_seconds', 'Maximum RTT of ping requests', ['server'])
RTT_AVG = Gauge('ping_rtt_avg_seconds', 'Average RTT of ping requests', ['server']) # Ping Latency
PACKET_LOSS = Gauge('packet_loss_count', 'Number of packets lost during ping', ['server'])
PING_LATENCY = Gauge('ping_request_latency_seconds', 'Latency of ping requests', ['server'])
PACKET_TRANSMIT = Gauge('packet_transmit_count', 'Number of packets transmitted', ['server'])
PACKET_RECEIVE = Gauge('packet_receive_count', 'Number of packets received', ['server'])
PACKET_DUPLICATE_COUNT = Gauge('packet_duplicate_count', 'Number of duplicate packets received', ['server'])
PACKET_DUPLICATE_RATE = Gauge('packet_duplicate_rate', 'Rate of duplicate packets received', ['server'])

# Load YAML Configuration File
def load_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except yaml.YAMLError as exc:
        print(f"Error: An error occurred while parsing YAML file - {exc}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

# Get Ping Metrics
def get_ping_metrics(destination):
    transmitter = pingparsing.PingTransmitter()
    ping_parser = pingparsing.PingParsing()
    
    transmitter.destination = destination
    transmitter.count = 4  # Number of pings per server
    
    result = transmitter.ping()
    stats = ping_parser.parse(result)
    
    # Expose metrics to Prometheus
    RTT_MIN.labels(server=destination).set(stats.rtt_min)
    RTT_MAX.labels(server=destination).set(stats.rtt_max)
    RTT_AVG.labels(server=destination).set(stats.rtt_avg)
    PACKET_LOSS.labels(server=destination).set(stats.packet_loss_count)
    PACKET_TRANSMIT.labels(server=destination).set(stats.packet_transmit)
    PACKET_RECEIVE.labels(server=destination).set(stats.packet_receive)
    PACKET_DUPLICATE_COUNT.labels(server=destination).set(stats.packet_duplicate_count or 0)
    PACKET_DUPLICATE_RATE.labels(server=destination).set(stats.packet_duplicate_rate or 0)
    
    return stats.as_dict()

# Display Metrics
def display_metrics(server, metrics):
    print(f"Metrics for {server}:")
    print(json.dumps(metrics, indent=4))

# Main Function for Ping Monitor
def ping_monitor(config):
    servers = config.get("servers", [])
    interval = config.get("interval", 60)  # Default to 60 seconds if not specified
    
    while True:
        for server in servers:
            try:
                # Get metrics and expose them to Prometheus
                metrics = get_ping_metrics(server)
                
                # Display metrics on the console
                display_metrics(server, metrics)
            except Exception as e:
                print(f"An error occurred while pinging {server}: {e}")
        
        print(f"Waiting {interval} seconds before the next round of pings...\n")
        time.sleep(interval)

if __name__ == "__main__":
    # Start Prometheus metrics server on port 8989
    start_http_server(8989)
    
    # Load the YAML configuration
    config = load_yaml_file('config.yml')
    
    if config:
        ping_monitor(config)
