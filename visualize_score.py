import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rewards = [np.load('./models/vanilla.npy')]

max_len = max([len(reward) for reward in rewards])
for i in range(len(rewards)):
    rewards[i] = np.append(rewards[i],np.repeat(np.nan,max_len-len(rewards[i])))

pd.DataFrame(np.array(rewards).T, columns=['vanilla']).rolling(100).mean().plot(title="Weighted reward at each game. (Rolling average)")

plt.show()