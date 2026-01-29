import numpy as np

def perturb(init_value: float, 
            bounds:tuple[float,float], 
            std_dev: float, 
            rng:np.random.Generator = np.random.default_rng()) -> float: 
    # perturbs a value by sampling from a normal distribution, enforcing minimum and maximum value constraints
    min_val = bounds[0]
    max_val = bounds[1]
    
    while True:
        new_val = rng.normal(init_value,std_dev)
        if (min_val <= new_val <= max_val):
            return new_val
        else:
            continue

