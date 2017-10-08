---
layout: default
title:  "The reward importance"
date:   2017-10-05 16:30:00
categories: main
---

<style type="text/css">
  {% include center.css %}
</style>

# The reward importance

## The impact of the reward choice

We will see how important it is to set a proper reward, playing with two hyperparameters, ie:

* The **discount factor** - for the discounted rewards
* The **reward expression**, as a function of the **production** - the hyperparameter being the function itself

The results of a well-chosen reward can lead to significant improvements ! Our bot, only trained for conquering the map as fast as possible, now systematically wins against the trained bot (that applies heuristics). This is best exemplified by the 3 games below.

<p align="center">
<img height="250" width="250" src="https://user-images.githubusercontent.com/15527397/31232356-f48483b8-a9e9-11e7-8c6a-34b63bcab417.gif">
<img height="250" width="250" src="https://user-images.githubusercontent.com/15527397/31232360-fa4bbac8-a9e9-11e7-8104-19bd49f43b2f.gif">
<img height="250" width="250" src="https://user-images.githubusercontent.com/15527397/31232357-f7ccef06-a9e9-11e7-96fa-286ad9e22aad.gif">
</p>

## Devising the reward

The reward is complex to devise since we take **multiple actions** at each turn, and we have to compute the reward for **each of these individual actions**.

Below is an insightful illustration to understand the process. The number written on each square are **the reward associated with the current action of the square**. Notice that, at each turn, **these reward are different for each square**, and that, when a square is about to conquer another adjacent square, **the reward for its action is high**.

It is even more higher as the square is more productive.

> HINT: highly productive square have a brighter background, and the poorly productive have a darker one.

Observe how the rewards evolve over time: there is already a **discount factor** applied, because we encourage (/reward) action **that will eventually lead to a reward over time**. Indeed, the `STILL` squares are earning rewards !

<br>

<ul class="list-unstyled list-inline text-center">
  <li>
    <img height="400" width="400" alt="reward1" src="https://user-images.githubusercontent.com/15527397/31237067-2b81fb78-a9f6-11e7-8f31-12141c2dba7a.gif">
    <figcaption>Discount = 0.6</figcaption>
  </li>
</ul>

## Understanding the discount factor

To better understand the discount factor, let's push it to its **limits**, and look at the corresponding reward for the exact same game. 

* On the left, notice that when the discount factor is set to 0, only the moves that conquer a square qre rewarded. This means that the `STILL` action for a square never gets rewarded - which is undesirable. 
* On the over end, with a discount rate of 0.9, the rewards tend to be **overall much higher**. Yet this excessively uniform pattern **doesn't favor much the actions that are actually good**. Too many actions are rewarded, even though they were potentially not efficient.
 
As expected, these reward strategies fare badly compared to a more balanced discount factor. See below the comparison.

<ul class="list-unstyled list-inline text-center">
  <li>
    <img height="300" width="300" alt="reward2" src="https://user-images.githubusercontent.com/15527397/31237065-2b6ebc48-a9f6-11e7-8325-39a00c15c138.gif">
    <figcaption>Discount = 0.0</figcaption>
  </li>
  <li>
    <img height="300" width="300" alt="reward3" src="https://user-images.githubusercontent.com/15527397/31237064-2b6dfe0c-a9f6-11e7-8df7-1827b673a778.gif">
    <figcaption>Discount = 0.9</figcaption>
  </li>
</ul>

## Variation of the raw reward

Each reward is computed according to the production of the conquered square, and then "backtracked" to the actions that lead to this reward.

But should this reward be proportional to the production ? Wouldn't it be better to make it **proportional to the square of the production** ? Or even to a higher power ?

Indeed, we want to strongly encourage our bot to conquer highly productive square, and a way to enforce efficiently this learning is by **giving significantly greater rewards for the highly productive square**.

All the example before had reward proportional to the power 4 of the production. But let's look for a **power 2** and a **linear** reward.

