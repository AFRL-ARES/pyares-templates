#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# *** Simple Single File PyAres Planner Template ***

# -----------------------------------------------------------------------------
# 1. Import Necessary Modules
# -----------------------------------------------------------------------------
from PyAres import AresPlannerService, PlanRequest, PlanResponse, AresDataType,Outcome # Required for the PyAres Service
import numpy as np # For example logic, feel free to delete if not needed

# -----------------------------------------------------------------------------
# 2. Define Your Service Details 
# -----------------------------------------------------------------------------
name = "<The name of your Planner>"
description = "<Description of your Planner>"
version = "<X.X.X>" # Planner version numbering that will be reported to ARES OS.
port =  7305 # The network port your Planner will use to communicate with ARES OS.
local = True # Whether to use localhost or not

# ----------------------------------------------------------------------------- 
# 3. Define the Planning Logic
# -----------------------------------------------------------------------------
# NOTE: In this example, the planner generates a random number in the bounds supplied with the planning parameters sampling from either a uniform or normal distribution 
def plan(bounds,type='normal'):
    out = []
    for i in bounds:
        min = i[0]
        max = i[1]
        if type == 'normal':
            # If normal, standard devation is set such that the min/max are 3 standard deviations away from the mean
            val = np.inf
            while val > max or val < min
                val = np.random.normal((max-min)/2,(max-min)/6)
        
        elif type =='uniform':
            val = np.random.uniform(min,max)

        out.append(val)
    
    return out


# -----------------------------------------------------------------------------
# 4. Define Planner Function.
# -----------------------------------------------------------------------------
# This function handles the "plumbing" of passing data to an from the ARES PlanRequest to the actual planning logic
def planner(request: PlanRequest) -> PlanResponse:
    parameter_names = [] 
    bounds = []
    try:
        dist_type = request.settings.get('Distribution')
        for param in request.parameters:
            parameter_names.append(param.name)
            bounds.append((param.minimum_value,param.maximum_value))

            '''
            In a real planner, you would probably want to know what the analysis values were and what previously planned values were
            they can be accessed with:
            Analysis results: request.analysis_results (returns a list of past analsysis results)
            Previous planning param.param_history (returns a list of param history objects with the values "planned_value" and "acheived_value". Acheived value is not used unless specified in the ARES OS campaign designer) 
            '''

        new_values = plan(bounds,dist_type)

        response = PlanResponse(parameter_names=parameter_names, parameter_values=new_values,planning_outcome=Outcome.SUCCESS)

    except Exception as e:
        parameter_names = [p.name for p in request.parameters]
        response = PlanResponse(parameter_names=parameter_names,parameter_values=[-1]*len(parameter_names),planning_outcome=Outcome.FAILURE)
    return response

# -----------------------------------------------------------------------------
# 4. Configure and Start Analyzer Service.
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    planner_service = AresPlannerService(planner,
                                         name,
                                         version,
                                         description, 
                                         use_localhost=local, 
                                         port=port)
    """
    Example planner that randomly perturbs each paramter within the parameter bounds

    Analyzer Settings are:
    1. Setting 1 - key: "Distribution" description: "What kind of distribution to sample from"

    Ensure that all your inputs have the appropriate data type(s) specified.
    See the PyAres documentation for more detial on data types


    """
    planner_service.add_supported_type(AresDataType.NUMBER)

    # Note that setting names are case sensitive in this example
    planner_service.add_setting("Distribution", AresDataType.STRING,constraints=['normal','uniform'])

    planner_service.start()
