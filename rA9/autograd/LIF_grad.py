from jax import jit
from jax import grad
import jax.numpy as jnp


def lif_grad(grad_output, *args):
    def grad(grad_output, weights, spike_list, time_step, Vth, gamma, tau_m):
        return jnp.multiply(
            jnp.matmul(weights, grad_output),
            jnp.multiply(
                (1 / Vth),
                (1 + jnp.multiply(
                    jnp.divide((1, gamma), jnp.multiply(jnp.exp(jnp.divide(jnp.subtract(time_step, spike_list), tau_m)),
                                                        (-1 / tau_m)))
                )
                 )
            )
        )

    return jit(grad)(grad_output, *args)


def loss_grad(input, target, timestep):
    def np_fn(input, target):
        return jnp.multiply(0.5,jnp.sum(jnp.square(jnp.argmax(input) - target.T)))

    return (grad(np_fn)(input, target)) / timestep


def elementwise_grad(fun, x, initial_grad=None):
    grad_fun = grad(fun, initial_grad, x)
    return grad_fun
