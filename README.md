# Halite-Python-RL

<p align="center"> <b> Halite Challenge Overview </b> <br> 
<a href="https://halite.io/" target="_blank"><img width="480" src="https://user-images.githubusercontent.com/15527397/30818756-c0526c06-a21c-11e7-95a8-317dded1e761.gif"></a></p>

<br>



## Description 

<a href="https://halite.io/">Halite</a> is an open source artificial intelligence programming challenge, created by <a href="https://www.twosigma.com/">Two Sigma</a>, where players build bots using the coding language of their choice to battle on a two-dimensional virtual board. The last bot standing or the bot with all the territory wins. Victory will require micromanaging of the movement of pieces, optimizing a bot’s combat ability, and braving a branching factor billions of times higher than that of Go.

## Objective

The objective of the project is to apply Reinforcement Learning strategies to teach the Bot to perform as well as possible. We teach an agent to learn the best actions to play at each turn. More precisely, given the game state, our untrained Bot initially performs random actions, but gets rewarded for the good one. Over time, the Bot automatically learns how to conquer efficiently the map.

Eventually, it is even possible to make multiple Bots fight against themselves and improve their responses to other Bots.

For now, we will only focus on one Bot, the objective being to conquer the map as fast as possible. With respect to reinforcement learning, the two main challenges to address are the following:

- Finding a good reward function, and associate properly each action to a reward.

Indeed, unlike chess or go, in the Halite turn-based game, we can do multiple actions at each turn, for each of the square you possess. This implies that we have to identify the specific actions leading to the reward, which can in turn be complicated to compute.

- Exploring the best learning strategies.

In this repository, we will mainly explore the solutions based on Neural Networks, and will start by a very simple <a href="https://en.wikipedia.org/wiki/Multilayer_perceptron">MLP</a>. This is inspired from a <a href="https://medium.com/@awjuliani/super-simple-reinforcement-learning-tutorial-part-2-ded33892c724">tutorial</a> on Reinforcement Learning agent.


## Detailing the approach step by step

We will explain the rules of the game in this section, along with our strategy for training the agent. To start simple, we will try to conquer a 3*3 map, where we are the only player (cf below). As we can see, this trained agent is already pretty efficient at conquering the map. 

<br>
<p align="center">
<img alt="conquermap" src="https://user-images.githubusercontent.com/15527397/30869334-20c1a650-a2e1-11e7-9c1b-9233640ccd01.gif" height="190" width="32%">
<br></p>

### How does it start ?

Each player starts with a single square of the map, and can either decide:

- To stay in order to increase the strength of its square (action = STILL).

- To move (/conquer) a neighboring square (action = NORTH, SOUTH, EAST, WEST).

Conquering is only possible once the square's strength is high enough, such that a wise bot would first wait for its strength to increase before attacking any adjacent square, since **squares don't produce when they attack**.

<br>

The white numbers on the map below represent the current strength of the squares. On the left is just a snap of the initial state of the game. On the right you can see the strength of the blue square increment over time. This is because our agent decides to stay (action = STILL).

<p align="center">

<img alt="the strength map" src="https://user-images.githubusercontent.com/15527397/30869344-24b55702-a2e1-11e7-9383-0dc7f562e5d6.png" height="190" width="32%">
 
<img height="190" width="32%" src="https://user-images.githubusercontent.com/15527397/30869349-27abe944-a2e1-11e7-8b6e-94dfde9e15a1.gif"></p>

The increase in production is computed according to a fixed production map. In our example, we can see the blue square's strength increases by 4 at each turn. Each square has a different production speed, as represented by the white numbers below the squares. (cf below). On the left is also a snap of the initial game, whereas the game's dynamic is on the right. 

<p align="center">
<img alt="production map" src="https://user-images.githubusercontent.com/15527397/30869351-299bd8c2-a2e1-11e7-80d2-62699551aaa2.png" height="190" width="32%">

<img height="190" width="32%" src="https://user-images.githubusercontent.com/15527397/30869356-2bce1fce-a2e1-11e7-86e6-339335636e0e.gif"></p>

This production map production is invariant over time, and is an information we should use to train our agent. Since we are interesting in maximizing our production, we should intuitively train our agent to target the squares with a high production rate.

On the other hand, we should also consider the strength map, since squares with low strength are easier to conquer.

> To conquer a square, we must move in its direction having a strictly superior strength (action = NORTH, SOUTH, EAST, WEST)

<p align="center"><img height="190" width="32%" src="https://user-images.githubusercontent.com/15527397/30869359-2e235f3c-a2e1-11e7-87ce-109ea5c08c27.gif"></p>

### The Agent

We will teach our agent with:

- The successive Game States.
- The agent's Moves (initially random).
- The corresponding Reward for each Move.

For now, the Game State is a (3 * 3) * 3 matrix (width * height) * n_features, the features being:

- The Strength of the Square
- The Production of the Square
- The Owner of the Square

<p align="center">
<img alt="matrix" src="https://user-images.githubusercontent.com/15527397/30869363-30c46a56-a2e1-11e7-8882-1c22bc2256f8.png" height="220" width="32%">

<img height="220" width="32%" src="https://user-images.githubusercontent.com/15527397/30869368-32e9be94-a2e1-11e7-831e-3d74b19981a4.gif"></p>

<br>
As for the reward, we focus on the production. Since each square being conquered increase the total production of our land, the action leading to the conquest is rewarded according to the production rate of the conquered square. This strategy will best reward the conquest of highly productive squares.

<p align="center"><img height="190" width="32%" src="https://user-images.githubusercontent.com/15527397/30869372-363a5c7a-a2e1-11e7-8784-9a83d4c62c44.gif"></p>
 
We train over 500 games and get significant improvements of the total reward obtained over time.

<p align="center">
<img alt="screen shot 2017-09-26 at 17 34 04" src="https://user-images.githubusercontent.com/15527397/30869383-3e046b94-a2e1-11e7-91c7-ecf2381eb83f.png" height="190" width="32%">
</p>

On the right, you can observe the behaviour of the original, untrained bot, with random actions, whereas on the right, you can see the trained bot.

<p align="center">
<img height="190" width="32%" src="https://user-images.githubusercontent.com/15527397/30869385-3fd296e4-a2e1-11e7-81f7-3a9436740792.gif">
<img height="190" width="32%" src="https://user-images.githubusercontent.com/15527397/30869390-41fe0d22-a2e1-11e7-9205-88fd2c47a544.gif">
</p>



