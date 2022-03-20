# AI-kalaha

The first 2 arguments are the types of Agents [0: HumanAgent, 1: RandomAgent, 2: MaxAgent, 3: MinimaxAgent]

--d1 or --d2 is the depth of each agent (Only changes something when using 3: MinimaxAgent)

other arguments are 

--rounds or -r, number of games to be played before giving win % for each agent.

--visual or -v, whether or not to show the game states when running.

--pruning or -p, whether or not to use alpha-beta pruning for the Minimax agents

To run 2 minimax against eachother with specified depths:
```
python3 kalaha_new.py 3 3 --d1=2 --d2=4 -r=10 -p
```
To run human vs minimax:
```
python3 kalaha_new.py 0 3 --d2=4 -v -p
```
otherwise see python3 kalaha_new.py -h for more options

Beware alpha-beta pruning is disabled from standard the flag -p=True needs to be included when running the AI.

Also dont choose depths over 6 it takes a long time and you propably wont beat it at 6 :) .
