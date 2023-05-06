from options.price import priceOption
from models.brownian import Brownian
from payoffs.vanilla import vanilla

brown = Brownian(mean=0,sd=1.0)
payoff = vanilla()

one = priceOption(start=100,num=1000,length=100,model=brown,payoff_model=payoff)
x = one.run_simulation_end()
print(one.call_price(70))