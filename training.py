from tictactoe import GameState
from pprint import pprint

# generate actual evaluation values by dfs

values = {}

def value(g: GameState) -> int:
    if g in values:
        return values[g]
    else:
        w = g.winner()
        if w is not None:
            ans = w
        else:
            f = [min, max][g.turn() == 1]
            ans = f(value(n) for n in g.nextStates())
        values[g] = ans
        return values[g]


g = GameState()
value(g)

# =======================================================================

import tensorflow as tf
tf.get_logger().setLevel('INFO')
import tensorflow.python.util.deprecation as deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
import numpy as np
from tensorflow import keras
import tensorflow.keras.backend as K

# make a neural net and train it to learn the evaluation values

print("Enter number of neurons in each layer (comma seperated)",)
print("[Last layer will have 3 neurons]: ",end=" ")

l = map(int, input().split(","))

model = keras.Sequential()

for n in l:
    model.add(keras.layers.Dense(n))
    model.add(keras.layers.Activation("sigmoid"))

model.add(keras.layers.Dense(3))
model.add(keras.layers.Activation("softmax"))

print("Enter learning rate [0.01~0.3]: ",end=" ")

learning_rate = lr = float(input())

model.compile(
    optimizer=keras.optimizers.SGD(lr = learning_rate, decay=2e-4, momentum=0.9, nesterov=True),
    loss='categorical_crossentropy',
    metrics=['categorical_accuracy']
)

data = []
labels = []

for k, v in values.items():
    data.append(k.board)
    labels.append(v)

data = np.array(data)
labels = keras.utils.to_categorical(np.array(labels) + 1)

delta_loss = 1

i = 0

print("Starting training ... \n")

print("Iteration\t\tLoss\t\tAccuracy\tLR\tΔ loss")
print("-"*85)
print("%9d  " % i, end="")
acc = model.evaluate(data, labels, verbose=0)
accuracy = acc[1]
loss = acc[0]
print(" "*10, end="")
print("\t%0.5f\t\t%0.3f %%\t\t%0.5f" % (acc[0], 100*acc[1], lr))

while abs(delta_loss) > 0.00001 or accuracy > 0.99:

    i += 1

    print("%9d  " % i,end="")
    sys.stdout.flush()

    _iter = tf.to_float(model.optimizer.iterations, name='ToFloat')
    _decay = tf.to_float(model.optimizer.decay, name='ToFloat')
    _lr = tf.to_float(model.optimizer.lr, name='ToFloat')
    lr = K.eval(_lr * (1. / (1. + _decay * _iter)))

    for x in range(10):
        model.fit(data, labels, epochs=10, batch_size=5478, verbose=0)
        print(".", end="")
        sys.stdout.flush()
    
    acc = model.evaluate(data, labels, verbose=0)
    delta_loss = loss - acc[0]
    accuracy = acc[1]
    loss = acc[0]
    
    print("\t%0.5f\t\t%0.3f %%\t%0.3f\t%0.5f" % (acc[0], 100*acc[1], lr, delta_loss))
    
    sys.stdout.flush()
    model.save('model.h5')
    
