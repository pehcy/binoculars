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
        avg_spread = []
        profit = []
        std = []

        S = np.zeros((self.M+1,1))
        b = np.zeros((self.M+1,1))
        a = np.zeros((self.M+1,1))
        reserve_prices = np.zeros((self.M+1,1))
        spread = np.zeros((self.M+1,1))
        delta_b = np.zeros((self.M+1,1))
        delta_a = np.zeros((self.M+1,1))
        q = np.zeros((self.M+1,1))
        w = np.zeros((self.M+1,1))
        equity = np.zeros((self.M+1,1))
        reserve_relation = np.zeros((self.M+1,1))

        b[0] = self.S0
        a[0] = self.S0
        S[0] = self.S0
        reserve_prices[0] = self.S0
        spread[0] = 0
        delta_b[0] = 0
        delta_a[0] = 0
        q[0] = 0
        w[0] = 0
        equity[0] = 0

        for t in range(1, self.M+1):
            S[t] = S[t-1] + self.sigma * math.sqrt(self.dt) * np.random.standard_normal()
            reserve_prices[t] = S[t] - q[t-1] * self.gamma * (self.sigma ** 2) * \
                                (self.T - t/float(self.M))
            spread[t] = self.gamma * (self.sigma ** 2) * (self.T - t/float(self.M)) + \
                        (2 / self.gamma) * math.log(1 + self.gamma / self.k)
            b[t] = reserve_prices[t] - 0.5 * spread[t]
            a[t] = reserve_prices[t] + 0.5 * spread[t]

            delta_b[t] = S[t] - b[t]
            delta_a[t] = a[t] - S[t]

            lambda_a = self.A * np.exp(-self.k * delta_a[t])
            prob_a = lambda_a * self.dt
            fa = random.random()

            lambda_b = self.A * np.exp(-self.k * delta_b[t])
            prob_b = lambda_b * self.dt
            fb = random.random()

            if prob_b > fb and prob_a < fa:
                q[t] = q[t-1] + 1
                w[t] = w[t-1] - b[t]
            
            if prob_b < fb and prob_a > fa:
                q[t] = q[t-1] - 1
                w[t] = w[t-1] + a[t]

            if prob_b < fb and prob_a < fa:
                q[t] = q[t-1]
                w[t] = w[t-1]
            
            if prob_b > fb and prob_a > fa:
                q[t] = q[t-1]
                w[t] = w[t-1] - b[t]
                w[t] = w[t] + a[t]

            equity[t] = w[t] + q[t] * S[t]

        avg_spread.append(spread.mean())
        profit.append(equity[-1])
        std.append(equity[-1])

        print("Results: \n")
        print(profit)
        print("%14s %20.5f" % ("Average spread: ", np.array(avg_spread).mean()))

as_model = ASmodel(1000, 200)
as_model.compute_optimal_spread()