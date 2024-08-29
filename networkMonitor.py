import pingparsing
import json

def get_ping_metrics(destination):
    # Create instances of PingTransmitter and PingParsing
    transmitter = pingparsing.PingTransmitter()
    ping_parser = pingparsing.PingParsing()

    # Set the destination and ping count
    transmitter.destination = destination
    transmitter.count = 4  # Number of ping requests to send

    # Execute the ping command
    result = transmitter.ping()

    # Parse the result
    stats = ping_parser.parse(result)
    
    # Return the parsed result as a dictionary
    return stats.as_dict()

def display_metrics(metrics):
    # Pretty-print the metrics
    print(json.dumps(metrics, indent=4))

def main():
    # Take user input for the destination to ping
    destination = input("Enter the server address to ping: ")
    
    try:
        # Get ping metrics
        metrics = get_ping_metrics(destination)
        
        # Display the metrics
        display_metrics(metrics)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
