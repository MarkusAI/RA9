import math
import numpy as jnp
from rA9.synapses.img2col import *

from rA9.networks.module import Module
from jax import random


# 대가리 깨져도 elementgradient
class Conv2d(Module):

    def __init__(self, input_channels, output_channels, kernel_size, stride=1, padding=0):
        super(Conv2d, self).__init__()
        self.input_channels = input_channels
        self.output_channels = output_channels
        self.kernel_size = (kernel_size, kernel_size)
        self.stride = stride
        self.padding = padding

        self.weight = jnp.zeros((output_channels, input_channels) + self.kernel_size)

        self.bias = jnp.zeros((self.output_channels, 1))

        self.reset_parameters()

    def reset_parameters(self):
        n = self.input_channels
        for k in self.kernel_size:
            n *= k
        stdv = 1. / math.sqrt(n)

        keyW = random.PRNGKey(0)

        self.weight = random.uniform(minval=-stdv, maxval=stdv, shape=self.weight.shape, key=keyW)

    def forward(self, input):

        def jnp_fn(input_jnp, weights_jnp, bias=None, stride=1, padding=0):

            n_filters, d_filter, h_filter, w_filter = weights_jnp.shape
            n_x, d_x, h_x, w_x = input_jnp.shape
            h_out = (h_x - h_filter + 2 * padding) / stride + 1
            w_out = (w_x - w_filter + 2 * padding) / stride + 1

            if not h_out.is_integer() or not w_out.is_integer():
                raise Exception('Invalid output dimension!')  # 오류 체크
            h_out, w_out = int(h_out), int(w_out)
            X_col = im2col_indices(input_jnp, h_filter, w_filter, padding=padding, stride=stride)
            W_col = weights_jnp.reshape(n_filters, -1)

            out = jnp.matmul(W_col, X_col)


            out = out.reshape(n_filters, h_out, w_out, n_x)
            out = jnp.transpose(out, (3, 0, 1, 2))

            if bias is None:
                return out
            else:
                return out

        self.jnp_args = (input, self.weights)

        output=jnp_fn(*self.jnp_args)

        return output


    def backward(self, grad_outputs):

        jnp_fn = self.jnp_fn
        jnp_args = self.jnp_args
        indexes = [index for index, need_grad in enumerate(self.needs_input_grad) if need_grad]

        jnp_grad_fn = elementwise_grad(jnp_fn, indexes, grad_outputs)
        grads = jnp_grad_fn(*jnp_args)
        return grads