<ul class="list-unstyled list-inline text-center">
  <li>
    <img height="300" width="300" alt="reward4" src="https://user-images.githubusercontent.com/15527397/31237063-2b683ce2-a9f6-11e7-9656-3de7e6c743f7.gif">
    <figcaption>Power: 2 (Discount = 0.6)</figcaption>
  </li>
  <li>
    <img height="300" width="300" alt="reward5" src="https://user-images.githubusercontent.com/15527397/31237070-2be72b1a-a9f6-11e7-8964-d352e99a6628.gif">
    <figcaption>Power: 1 (Discount = 0.6)</figcaption>
  </li>
</ul>

### The ratio changes

Let's **extract one frame of the above**. (*see gifs below*) Let's not focus on the absolute value of the rewards, but rather on **the ratio between the rewards of different actions**.

The two actions that we compare here are:

* The square on the top left that conquers its left neighbour (1)
* The square on the bottom right that conquers its above neighbour (2)

We would want action (1) to be better reward than action (2). Indeed look at the background color of the conquered square. The conquered square in (1) is **brighter** than the conquered square in (2) and therefore **more productive**.

In all cases, `reward(1) > reward(2)`. But if we look at the ratio (*see gifs below*), we have, from left to right:

* 0.65/0.24 = 2.7
* 0.93/0.49 = 1.8
* 1.1/0.7 = 1.5

Which illustrates that, the **higher the exponent** for the reward, **the greater the difference between the reward** of good and very good actions.

<ul class="list-unstyled list-inline text-center">
  <li>
    <img height="250" width="250" alt="reward1-bis" src="https://user-images.githubusercontent.com/15527397/31237066-2b7e737c-a9f6-11e7-95d6-47daee50e051.gif">
    <figcaption>Power: 4 (D = 0.6)</figcaption>
  </li>
  <li>
    <img height="250" width="250" alt="reward4-bis" src="https://user-images.githubusercontent.com/15527397/31237068-2b8448f6-a9f6-11e7-8b71-5c54264e7146.gif">
    <figcaption>Power: 2 (D = 0.6)</figcaption>
  </li>
  <li>
    <img height="250" width="250" alt="reward5-bis" src="https://user-images.githubusercontent.com/15527397/31237062-2b3ab4fc-a9f6-11e7-88c9-d0f39e6c9bf6.gif">
    <figcaption>Power: 1 (D = 0.6)</figcaption>
  </li>
</ul>

## The performance

According to the choice of reward, the training can be much slower, or even converge to a worse equilibrium. We should keep this in mind as we explore new strategies in the future.

<br>

<p align="center">
<img width="400" alt="performance" src="https://user-images.githubusercontent.com/15527397/31232668-db0cf324-a9ea-11e7-8f9e-923c582df6e8.png">
</p>

<br>

## Scaling up

What about the results on a larger map ?

Our trained Bot **still wins** all the games against the OpponentBot when we increase the map size.

<ul class="list-unstyled list-inline text-center">
  <li>
    <img height="250" width="250" src="https://user-images.githubusercontent.com/15527397/31232362-fc674822-a9e9-11e7-958f-db34cfafc625.gif">
  </li>
  <li>
    <img height="250" width="250" src="https://user-images.githubusercontent.com/15527397/31232371-fe85eaf0-a9e9-11e7-97d7-dc96a15a7e92.gif">
  </li>
  <li>
    <img height="250" width="250" src="https://user-images.githubusercontent.com/15527397/31232374-00d8f252-a9ea-11e7-82f3-505eb6556029.gif">
  </li>
</ul>

However, we notice that:

* This solution is too long to compute for each square individually
    * Maybe we should only apply it for **the squares on the border** (and find another strategy for the squares in the center)
    * We could gain time if we made **only one call to the tensorflow session**. Besides, the extraction of the local game states would probably be faster on the tensorflow side.
* Squares in the middle have a **suboptimal behaviour** - seems like they tend to move to the left systematically.
