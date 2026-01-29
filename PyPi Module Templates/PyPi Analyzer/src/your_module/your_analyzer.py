#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /PyPi Module Templates/PyPi Analyzer/src/your_module/your_analyzer.py
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
from PyAres import Analysis, AnalysisRequest, Outcome
import numpy as np
from .support_functions import support_function_2
# the . in the above import stament tells the code it should look in the local directory
# where it will find the support_functions directory and the associated __init__.py

"""
This main analyzer function is what will be called by the service whenever a request is recieved 
If the logic is simple, it can simply be defined within the main function, but more complex processes
may benefit from being broken out into subfunctions within this file or into other files and subdirectories
with the top level analyzer function primarily servering to pass data back and forth a mix of both approaches 
is used here for illustrative purposes

"""

def your_analyzer_function(request: AnalysisRequest) -> Analysis:

    """
    This demo analyzer parses the request to extract the inputs, multiplies the array 'bar'
    by an array of random numbers of the same length and adds it to the number 'foo'. 
    If the setting string 'baz' is "add", the numbers array is summed, otherwise the array is averaged
    """

    # This example enforces typing as good practice, but it is not strictly speaking necesary
    foo: float | int = request.inputs['foo']
    bar : list = request.inputs['bar']

    baz : str = request.settings["baz"]

    try: # It is good practive to have error handling 
        # so that the analysis service always returns something back to ARES OS 
        qux = foo+support_function_1(bar)*np.asarray(bar)
        quux = support_function_2(qux,baz)
    except Exception as e:
        print(f"Error during analysis: {e}")
        return Analysis(result=0.0, outcome=Outcome.FAILURE)
    
    return Analysis(result=quux, outcome=Outcome.SUCCESS)

def support_function_1(array:list) -> np.ndarray:
    # Returns an array of random numbers the same size as the input array
    return np.random.normal(size=len(array))



    
