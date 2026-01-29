#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: /PyPi Module Templates/PyPi Analyzer/start_analyzer_service.py
# Project: pyares-templates
# Created Date: Thursday, January 29th 2026, 11:00:20 am
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
only to define and start the service, calling an analyzer functon that is 
defined within the package

"""

from PyAres import AresAnalyzerService, AresDataType
from your_module import your_analyer_function

if __name__ == "__main__":
    name = "<The name of your analyzer>"
    description = "<Description of your analyzer>"
    version = "<X.X.X>"
    port = 7356
    local = True

    analyzer = AresAnalyzerService(your_analyer_function,
                                    name,
                                    version,
                                    description, 
                                    use_localhost=local, 
                                    port=port)
    """
    Analyzer inputs are:
    1. Input 1 - key: "foo"
    2. Input 2 - key: "bar"

    Analyzer Settings are:
    1. Setting 1 - key: "baz"

    Ensure that all your inputs have the approriate data type specified.
    See the PyAres documentation for more detial on data type
    """

    analyzer.add_analysis_parameter("foo", AresDataType.NUMBER)
    analyzer.add_analysis_parameter("bar", AresDataType.NUMBER_ARRAY)

    analyzer.add_setting("baz", AresDataType.STRING)

    analyzer.start()
