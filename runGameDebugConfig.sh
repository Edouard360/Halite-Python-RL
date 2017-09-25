#!/bin/bash

if hash python3 2>/dev/null; then
    kill $(ps aux | grep python | grep $1| awk '{print $2}');./halite -x 30 -j -t -d "10 10" "python3 RandomBotTraining.py" "python3 pipe_socket_translator.py $1";
fi
