import jax.numpy as jnp
from .module import Module
from .. import functional as F
from rA9.autograd.variable import Variable


class Output(Module):

    def __init__(self, out_features, tau_m=0.1, dt=1, Vth=1):
        super(Output, self).__init__()
        self.out_features = out_features
        self.v_current = None
        self.tau_m = tau_m
        self.time_step = 1
        self.Vth = Vth
        self.dt = dt

        self.reset_parameters()

    def forward(self, input, time, activetime):
        if activetime == 0:
            self.v_current = Variable(jnp.zeros(shape=(1, self.out_features)))

        out, v_current_ret = F.Output(input=input,
                                      v_current=self.v_current,
                                      tau_m=self.tau_m, dt=self.dt,
                                      time_step=time + self.time_step)
        self.v_current = v_current_ret

        return out, time + self.dt * self.time_step

    def reset_parameters(self):
        pass
