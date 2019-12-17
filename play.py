from tictactoe import GameState
import numpy as np
import random
from pprint import pprint


# sorry for this mess...
# this is just to make tensorflow shut up
# about those stupid deprecation warnings
# this needs to be in a particular order
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.get_logger().setLevel('INFO')
import tensorflow.python.util.deprecation as deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False
from tensorflow import keras

# load the model
print("Loading model ...")
model = keras.models.load_model("model.h5")
print("Done.\n")

# helper function
def predict(g : GameState):
    a,b,c = model.predict(np.array([g.board]))[0]    
    return a * -1 + b * 0 + c * 1

# initial state
g = GameState()

# just help the human see the move numbers
print("""
0 1 2
3 4 5
6 7 8
""")

# the huamn goes first with 0.5 probability
players = random.choice([
    {1: "human", 0: "draw", -1: "bot"},
    {-1: "human", 0: "draw", 1: "bot"}
])

while g.winner() is None:
    if players[g.turn()] == "human":
        g = g.playHumanMove()
    else:
        g = g.playBotMove(predict)

g.print()

print("The winner is: ", players[g.winner()])
