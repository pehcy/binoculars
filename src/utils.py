import numpy as np
import math

def sigmoid(z):
    g = 1 / (1 + np.exp(np.negative(z)))
    return g

def z_scaler(data):
    """
    Rescaling the data to reasonable interval

    Arg:
     data:  ndarray (n,)
    """
    mu = np.mean(data)
    stddev = np.sqrt(np.var(data))
    return (data - mu) / stddev

def compute_cost(X, y, w, b):
    m, n = X.shape
    
    z = np.matmul(X,w) + b
    f_wb = sigmoid(z)
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


def gradient_descent(X, y, w_in, b_in, cost_function, gradient_function, alpha, num_iters, lambda_): 
    """
    Performs batch gradient descent to learn theta. Updates theta by taking 
    num_iters gradient steps with learning rate alpha
    
    Args:
      X :    (array_like Shape (m, n)
      y :    (array_like Shape (m,))
      w_in : (array_like Shape (n,))  Initial values of parameters of the model
      b_in : (scalar)                 Initial value of parameter of the model
      cost_function:                  function to compute cost
      alpha : (float)                 Learning rate
      num_iters : (int)               number of iterations to run gradient descent
      lambda_ (scalar, float)         regularization constant
      
    Returns:
      w : (array_like Shape (n,)) Updated values of parameters of the model after
          running gradient descent
      b : (scalar)                Updated value of parameter of the model after
          running gradient descent
    """
    
    # number of training examples
    m = len(X)
    
    # An array to store cost J and w's at each iteration primarily for graphing later
    J_history = []
    w_history = []
    
    for i in range(num_iters):

        # Calculate the gradient and update the parameters
        dj_db, dj_dw = gradient_function(X, y, w_in, b_in, lambda_)   

        # Update Parameters using w, b, alpha and gradient
        w_in = w_in - alpha * dj_dw               
        b_in = b_in - alpha * dj_db              
       
        # Save cost J at each iteration
        if i<100000:      # prevent resource exhaustion 
            cost =  cost_function(X, y, w_in, b_in, lambda_)
            J_history.append(cost)

        # Print cost every at intervals 10 times or as many iterations if < 10
        if i% math.ceil(num_iters/10) == 0 or i == (num_iters-1):
            w_history.append(w_in)
            print(f"Iteration {i:4}: Cost {float(J_history[-1]):8.2f}   ")
        
    return w_in, b_in, J_history, w_history #return w and J,w history for graphing


def compute_cost_reg(X, y, w, b, lambda_ = 1):
    """
    Computes the cost over all examples
    Args:
      X : (array_like Shape (m,n)) data, m examples by n features
      y : (array_like Shape (m,)) target value 
      w : (array_like Shape (n,)) Values of parameters of the model      
      b : (array_like Shape (n,)) Values of bias parameter of the model
      lambda_ : (scalar, float)    Controls amount of regularization
    Returns:
      total_cost: (scalar)         cost 
    """

    m, n = X.shape
    
    # Calls the compute_cost function that you implemented above
    cost_without_reg = compute_cost(X, y, w, b)

    reg_cost = 0.
    reg_cost = np.sum(np.square(w))
    
    # Add the regularization cost to get the total cost
    total_cost = cost_without_reg
    #total_cost = cost_without_reg + (lambda_/(2 * m)) * reg_cost

    return total_cost


def compute_gradient_reg(X, y, w, b, lambda_ = 1): 
    """
    Computes the gradient for linear regression 
 
    Args:
      X : (ndarray Shape (m,n))   variable such as house size 
      y : (ndarray Shape (m,))    actual value 
      w : (ndarray Shape (n,))    values of parameters of the model      
      b : (scalar)                value of parameter of the model  
      lambda_ : (scalar,float)    regularization constant
    Returns
      dj_db: (scalar)             The gradient of the cost w.r.t. the parameter b. 
      dj_dw: (ndarray Shape (n,)) The gradient of the cost w.r.t. the parameters w. 

    """
    m, n = X.shape
    
    dj_db, dj_dw = compute_gradient(X, y, w, b)
    # dj_dw = dj_dw + np.dot(lambda_ / m, w)
    
    return dj_db, dj_dw


def map_feature(X1, X2):
    """
    Map features using polynomial with degree=8 
    """
    X1 = np.atleast_1d(X1)
    X2 = np.atleast_1d(X2)
    degree = 8
    out = []
    for i in range(1, degree+1):
        for j in range(i + 1):
            out.append((X1**(i-j) * (X2**j)))
    return np.stack(out, axis=1)


def plot_decision_boundary(ax, w, b, X, y):
    # Credit to dibgerge on Github for this plotting code
    
    if X.shape[1] <= 2:
        plot_x = np.array([min(X[:, 0]), max(X[:, 0])])
        plot_y = (-1. / w[1]) * (w[0] * plot_x + b)
        
        ax.plot(plot_x, plot_y, c="b")
        
    else:
        u = np.linspace(-8, 8, 200)
        v = np.linspace(-8, 8, 200)
        
        z = np.zeros((len(u), len(v)))

        # Evaluate z = theta*x over the grid
        for i in range(len(u)):
            for j in range(len(v)):
                z[i,j] = sigmoid(np.dot(map_feature(u[i], v[j]), w) + b)
        
        # important to transpose z before calling contour       
        z = z.T
        
        # Plot z = 0.5
        ax.contour(u,v,z, levels = [0.45], colors="g")


def predict(X, w, b):
    """
    Predict whether the label is 0 (loss) or 1 (gain) using 
    learned logistic regression on weight vector w

    Args:
    X : (ndarray Shape (m, n))
    w : (array_like_Shape (n,))     Parameters of the model
    b : (scalar, float)             Parameter of the model
    
    Returns:
    p : (ndarray (m,1))
        The probability for X using a threshold at 0.5
    """
    m, n = X.shape
    p = np.zeros(m)

    f_wb = sigmoid(np.matmul(X,w) + b)
    p = np.where(f_wb >= 0.5, 1, 0)

    return p