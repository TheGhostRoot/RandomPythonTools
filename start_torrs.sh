#!/bin/bash

#!/bin/bash

start_port=9050
port_step=10

read -p "Enter number of Tor processes to start: " num_processes

for (( i=0; i<num_processes; i++ )); do
    port=$(( start_port + i * port_step ))
    config_file="/etc/tor/torrc.${port}"
    if [ ! -f "$config_file" ]; then
        echo "Creating config file: $config_file"
        touch $config_file
        echo SocksPort $port >> $config_file
        echo ControlPort $(( port + 1 )) >> $config_file
        echo DataDirectory /var/lib/tor$port >> $config_file
        echo CookieAuthentication 1 >> $config_file
    fi
    echo "Starting Tor at Socks Port ${port} and Control Port $(( port + 1 ))"
    sudo tor -f $config_file &
done


# ./start_torrs.sh 3
# starts the first 3 tor configs
