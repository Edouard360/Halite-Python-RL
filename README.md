# Halite-Python-RL

<p align="center"> <b> Halite Challenge Overview </b> <br> <a href="https://halite.io/" target="_blank"><img width="480" src="https://user-images.githubusercontent.com/15527397/30818756-c0526c06-a21c-11e7-95a8-317dded1e761.gif"></a></p>

## Artificial Intelligence & Reinforcement Learning

### Teaser

Halite is an open source artificial intelligence programming challenge, created by <a href="https://www.twosigma.com/">Two Sigma</a>, where players build bots using the coding language of their choice to battle on a two-dimensional virtual board. The last bot standing or the bot with all the territory wins. Victory will require micromanaging of the movement of pieces, optimizing a bot’s combat ability, and braving a branching factor billions of times higher than that of Go.

### Rules

Each player starts with a single square, and is given information about the surrounding squares to conquer. Each of these squares have a given strength - pink number in the image below, and also represented by the size of the square.

<img align="center" width="480" src="https://user-images.githubusercontent.com/15527397/30821143-9bec343e-a224-11e7-8087-2463d4489475.png">

The origin square itself has a strength.

<img align="center" width="480" src="https://user-images.githubusercontent.com/15527397/30821163-b0d70cf2-a224-11e7-9fbc-e1ff483f53b8.png">

To conquer a adjacent square, the player must have sufficient strength. The remaining strength is afterwards reduced. 

<img align="center" width="480" src="https://user-images.githubusercontent.com/15527397/30821191-c79c6b30-a224-11e7-9ec3-0a9314f2d12d.png">

Each square **possessed by a player** can gain strength at each turn according to a production map

<img align="center" width="480" src="https://user-images.githubusercontent.com/15527397/30821225-dcadd946-a224-11e7-829c-5d3b700c008c.png">

But beware, only a square that doesn't attack an adjacent square increases its strength.

To conquer the map **as fast as possible**, we need to attack the squares with a **high production rate** and a **weak strength**.

### Reinforcement Learning strategy
 
We will try to teach our Bot to expand quickly using **rewards associated with the production rate of the squares**.



