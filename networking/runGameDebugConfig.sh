#!/bin/bash

if hash python3 2>/dev/null; then
    kill $(ps aux | grep python | grep $1| awk '{print $2}'); ./public/halite -j -z 25 -n 1 -x 25 -t -d "10 10" "python3 networking/pipe_socket_translator.py $1";
fi
