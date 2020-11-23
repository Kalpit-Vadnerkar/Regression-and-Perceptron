# learning.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to Clemson University and the authors.
# 
# Authors: Pei Xu (peix@g.clemson.edu) and Ioannis Karamouzas (ioannis@g.clemson.edu)
'''
Project 5 - Linear Regression and Binary Perceptron

Team Members:
    1. Kalpit Vadnerkar
    2. Dhananjay Nikam
'''



"""
In this assignment, you will implement linear and logistic regression
using the gradient descent method, as well as the binary perceptron algorithm. 
To complete the assignment, please modify the linear_regression(), binary_perceptron(), 
and logistic_regression() functions. 

The package `matplotlib` is needed for the program to run.
You should also use the 'numpy' library to vectorize 
your code, enabling a much more efficient implementation of 
linear and logistic regression. You are also free to use the 
native 'math' library of Python. 

All provided datasets are extracted from the scikit-learn machine learning library. 
These are called `toy datasets`, because they are quite simple and small. 
For more details about the datasets, please see https://scikit-learn.org/stable/datasets/index.html

Each dataset is randomly split into a training set and a testing set using a ratio of 8 : 2. 
You will use the training set to learn a regression model. Once the training is done, the code
will automatically validate the fitted model on the testing set.  
"""

# use math and/or numpy if needed
import math
import numpy as np


def linear_regression(x, y, logger=None):
    """
    Linear regression using full batch gradient descent.
    A 1D array w should be returned by this function such that given a
    sample x, a prediction can be obtained by x^T w, where x is a column vector. 
    The intercept term can be ignored due to that x has been augmented by adding '1' as an extra feature. 
    You should use as learning rate alpha=0.0001. If you scale the cost function by 1/#samples, use alpha=0.001  

    Parameters
    ----------
    x: a 2D array of size [N, f+1]
       where N is the number of samples, f is the number of features
    y: a 1D array of size [N]
       It contains the target value for each sample in x
    logger: a logger instance for plotting the loss
       Usage: logger.log(i, loss) where i is the number of iterations
       Log updates can be performed every several iterations to improve performance.
    
    Returns
    -------
    w: a 1D array
       linear regression parameters
    """
    def Cost(Y, H):
        #return 0.5 / Y.shape[0] * np.sum(np.square(H - Y))
        return 0.5 * np.sum(np.square(H - Y))
    
    X = np.array(x)
    Y = np.array(y).reshape((len(y), 1))
    w = np.zeros((X.shape[1], 1))
    alpha = 0.0001
    for i in range(10000):
        H = np.dot(X,w)
        #neww = w - alpha / Y.shape[1] * np.dot(X.T, (H-Y))
        neww = w - alpha * np.dot(X.T, (H-Y))
        logger.log(i, Cost(Y, H))
        if(np.max(abs(neww-w)) <= 1e-4):
            break
        w = neww
    
    print(f'W in the learning.py function = \n{w}\n')
    train_err = 0.5 / Y.shape[0] * np.sum(np.square(np.matmul(X,w) - Y))
    print(f'train error = {train_err}')
    return w

def binary_perceptron(x, y, logger=None):
    """
    Binary classifaction using a perceptron. 
    A 1D array w should be returned by this function such that given a
    sample x, a prediction can be obtained by
        h = (x^T w) 
    with the decision boundary:
        h >= 0 => x in class 1
        h < 0  => x in class 0
    where x is a column vector. 
    The intercept/bias term can be ignored due to that x has been augmented by adding '1' as an extra feature. 
    
    
    Parameters
    ----------
    x: a 2D array with the shape [N, f+1]
       where N is the number of samples, f is the number of features
    y: a 1D array with the shape [N]
       It is the ground truth value for each sample in x
    logger: a logger instance through which plotting loss
       Usage: Please do not use the logger in this function.
    
    Returns
    -------
    w: a 1D array
       binary perceptron parameters
    """
    X = np.array(x)
    Y = np.array(y).reshape((len(y), 1))
    _,features = x.shape
    w = np.zeros(features)
    #Y_hat = np.zeros(Y.shape)
    #while (not np.array_equal(Y,Y_hat)):
     #   for i in range(X.shape[0]):
      #      xi = X[i].reshape((1,X[i].shape[0]))
       #     prod =np.matmul(xi, w)
        #    Y_hat[i] = 1 if(prod >= 0) else 0
         #   if Y_hat[i] != Y[i]:
          #      w = w + ((Y[i] - Y_hat[i]) * xi.T)
    return w.tolist()


