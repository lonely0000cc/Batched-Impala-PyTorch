# TODO model replay

# TODO
# This would be a callback to check the performancesimport random
import numpy as np
import torch
import cv2
from torch.multiprocessing import Process
import os
from math import ceil
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import os

from src.GymEnv import make_env

from src.utils import load_inference

# Define the codec and create VideoWriter object
model = load_inference("checkpoint.pt").float().to("cuda")

env = make_env(game='SuperMarioKart-Snes', state="MarioCircuit.Act3", stacks=1, size=(54, 54), record=True)

step_max = -1 

for i in range(100):
    obs = env.reset()

    done = False
    
    step = 0

    lstm_hxs = [torch.zeros((1, 1, 256)).to("cuda")]*2


    while not done:

        obs_tensor = torch.tensor(obs, dtype=torch.float).float().unsqueeze(0).to("cuda")
        action, _ , lstm_hxs = model.act(obs_tensor, lstm_hxs)
        obs, rew, done, info = env.step(action)

        step += 1
    
    print(step)

    if step > step_max:
        os.rename("record.avi", "best.avi")


env.close()