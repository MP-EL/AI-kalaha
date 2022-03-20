# AI-kalaha

To run 2 minimax against eachother with specified depths:
```
python3 kalaha_new.py 3 3 --d1=6 --d2=4 --rounds=20
```
To run human vs minimax:
```
python3 kalaha_new.py 0 3 --d2=4 -v
```
otherwise see python3 kalaha_new.py -h for more options

Beware alpha-beta pruning is disabled from standard the flag -p=True needs to be included when running the AI.
