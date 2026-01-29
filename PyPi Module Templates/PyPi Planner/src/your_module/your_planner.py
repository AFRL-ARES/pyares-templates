#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /PyPi Module Templates/PyPi Planner/src/your_module/your_planner.py
# Project: pyares-templates
# Created Date: Thursday, January 29th 2026, 11:08:28 am
# Author(s): Arthur W. N. Sloan
# -----
# MIT License
# 
# Copyright (c) 2026 AFRL-ARES
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
###
from PyAres import PlanRequest, PlanResponse
import numpy as np
from typing import Any
from .support_functions import perturb
# the . in the above import stament tells the code it should look in the local directory
# where it will find the support_functions directory and the associated __init__.py

"""
In general, the planner will not be aware of the dimensionality of the problem it is tyring to solve beforehand.
The actual parameters that it is planning over defined on the ARES OS side and are recieved as part of
the planning request. For some approaches, this can cause some headaches if some settings are specific to some parameters.

For this example we three settings, one of which (foo) is global, while the other two (bar, baz) apply 
only to one parameter. In this case the relationship between the one setting and these parameters 
must be hard coded, with the 'find matching settings' helper function returning the values of 'bar' and 'baz' only 
for the paramter named 'qux'. This will only work propperly if the parameter name 'qux' is correclty configured in ARES OS

"""

def find_matching_setting(param_name: str, settings: dict[str, Any]) -> tuple:
   # This provides a mapping between the parameter names coming from ARES os and the 
   # settings keys defined when the planner service is started
   # Hopefully we will reach a point where this can be handled automatically soon

   maping_dict = {'qux':('bar','baz')}
   param_name = param_name.lower()
   if param_name in maping_dict:
      setting_names = maping_dict[param_name]
      return tuple(settings[i] for i in setting_names)
   else:
      return tuple()

"""
This main planner function is what will be called by the service whenever a request is recieved 
If the logic is simple, it can simply be defined within the main function, but more complex processes
may benefit from being broken out into subfunctions within this file or into other files and subdirectories
with the top level planner function primarily servering to pass data back and forth a mix of both approaches 
is used here for illustrative purposes

"""

def your_planner_function(request: PlanRequest) -> PlanResponse:
    """
    This demo planner perturbs each parameter from its previous value by sampling 
    from a normal distribution with an average of the previous value and a standard deviaiton of 10% of the current value.
    min and max values set within ARES are enforced. 
    the setting 'foo' is global and sets the random number generator seed for repeatable resutls
    the settings 'bar' and 'baz' apply only to the parameter 'qux', with 'bar' being the standard deviaton
    and 'baz' being a multiplicative factor applied after the perturbation
    """

    # Initialize a random number generator with the
    foo:int = int(request.settings['foo'])
    rng = np.random.default_rng(seed=foo)

    # The ARES OS loop always starts with planning, so we need to handle the
    # behavior on the first call where there are no analysis results 
    N_iter = len(request.analysis_results)
    parameter_names : list[str] = []
    new_condition : list[float] = []

    if N_iter == 0:
        for param in request.parameters:
            parameter_names.append(param.name)
            
            if isinstance(param.initial_value, float):
                new_condition.append(param.initial_value)
            else:
                print("Problem trying to access intial value! Value was not of type float.")
                new_condition.append(0.0)
    else:
        for parameter in request.parameters:
            parameter_names.append(parameter.name)
            parameter_bounds = (parameter.minimum_value,parameter.maximum_value)
            parameter_value = float(parameter.param_history[-1].planned_value) 
            # this could also be achived_value if a physical system doesn't always hit a target setpoint.
            p = find_matching_setting(parameter.name,request.settings)
            if len(p) == 2:
               new_condition.append(p[0]*perturb(parameter_value,parameter_bounds,p[1],rng))
            else:
               new_condition.append(perturb(parameter_value,parameter_bounds,0.1*parameter_value,rng))
    return PlanResponse(parameter_names=parameter_names, parameter_values=new_condition)