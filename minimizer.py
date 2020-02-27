import scipy.optimize as spo

def f(x):
     y = (x - 1.5) ** 2 + 0.5
     print("X = {}, Y ={}".format(x, y))
     return y

if __name__ == "__main__":
    print("Optimizing ", f)
    minimized = spo.minimize(f, 2.0, method="SLSQP", options={'disp': True})
    print("Printing the results of the minimization")
    print(minimized.x)
    print(minimized.fun)
