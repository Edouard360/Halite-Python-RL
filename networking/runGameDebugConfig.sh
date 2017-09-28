#!/bin/bash

kill $(ps aux | grep python | grep $1| awk '{print $2}'); ./public/halite -j -t -n 1 -z 25 -x 25 -d "10 10" "python3 ./networking/pipe_socket_translator.py $1";