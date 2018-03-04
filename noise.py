import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
def add_noise(function, a, b,sample_size,noisyness,noise_shape=np.random.normal):  #add normally distributed noise to a true function
    data_points = [a+float(i)*(b-a)/sample_size for i in range(sample_size)]
    true_points = [function(i) for i in data_points]
    noise = [noisyness*noise_shape() for i in range(len(true_points))]
    with_noise = [sum(i) for i in zip(true_points,noise)]
    plt.plot(data_points, with_noise, 'ro')
    plt.axis([a, b, min(with_noise), max(with_noise)])
    plt.show()
