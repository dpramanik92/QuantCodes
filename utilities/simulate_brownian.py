import numpy as np
import pandas as pd

class Brownian:
    def __init__(self,**kwargs):
        pass 

    def __generate_step(self):
        return np.random.normal(0,1)

    def generate_path(self,steps=100):
        x = [0.0]
        for i in range(1,steps):
            x.append(x[i-1]+self.__generate_step())
            return x

    def run_simulation(num_simulation=1000,steps=100):
        y = []
        for i in range(num_simulation):
            y.append([self.generate_path(steps)])

        return y

