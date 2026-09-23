#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# *** A simple PyAres device for doing math to values ***

"""
Sometimes it could be nessary to do some math to raw experimental values coming out of ARES Devices
mid-experiment in ways that either can't or shouldn't be built in to an analyzer service. While basic math can be implemented using
custom commands within ARES, more complex operations may be better suited to an external service

By defining multiple functions and command schema you can manage all of the math with a single PyAres device.

Some example use cases for an arithmetic device:

1. Calculating concentration of a flammable species and the necessary dilution 
   flow to dilute the overall gas flow to a safe level in order to set the flow rate on 
   a controler.

2. Calculating the total mass flux of an experiment in order to set the sampling time so each 
   experiment samples the same total mass.

3. Converting a raw experimental value to a log value

"""

# -----------------------------------------------------------------------------
# 1. Import Necessary Modules
# -----------------------------------------------------------------------------
from PyAres import AresDeviceService, DeviceSchemaEntry, DeviceCommandDescriptor, AresDataType # Required for the PyAres Service
import numpy as np
import argparse


# -----------------------------------------------------------------------------
# 2. Define Your Service Details 
# -----------------------------------------------------------------------------
name = "PyAres Math Device"
description = "Implements helper math operations for raw experimental values"
version = "1.0.0" # device version numbering that will be reported to ARES OS.
default_port =  5555 # The network port your device will use to communicate with ARES OS.
default_local = True # Whether to use localhost or not

# ----------------------------------------------------------------------------- 
# 3. Define the math you want to do
# -----------------------------------------------------------------------------

def fractional_compositon(flows) -> list[float]:
    # Calculate the fractional composition from an array of absolute values
    return list(flows/np.sum(flows))

def calculate_dilution_flow(flammable_flow: list[float],
                            inert_flow: list[float],
                            flam_thresh: float = 0.05) -> float:
    # Calculates an supplementarty inert flow rate such that the total fraction of the
    # flammable components is less than the value of flam_thresh (default: 0.05)

    # *** NOTE THAT THIS IS NOT A RIGOROUS FLAMMABILITY/DILUTION FACTOR CALCULATION DO NOT USE FOR LIFE SAFETY***
    total_flammables = np.sum(flammable_flow)
    total_inerts = np.sum(inert_flow)
    flam_frac = total_flammables/(total_flammables+total_inerts)
    if flam_frac <= flam_thresh:
        dilution_flow = 0.0
    else:
        dilution_flow = total_flammables*(1/flam_thresh -1) - total_inerts

    return dilution_flow

def calculate_sample_time(flows:list[float],
                          target_sample_amount: float) -> float:
    # Calculates the required sample time to collect a target amount of sample based on 
    # The experimental flows
    total_flow = np.sum(flows) # In units of amount/time
    sample_time = target_sample_amount/total_flow

    return sample_time # In the time unit of the original flow rate


    return list(np.asarray(x) + offset_value)

def log10_scalar(x:float) -> float:
    return np.log10(x)

def log10_array(x:float) -> list[float]:
    return list(np.log10(x))

def ln_scalar(x:float) -> float:
    return np.log(x)

def ln_array(x:float) -> list[float]:
    return list(np.log(x))

def exp_scalar(x:float) -> float:
    return np.exp(x)

def exp_array(x:float) -> list[float]:
    return list(np.exp(x))

# Pyares Requires these methods be defined 
def safe_mode():
    pass

def get_state():
    return {}
    
