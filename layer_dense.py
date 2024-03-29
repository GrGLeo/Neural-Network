#Dense layer
import numpy as np

class Layer_Dense:
    #layer initialization
    def __init__(self,n_inputs,n_neurons,
                 weight_regularizer_l1=0,weight_regularizer_l2=0,
                 bias_regularizer_l1=0,bias_regularizer_l2=0):
        #Initialize weights and biases
        self.weights = 0.01 * np.random.randn(n_inputs,n_neurons)
        self.biases = np.zeros((1,n_neurons))
        #Set regularizer strenght
        self.weight_regularizer_l1 = weight_regularizer_l1
        self.weight_regularizer_l2 = weight_regularizer_l2
        self.bias_regularizer_l1 = bias_regularizer_l1
        self.bias_regularizer_l2 = bias_regularizer_l2

    #Forward pass
    def forward(self,inputs):
        #Calculate the output value from inputs, weights, and biases
        self.inputs = inputs
        self.output = np.dot(inputs, self.weights) + self.biases
        # print(self.weights)

    #Backward pass
    def backward(self,dvalues):
        #Gradients on parameters
        self.dweights = np.dot(self.inputs.T, dvalues)
        self.dbiases = np.sum(dvalues, axis=0,keepdims=True)

        # Gradients on regularization
        # Weights
        if self.weight_regularizer_l1 > 0:
            dL1 = np.ones_like(self.weights)
            dL1[self.weights < 0] = -1
            self.dweights += self.weight_regularizer_l1 * dL1

        if self.weight_regularizer_l2 > 0:
            self.dweights += 2 * self.weight_regularizer_l2 * self.dweights

        # Biases
        if self.bias_regularizer_l1 > 0:
            dL1 = np.ones_like(self.biases)
            dL1[self.biases < 0] = -1
            self.dbiases += self.bias_regularizer_l1 * dL1

        if self.bias_regularizer_l2 > 0:
            self.dbiases += 2 * self.bias_regularizer_l2 * self.biases

        #Gradients on values
        self.dinputs = np.dot(dvalues,self.weights.T)


class Layer_Dropout:
    def __init__(self,rate):
        self.rate = 1 - rate

    def forward(self,inputs):
        self.inputs = inputs
        self.binary_mask = np.random.binomial(1,self.rate, inputs.shape) / self.rate
        self.output = inputs * self.binary_mask

    def backward(self, dvalues):
        self.dinputs = dvalues * self.binary_mask
