from jax import jit
import jax.numpy as jnp
from rA9.autograd import Function
from rA9.autograd import Variable


class Output(Function):
    id = "output"

    @staticmethod
    def forward(ctx, input, v_current, tau_m, dt, time_step):
        assert isinstance(v_current, Variable)
        assert isinstance(input, Variable)

        def np_fn(input_np, v_current, time_step, dt, tau_m):
            return (input_np+v_current*jnp.exp(-1/tau_m))/time_step, input_np+v_current*jnp.exp(-1/tau_m)

        def grad_fn(grad_outputs, input, s_time_list, time, tau_m, gamma):
            return (jnp.divide(grad_outputs, time), jnp.matmul(input.T, jnp.divide(grad_outputs, time)))
        
        
        np_args = (input.data, v_current.data, time_step, dt, tau_m)
        out, v_current = jit(np_fn)(*np_args)

        grad_np_args = (input.data, time_step, tau_m, 0, 0)

        id = "output"
        return grad_fn, grad_np_args, out, v_current, id

    @staticmethod
    def backward(ctx, grad_outputs):
        super(Output, Output).backward(ctx, grad_outputs)
