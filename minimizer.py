import scipy.optimize as spo
import numpy as np

def generate_data(slope, intercept):
    print("Original slope {}".format(slope))
    print("Original Intercept {}".format(intercept))
    x = np.linspace(1, 100, 50).reshape(50, 1)
    y = slope * x + intercept
    return np.concatenate((x, y), axis=1)

def squared_error_sum(line, data):
    return np.sum((data[:,1] - (data[:, 0] * line[0] +  line[1])) ** 2) 

def fit_line(data, error_function):
    initial = np.float32([0, np.mean(data[:, 1])])
    # minimizer will pass initial as the first argument into error_function
    return spo.minimize(error_function, initial, args=(data, ), method="SLSQP", options={'disp': True})


if __name__ == "__main__":
    print("Optimizing a linear relationship")

    # generate random linear data 
    print("Generating random data")
    data = generate_data(5, 3)
    print("Random data generated with size {}".format(data.shape))

    result = fit_line(data, squared_error_sum)

    print("Printing the results of the minimization")
    print(result.x)

    print("The original slope and intercept should be very close to the result's x")
    

