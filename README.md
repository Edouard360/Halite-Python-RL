[![Build Status](https://travis-ci.org/Edouard360/Halite-Python-RL.svg?branch=master)](https://travis-ci.org/Edouard360/Halite-Python-RL) [![Coverage Status](https://coveralls.io/repos/github/Edouard360/Halite-Python-RL/badge.svg?branch=master)](https://coveralls.io/github/Edouard360/Halite-Python-RL?branch=master)

# Halite-Python-RL

<p align="center"> <b> Halite Challenge Overview </b> <br> 
<a href="https://halite.io/" target="_blank"><img width="480" src="https://user-images.githubusercontent.com/15527397/30818756-c0526c06-a21c-11e7-95a8-317dded1e761.gif"></a></p>

<br>

## Description 

<a href="https://halite.io/">Halite</a> is an open source artificial intelligence programming challenge, created by <a href="https://www.twosigma.com/">Two Sigma</a>, where players build bots using the coding language of their choice to battle on a two-dimensional virtual board. The last bot standing or the bot with all the territory wins. Victory will require micromanaging of the movement of pieces, optimizing a bot’s combat ability, and braving a branching factor billions of times higher than that of Go.

## Objective

The objective of the project is to apply **Reinforcement Learning** strategies to teach the Bot to perform as well as possible. We teach an agent to learn the best actions to play at each turn. More precisely, given the game state, our untrained Bot **initially performs random actions, but gets rewarded for the good one**. Over time, the Bot automatically learns how to conquer efficiently the map.

Eventually, it is even possible to make multiple Bots fight against themselves and improve their responses to other Bots.

For now, **we will only focus on one Bot**, the objective being to **conquer the map as fast as possible**. With respect to Reinforcement Learning, the two main challenges to address are the following:

- Finding a good **Reward Function**, and associate properly each action to a reward.

Indeed, unlike chess or go, in the Halite turn-based game, we can do **multiple actions at each turn**, for each of the square we possess. This implies that we have to identify the specific actions leading to the reward, which can in turn be complicated to compute.

- Exploring the **Best Learning Strategies**.

In this repository, we will mainly explore the solutions based on **Neural Networks**, and will start by a very simple <a href="https://en.wikipedia.org/wiki/Multilayer_perceptron">MLP</a>. This is inspired from a <a href="https://medium.com/@awjuliani/super-simple-reinforcement-learning-tutorial-part-2-ded33892c724">tutorial</a> on Reinforcement Learning agent.

## Documentation & Articles

To get started, blog articles and documentation are available at <a href="https://edouard360.github.io/Halite-Python-RL/">this page</a>.