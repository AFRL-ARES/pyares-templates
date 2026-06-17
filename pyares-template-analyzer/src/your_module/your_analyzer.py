#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from PyAres import Analysis, AnalysisRequest, Outcome

# Necessary logic can be imported from modules installed in your python environment, other files/folders within the module 
# or defined in the analyzer file as needed
import numpy as np
from .support_function1 import divide
from .support_function2 import add, subtract
def multiply(a,b):
    return a*b


def analysis_logic(a,b,c,multiply=True):
    # Example analysis code takes three inputs and a setting and returns a single value
    if multiply:
        return np.sqrt(subtract(add(a,b),(b*c)))    
    else:
        return np.sqrt(subtract(add(a,b),divide(b,c)))

def your_analyzer_function(request: AnalysisRequest) -> Analysis:
    # this function is what the analyzer service will call. It handles parsing between the ARES requests and the inputs and outputs of your analysis logic
    val_1 = request.inputs.get('Value 1')
    val_2 = request.inputs.get('Value 1')
    val_3 = request.inputs.get('Value 1')

    mult = request.settings.get('Multiply')
    try:
        result = analysis_logic(val_1,val_2,val_3,mult)
        outcome = Outcome.SUCCESS
    except Exception as e:
        print(f"Error during analysis: {e}")
        return Analysis(result=0.0, outcome=Outcome.FAILURE)
    return Analysis(result=result, outcome=Outcome.SUCCESS)



    