# -----------------------------------------------------------------------------
# 4. Configure and Start the service.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog='PyAres_demo_response',
            description='Generates a syntheic process space for sampling with ARES OS',
        )
    parser.add_argument('-p','--port',help='Port to host the planner service on',type=int, default=default_port)
    parser.add_argument('-l','--local',help='Whether to run the service only on localhost', type=bool, default=default_local)
    args = parser.parse_args()

    port = args.port
    local = args.local

    math_service = AresDeviceService(safe_mode,
                                       get_state,
                                       name,
                                       version,
                                       description, 
                                       use_localhost=local, 
                                       port=port)
    
    #%% Configuring input and output schema for the availible commands/math functions
    ### Fractional Compostion Calculation ###
    frac_comp_input = {
        "flows":DeviceSchemaEntry(type=AresDataType.NUMBER_ARRAY,
                                   description="Array of input amounts"),
    }

    frac_comp_output = {
        "fracs":DeviceSchemaEntry(type=AresDataType.NUMBER_ARRAY,
                                   description="Array of fractional compositions"),
    }
    frac_comp_desc = DeviceCommandDescriptor(name="fractional_composition",
                                              description="Calculates the fractional compositon from an array of absolute amounts", 
                                              input_schema=frac_comp_input,
                                              output_schema=frac_comp_output)

    math_service.add_new_command(frac_comp_desc,fractional_compositon)
    
    ### Dilution Flow calculation ###
    dil_flow_input = {
        "flammable_flow":DeviceSchemaEntry(type=AresDataType.NUMBER_ARRAY,
                                   description="Array of input amounts"),
        "inert_flow":DeviceSchemaEntry(type=AresDataType.NUMBER_ARRAY,
                                    description="Array of input amounts"),
        "flam_thresh":DeviceSchemaEntry(type=AresDataType.NUMBER,
                                    description="Allowable flammables concentratation")
    }

    dil_flow_output = {
        "dilution_flow":DeviceSchemaEntry(type=AresDataType.NUMBER,
                                   description="Required Dilution Flow"),
    }

    dil_flow_desc = DeviceCommandDescriptor(name="calculate_dilution_flow",
                                                  description="Calculates the required inert gas flow to dilute flammable species below a threshold value", 
                                                  input_schema=dil_flow_input,
                                                  output_schema=dil_flow_output)
    
    math_service.add_new_command(dil_flow_desc,calculate_dilution_flow)

    ### Sampling Time Calculation ###
    sample_time_input = {
        "flows":DeviceSchemaEntry(type=AresDataType.NUMBER_ARRAY,
                                    description="Array of input amounts"),
        "target_sample_amount":DeviceSchemaEntry(type=AresDataType.NUMBER,
                                    description="amount of sample to collect"),
    }

    sample_time_output = {
        "sample_time":DeviceSchemaEntry(type=AresDataType.NUMBER,
                                    description="Sampling Time"),
    }

    sample_time_desc = DeviceCommandDescriptor(name="calculate_sample_time",
                                                    description="Calculates the sampling time for a target amount based on an array of flows", 
                                                    input_schema=sample_time_input,
                                                    output_schema=sample_time_output)
    
    math_service.add_new_command(sample_time_desc,calculate_sample_time)

    ### Log & exp functions ###
    scalar_input_output = {
        "x":DeviceSchemaEntry(type=AresDataType.NUMBER,
                              description="A scalar value"),
    }

    array_input_output = {
        "x":DeviceSchemaEntry(type=AresDataType.NUMBER_ARRAY,
                                description="An array of values"),
    }

    log10_scalar_desc = DeviceCommandDescriptor(name="log10_scalar",
                                                description="Returns the log10 of the input value", 
                                                input_schema=scalar_input_output,
                                                output_schema=scalar_input_output)
    log10_array_desc = DeviceCommandDescriptor(name="log10_array",
                                                description="Returns the log10 of the input values", 
                                                input_schema=array_input_output,
                                                output_schema=array_input_output)
    
    ln_scalar_desc = DeviceCommandDescriptor(name="ln_scalar",
                                            description="Returns the natural log of the input value", 
                                            input_schema=scalar_input_output,
                                            output_schema=scalar_input_output)
    ln_array_desc = DeviceCommandDescriptor(name="ln_array",
                                            description="Returns the natural log of the input values", 
                                            input_schema=array_input_output,
                                            output_schema=array_input_output)

    exp_scalar_desc = DeviceCommandDescriptor(name="exp_scalar",
                                            description="Returns exp() of the input value", 
                                            input_schema=scalar_input_output,
                                            output_schema=scalar_input_output)
    exp_array_desc = DeviceCommandDescriptor(name="exp_array",
                                            description="Returns exp() of the input values", 
                                            input_schema=array_input_output,
                                            output_schema=array_input_output)
    
    math_service.add_new_command(log10_scalar_desc,log10_scalar)
    math_service.add_new_command(log10_array_desc,log10_array)
    math_service.add_new_command(ln_scalar_desc,ln_scalar)
    math_service.add_new_command(ln_array_desc,ln_array)
    math_service.add_new_command(exp_scalar_desc,exp_scalar)
    math_service.add_new_command(exp_array_desc,exp_array)


    # It is a good idea to wrap running the service in a try/except/finally block to enable graceful shutdown 
    try:
        math_service.start()
    except KeyboardInterrupt:
        print("Shutting down device service...")
    except Exception as e:
        print("An error occurred while running the device service: ", e)        