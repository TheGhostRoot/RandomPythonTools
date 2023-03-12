#!/bin/bash

# Define starting port and number of instances
start_port=9050
num_instances=$1

# Loop through the desired number of instances
for (( i=0; i<$num_instances; i++ )); do
  # Calculate the port number based on the current iteration
  port=$(($start_port + ($i * 10)))

  # Stop Tor with the specified config file
  sudo killall -q -s SIGINT tor

  # Remove the config file
  #sudo rm "/etc/tor/torrc.$port"
done

# ./stop_torrs.sh 3
# stops the first 3 tor configs
