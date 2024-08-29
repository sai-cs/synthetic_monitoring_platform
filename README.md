# Synthetic Monitoring Platform
This project is a Synthetic Monitoring Platform that collects and exposes network metrics like Round-Trip Time (RTT), Packet Loss, and other relevant statistics using Prometheus and visualizes them with Grafana.

Project Structure
config.yml: This file contains the server addresses to be monitored and the interval for pinging.
networkMonitor.py: Contains functions for performing ping operations and extracting metrics.
pingMonitor.py: The main script that runs the ping operations, collects metrics, and exposes them to Prometheus.
readYAML.py: Handles loading and parsing the YAML configuration file.
prometheus.yml: Configuration file for setting up Prometheus to scrape metrics from the ping monitor.
How to Set Up and Run the Platform
Step 1: Clone the Repository
First, clone this repository to your local machine:

git clone https://github.com/your-username/synthetic_monitoring_platform.git cd synthetic_monitoring_platform

Step 2: Set Up Prometheus
Install Prometheus: If Prometheus is not already installed on your machine, you can download it from the Prometheus website.

Configure Prometheus:

Copy the prometheus.yml file from this repository to your Prometheus configuration directory.
This configuration file tells Prometheus to scrape metrics from the Synthetic Monitoring Platform (on port 8989) and from Prometheus itself (on port 9090).
Start Prometheus:

Run the following command in your terminal to start Prometheus:
./prometheus --config.file=prometheus.yml

Ensure that Prometheus is running by navigating to http://localhost:9090 in your web browser.
Step 3: Set Up and Run the Synthetic Monitoring Platform
Install Required Python Packages:

Navigate to the directory where you cloned the repository and install the necessary Python packages:
pip install prometheus-client pingparsing pyyaml

Configure the Servers to Monitor:

Edit the config.yml file to include the servers you want to monitor and set the desired interval for pinging (in seconds):
servers:

google.com
amazon.com
microsoft.com interval: 10
Run the Monitoring Script:

Run the pingMonitor.py script to start the monitoring process:
python pingMonitor.py

The script will start pinging the specified servers at the defined interval and expose the collected metrics on http://localhost:8989.
Step 4: Set Up Grafana
Install Grafana: If Grafana is not already installed, you can download it from the Grafana website.

Start Grafana:

Run Grafana and access it via http://localhost:3000.
Log in with the default credentials (admin / admin) and change the password when prompted.
Add Prometheus as a Data Source:

Navigate to Configuration > Data Sources.
Click Add data source and select Prometheus.
Set the URL to http://localhost:9090 and click Save & Test.
Create a Dashboard:

Create a new dashboard in Grafana and add panels to visualize the metrics collected by the Synthetic Monitoring Platform. Some metrics you may want to visualize include:
RTT Min (ping_rtt_min_seconds)
RTT Max (ping_rtt_max_seconds)
RTT Avg (ping_rtt_avg_seconds)
Packet Loss (packet_loss_count)
Packet Transmit Count (packet_transmit_count)
Packet Receive Count (packet_receive_count)
Packet Duplicate Count (packet_duplicate_count)
Packet Duplicate Rate (packet_duplicate_rate)
Step 5: Monitor Your Servers
Once everything is set up, Grafana will display real-time metrics collected by your synthetic monitoring platform. Customize the dashboards and panels as needed to suit your monitoring requirements.
