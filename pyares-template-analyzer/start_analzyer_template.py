#!/usr/bin/env python3
# -*- coding:utf-8 -*-

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
    1. Input 1 - key: "Value 1"
    2. Input 2 - key: "Value 2"
    3. Input 3 - key: "Value 3"

    Analyzer Settings are:
    1. Setting 1 - key: "Multiply"

    Ensure that all your inputs have the approriate data type specified.
    See the PyAres documentation for more detial on data type
    """

    analyzer.add_analysis_parameter("Value 1", AresDataType.NUMBER)
    analyzer.add_analysis_parameter("Value 1", AresDataType.NUMBER)
    analyzer.add_analysis_parameter("Value 3", AresDataType.NUMBER)
    
    analyzer.add_setting("Multiply", AresDataType.BOOLEAN)

    analyzer.start()