def logistic_regression(x, y, logger=None):
    """
    Logistic regression using batch gradient descent.
    A 1D array w should be returned by this function such that given a
    sample x, a prediction can be obtained by p = sigmoid(x^T w)
    with the decision boundary:
        p >= 0.5 => x in class 1
        p < 0.5  => x in class 0
    where x is a column vector. 
    The intercept/bias term can be ignored due to that x has been augmented by adding '1' as an extra feature. 
    In gradient descent, you should use as learning rate alpha=0.001    

    Parameters
    ----------
    x: a 2D array of size [N, f+1]
       where N is the number of samples, f is the number of features
    y: a 1D array of size [N]
       It contains the ground truth label for each sample in x
    logger: a logger instance for plotting the loss
       Usage: logger.log(i, loss) where i is the number of iterations
       Log updates can be performed every several iterations to improve performance.
        
    Returns
    -------
    w: a 1D array
       logistic regression parameters
    """
    def Calculate_H(X, W):
        Z = np.dot(X, W)
        H = 1 / (1 + np.exp(-Z))
        H = np.where(H >= 0.5, 1, 0)
        return H

    def Cost(Y, H):
        Cost = (Y * np.log(H, where = H>0)) + ((1 - Y) * np.log(1 - H, where = (1 - H)>0))
        J = - np.sum(Cost)/Cost.shape[0]
        return J
    
    alpha = 0.001
    iterations = 10000
    X = np.array(x)
    Y = np.array(y).reshape((len(y), 1))
    w = np.zeros((X.shape[1], 1))
    for i in range(iterations):
        H = Calculate_H(X, w)
        neww = w - (alpha * (np.dot((H - Y).T, X).T)/Y.shape[0])
        if not i%100:
            logger.log(i,Cost(Y, H))
        if(np.max(abs(neww-w)) <= 1e-4):
            break
        w = neww
    return w



if __name__ == "__main__":
    import os
    import tkinter as tk
    from app.regression import App

    import data.load
    dbs = {
        "Boston Housing": (
            lambda : data.load("boston_house_prices.csv"),
            App.TaskType.REGRESSION
        ),
        "Diabetes": (
            lambda : data.load("diabetes.csv", header=0),
            App.TaskType.REGRESSION
        ),
        "Handwritten Digits": (
            lambda : (data.load("digits.csv", header=0)[0][np.where(np.equal(data.load("digits.csv", header=0)[1], 0) | np.equal(data.load("digits.csv", header=0)[1], 1))],
                      data.load("digits.csv", header=0)[1][np.where(np.equal(data.load("digits.csv", header=0)[1], 0) | np.equal(data.load("digits.csv", header=0)[1], 1))]),
            App.TaskType.BINARY_CLASSIFICATION
        ),
        "Breast Cancer": (
            lambda : data.load("breast_cancer.csv"),
            App.TaskType.BINARY_CLASSIFICATION
        )
     }

    algs = {
       "Linear Regression (Batch Gradient Descent)": (
            linear_regression,
            App.TaskType.REGRESSION
        ),
        "Logistic Regression (Batch Gradient Descent)": (
            logistic_regression,
            App.TaskType.BINARY_CLASSIFICATION
        ),
        "Binary Perceptron": (
            binary_perceptron,
            App.TaskType.BINARY_CLASSIFICATION
        )
    }

    root = tk.Tk()
    App(dbs, algs, root)
    tk.mainloop()
