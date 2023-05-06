import numpy as np

class Brownian:
    def __init__(self,**kwargs):
        self.mean = kwargs.get('mean')
        self.sd = kwargs.get('sd')

    def generate_step(self):
        return np.random.normal(self.mean,self.sd)
