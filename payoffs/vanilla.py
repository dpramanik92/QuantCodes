import numpy as np

class vanilla:
    def payoff(self,x,K):
        return max(x-K,0)
