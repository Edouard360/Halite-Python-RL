#!/bin/bash

kill $(ps aux | grep python | grep -v start_game.py | grep $1| awk '{print $2}');