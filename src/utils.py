import numpy as np
import math

def sigmoid(z):
    g = 1 / (1 + np.exp(np.negative(z)))
    return g

def compute_cost(X, y, w, b):
    m, n = X.shape
    
    z = np.matmul(X,w) + b
    f_wb = sigmoid(z)
    # print(f_wb)
    total_cost = 0

    for i in range(m):
        loss = -y[i] * math.log(f_wb[i]) - (1 - y[i]) * math.log(1 - f_wb[i])
        total_cost += np.sum(loss)
    
    total_cost /= m

    return total_cost

def compute_gradient(X, y, w, b, lambda_=None): 
    """
    Computes the gradient for logistic regression 
 
    Args:
      X : (ndarray Shape (m,n)) variable such as house size 
      y : (array_like Shape (m,1)) actual value 
      w : (array_like Shape (n,1)) values of parameters of the model      
      b : (scalar)                 value of parameter of the model 
      lambda_: unused placeholder.
    Returns
      dj_dw: (array_like Shape (n,1)) The gradient of the cost w.r.t. the parameters w. 
      dj_db: (scalar)                The gradient of the cost w.r.t. the parameter b. 
    """
    m, n = X.shape
    dj_dw = np.zeros(w.shape)
    dj_db = 0.

    z = np.matmul(X,w) + b
    f_wb = sigmoid(z)
    dj_db = 1 / m * np.sum(f_wb - y)
    
    b_i = 0.
    dj_dw = np.dot(1/m, np.matmul(np.transpose(X), f_wb - y))
        
    return dj_db, dj_dw