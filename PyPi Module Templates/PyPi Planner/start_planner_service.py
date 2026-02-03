#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /PyPi Module Templates/PyPi Planner/start_planner_service.py
# Project: pyares-templates
# Created Date: Thursday, January 29th 2026, 12:24:17 pm
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

"""
One of the key ideas behind PyAres is to allow users to reuse 
as much of their code as possible. This top level function serves 
only to define and start the service, calling a planner functon that is 
defined within the package

"""
from PyAres import AresPlannerService, AresDataType
from your_module import your_planner_function

if __name__ == "__main__":
    name = "<The name of your planner]>"
    description = "<Description of your planner>"
    version = "<X.X.X>"
    port = 1337
    local = True

    planner = AresPlannerService(your_planner_function,
                                    service_name = name,
                                    service_version = version,
                                    service description = description, 
                                    use_localhost=local, 
                                    port=port)
    #Mark that the planner supports numbers
    planner.add_supported_type(AresDataType.NUMBER)

    """
    Planner Settings are:
    1. Setting 1 - key: "foo"
    2. Setting 2 - key: "bar"
    3. Setting 3 - key: "baz" 

    Ensure that all your inputs have the approriate data type specified.
    See the PyAres documentation for more detial on data type

    The names set here are what are reported to ARES OS, so for a real planner,
    it is good practice to make them descriptive. 

    With the current release of PyAres, mapping settings to specific parameters
    can be be a little clunky and manual, see your_planner.py for more details.
    """

    # Settings for planner condfiguration
    planner.add_setting("foo", AresDataType.NUMBER)
    planner.add_setting("bar", AresDataType.NUMBER)
    planner.add_setting("baz", AresDataType.NUMBER)

    planner.start()
