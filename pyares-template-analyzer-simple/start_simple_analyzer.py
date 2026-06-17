# -----------------------------------------------------------------------------
# 1. Import Necessary Modules
# -----------------------------------------------------------------------------
from PyAres import (AresAnalyzerService, # Required for the Service
                    AnalysisResponse, AnalysisRequest, AresDataType,Outcome) 
import numpy as np # For example logic, feel free to delete if not needed

# -----------------------------------------------------------------------------
# 2. Define Your Service Details 
# -----------------------------------------------------------------------------
name = "<The name of your analyzer>"
description = "<Description of your analyzer>"
version = "<X.X.X>" # Analzyer version numbering that will be reported to ARES OS.
port =  7300 # The network port your analyzer will use to communicate with ARES OS.
local = True # Whether to use localhost or not

# ----------------------------------------------------------------------------- 
# 3. Define the Analysis Logic
# -----------------------------------------------------------------------------
# NOTE: In this example, the analyzer returns the standard deviation list of values. 
# Can be configured to normalize by the mean.
def analyze(values, normalize=False):
    mean = np.mean(values)
    std = np.std(values)
    if normalize:
        out = std/mean
    else:
        out = std

    return out

# -----------------------------------------------------------------------------
# 4. Define Analyzer Function.
# -----------------------------------------------------------------------------
# This function handles the "plumbing" of passing data to an from the ARES AnalysisRequest to the actual analysis logic

def analyzer(request: AnalysisRequest) -> AnalysisResponse:
    try:
        # Get input and settings values from the request and pass them to the analsis logic
        values_list = request.inputs.get("Experiment Values")
        normalize = request.settings.get("Normalize")
        ouput_value = analyze(values_list, normalize)

        # Put the value from analysis logic into an analysis message to be sent back to ARES
        analysis = AnalysisResponse(result=ouput_value, outcome=Outcome.SUCCESS)

    except Exception as e:
        analysis = AnalysisResponse(result=-1, outcome=Outcome.FAILURE)

    return analysis

# -----------------------------------------------------------------------------
# 4. Configure and Start Analyzer Service.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    """
    Example analyzer that returns the standard deviation of a list of numbers, with the option to normalize the value by the mean
        Analyzer inputs are:
            1. Input 1 - key: "Experiment Values" description: "A list of values"
        Analyzer Settings are:
            1. Setting 1 - key: "Normalize" description: "Whether to normalize the returned value or not"
    Ensure that all your inputs have the appropriate data type(s) specified.
    """
    analyzer_service = AresAnalyzerService(analyzer,
                                           name,
                                           version,
                                           description, 
                                           use_localhost=local, 
                                           port=port)

    # Note that parameter/setting names are case sensitive in this example
    analyzer_service.add_analysis_parameter("Experiment Values", AresDataType.NUMBER_ARRAY)
    analyzer_service.add_setting("Normalize", AresDataType.BOOLEAN)

    # It is good practice to wrap the operation of the service in a try/except/finally block
    try:
        analyzer_service.start()
    except Exception as e:
        print(f"An Exception Occured: {e}")
    except KeyboardInterrupt:
        print(f"\nShutting Down PyAres Service...")
    finally: # Use the finally block for things like saving/closing any active data files, closing remote connections, etc.
        pass

