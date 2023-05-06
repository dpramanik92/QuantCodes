import numpy as np
import matplotlib.pyplot as plt

class pathSimulator:
    def __init__(self,**kwargs):
        self.start_pt = kwargs.get('start')
        self.num_path = kwargs.get('num')
        self.model = kwargs.get('model')
        self.length = kwargs.get('length')
        
    def generate_path(self):
        _path = []
        x = self.start_pt
        if self.model == None:
            for i in range(self.length):
                x1 = x + np.random.normal(0,1)
                _path.append(x)
                x = x1
        else:
            for i in range(self.length):
                x1 = x + self.model.generate_step()
                _path.append(x)
                x = x1
        return _path 
    
    def plot_path(self):
        _path = self.generate_path()
        fig,ax = plt.subplots()
        ax.plot(_path)
        
    def run_simluation_path(self):
        paths = []
        
        for i in range(self.num_path):
            paths.append(self.generate_path())
            
        return paths
    
    def run_simulation_end(self):
        paths = []
        
        for i in range(self.num_path):
            paths.append(self.generate_path()[-1])
        
        self.paths = paths
        return paths
    
    def plot_all(self):
        fig,ax = plt.subplots()
        paths = self.run_simluation_path()
        for path in paths:
            ax.plot(path)
            
class priceOption(pathSimulator):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.rate = kwargs.get('rate')
        self.payoff_model = kwargs.get('payoff_model')
        
    def payoff_func(self,x,K):
        if self.payoff_model == None:
            return max(x-K,0)
        else:
            return self.payoff_model.payoff(x,K)
    
    def call_price(self,K):
        y = []
        for i in self.paths:
            y.append(self.payoff_func(i,K))

        y = np.array(y)
        c = sum(y*np.exp(-0.03/12*3.0))/10000
        return c
    
