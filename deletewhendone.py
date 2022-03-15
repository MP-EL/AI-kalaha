from cmath import nan
import numpy as np
from timeit import default_timer as timer
x = []
y = []
for i in range(10):
    x_column = []
    y_column = []
    for i in range(3):
        start_time = timer()


        end_timer = timer()
        x_column.append(end_timer-start_time)
    
    x.append(x_column)

    y.append([i for i in range(len(x_column))])
print(y)

