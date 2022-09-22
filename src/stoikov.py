# avellaneda-stoikov model
import numpy as np
import random
import math

class ASmodel:
    def __init__(self, S0, step) -> None:
        self.S0 = S0
        self.T = 1          # end time
        self.sigma = 2
        self.gamma = 0.1    # risk aversion
        self.M = step
        self.dt = self.T / step
        self.k = 1.5
        self.A = 140
    
    ## reservation price:
    ## r(s,t) = s - q * gamma * sigma^2 * (T-t)
    def get_reservation_price(s, q, t, T, gamma, sigma):
        return s - q * gamma * math.pow(sigma, 2) * (T - t)

    def compute_optimal_spread(self):
        S = np.zeros((self.M+1,1))
        b = np.zeros((self.M+1,1))
        a = np.zeros((self.M+1,1))
        reserve_prices = np.zeros((self.M+1,1))
        spread = np.zeros((self.M+1,1))
        delta_b = np.zeros((self.M+1,1))
        delta_a = np.zeros((self.M+1,1))
        q = np.zeros((self.M+1,1))
        w = np.zeros((self.M+1,1))

        b[0] = self.S0
        reserve_prices[0] = self.S0

        z = np.random.standard_normal(200)

        for t in range(1, self.M+1):
            S[t] = S[t-1] + self.sigma * math.sqrt(self.dt) * z[t]
            reserve_prices[t] = S[t] - q[t-1] * self.gamma * (self.sigma ** 2) * \
                                (self.T - t/float(self.M))
            spread[t] = self.gamma * (self.sigma ** 2) * (self.T - t/float(self.M)) + \
                        (2 / self.gamma) * math.log(1 + self.gamma / self.k)
            b[t] = reserve_prices[t] - 0.5 * spread[t]
            a[t] = reserve_prices[t] + 0.5 * spread[t]

            delta_b = S[t] - b[t]
            delta_a = a[t] - S[t]

            lambda_a = self.A * np.exp(-self.k * delta_a[t])
            prob_a = lambda_a * self.dt
            fa = random.random()

            lambda_b = self.A * np.exp(-self.k * delta_b[t])
            prob_b = lambda_b * self.dt
            fb = random.random()

        print("result")

if __name__ == "__init__":
    as_model = ASmodel(1000, 200)
    as_model.compute_optimal_spread()