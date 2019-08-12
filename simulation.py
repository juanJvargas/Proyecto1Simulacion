import numpy
import math
import matplotlib.pyplot as plt
from scipy.stats import uniform

# number of data
n = 100
# loc value for P1
l1 = 3
# loc value for P2
l2 = 4
# loc value for machine load time
t = 2
# scale value
s = 2
# m intervals 
m = math.sqrt(n)

# pseudorandom numbers from loc to loc+scale for queue P1
p1 = uniform.rvs(loc=l1,scale=s,size=n)
# pseudorandom numbers from loc to loc+scale for queue P2
p2 = uniform.rvs(loc=l2,scale=s,size=n)
# pseudorandom numbers from loc to loc+scale for machine load time
r = uniform.rvs(loc=t,scale=s,size=n)
   
print(p1)
