#!/bin/bash

kill $(ps aux | grep python | grep -v start_game.py | grep $1| awk '{print $2}');

kill $(ps aux | grep python | grep -v pipe_socket_translator.py | grep $1| awk '{print $2}');