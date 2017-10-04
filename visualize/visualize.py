import json
import os
import sys
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from train.reward import discountedRewards
from public.models.bot.trainedBot import TrainedBot


@app.route("/")
def home():
    return render_template('visualizer.html')


print("Look at http://127.0.0.1:5000/performance.png for performance insights")


@app.route("/performance.png")
def performance_plot():
    fig = Figure()
    sub1 = fig.add_subplot(111)
    import pandas as pd
    path_to_variables = os.path.abspath(os.path.dirname(__file__)) + '/../public/models/variables/'
    list_variables = [name for name in os.listdir(path_to_variables) if name != "README.md"]
    path_to_npy = [path_to_variables + name + '/' + name + '.npy' for name in list_variables]

    rewards = [np.load(path) for path in path_to_npy]

    max_len = max([len(reward) for reward in rewards])
    for i in range(len(rewards)):
        rewards[i] = np.append(rewards[i], np.repeat(np.nan, max_len - len(rewards[i])))

    pd.DataFrame(np.array(rewards).T, columns=list_variables).rolling(100).mean().plot(
        title="Weighted reward at each game. (Rolling average)", ax=sub1)

    plt.show()
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


def convert(request):
    def get_owner(square):
        return square['owner']

    def get_strength(square):
        return square['strength']

    get_owner = np.vectorize(get_owner)
    get_strength = np.vectorize(get_strength)
    owner_frames = get_owner(request.json["frames"])[:, np.newaxis, :, :]
    strength_frames = get_strength(request.json["frames"])[:, np.newaxis, :, :]
    production_frames = np.repeat(np.array(request.json["productions"])[np.newaxis, np.newaxis, :, :],
                                  len(owner_frames),
                                  axis=0)

    moves = np.array(request.json['moves'])

    game_states = np.concatenate(([owner_frames, strength_frames, production_frames]), axis=1)

    moves = ((-5 + 5 * game_states[:-1, 0, :]) + ((moves - 1) % 5))
    return game_states, moves


@app.route('/post_discounted_rewards', methods=['POST'])
def post_discounted_rewards():
    game_states, moves = convert(request)
    discounted_rewards = discountedRewards(game_states, moves)
    return json.dumps({'discountedRewards': discounted_rewards.tolist()})


@app.route('/post_policies', methods=['POST'])
def post_policies():
    game_states, _ = convert(request)
    bot = TrainedBot()
    policies = np.array([bot.get_policies(game_state) for game_state in game_states])
    return json.dumps({'policies': policies.tolist()})
