# Pyares Devices an Abstraction for Arbitrary Experimental Logic - EXAMPLE: Arithmetic
## Introduction
Often in a a closed-loop experimental procedure there is a need for some level of custom executionlogic that cannot be neatly cateogrized as an interaction with a planner, analyzer, or phyicical device. This could take the form of converting a raw experimental value, a log value, alternative units or fractional composition, summing other values to calcualte the input to another device, running a cleanup script to coalate and archive a folder log files, or inserting the values returned by the planner into a template file that is then passed to other experimental elements. 

One way to implment this behavior is to use extend the concept of a device beyond just interactions with the physical world to a service that does an some action. With this approach, it is possible to create arbitrarily complex execution logic using device services. There is some overlap with the [Custom Commands](https://afrl-ares.github.io/docs/ares/custom-commands) within ARES OS. In general custom commands should be used for very basic math operations or for cooridination between devices is needed, while devices should be used for more complex math and other self-contained logic, as it allows for greater flexibility for these tasks.
## The Arithmetic Device
The included `arithmetic_device.py` provides an example of how a device can be used to provide additonal mathematical functionality to ARES OS. The devices implements the following:
1. Calculation of `log10()`, `ln()`, and `exp()` for scalar and vector values
2. Calculation of fractional composition from an array of absolute amounts
3. Calculation of required dilution flow rate given flow rates for flammables, inerts and a flammability threshold value
4. Calculation of the required sampling time given an array of flow rates and desired sample amount.

### Using the Arithmetic Device
1. Clone this repository to your local machine.
2. Install the dependencies to an environment of your choiseusing pip with by running `pip install -r requirements.txt` from the parent directory. (Note that the only dependencies for this example are PyAres and numpy)
3. Run your analyzer with `python start_simple_planner.py` from within the parent directory. The script supports the following options for easy configuration at launch time:
* `-p`: The network port to host the planner service on. (Default: 5555)
* `-l`: Whether to host the service only on localhost. (Default: True) 

## Managing Dependencies and Python Environments
The complexity of scientifc code can vary widely from researcher to researcher, from a simple single file script that does basic math on the input data, to sprawling projects with dozens of external dependences, logic spread across multiple files, and resoruces such as calibraiton data or settings files that need to be loaded. As ARES OS can require multiple projects of this scale operating in tandem it is easy to run in to dependency conflicts or issues resolving resource paths if everything is being run out of the system python environment. Proper Python environment managment is also critical for making PyAres services portable across computers or laboratory environments 

To minimize these potential confilicts we recomend that each service be run in its own dedicated Python environment as described below. Note that PyAres requires Python version 3.10 or newer. 
### Option A: Using Anaconda / Miniconda / Miniforge 

1.  **Create the environment:**
    ```bash
    conda create -n my_env python=3.1x pip 
    ```
2.  **Activate the environment:**
    ```bash
    conda activate my_env
    ```
3.  **Install dependencies:**
    Navigate to the project root directory and run:
    ```bash
    pip install -r requirements.txt
    ```
    This will automatically install dependencies listed in `requirements.txt`.

### Option B: Using Python venv

1.  **Ensure you have Python >=3.10 installed:**
    Check your version:
    ```bash
    python3 --version
    ```
2.  **Create the virtual environment:**
    ```bash
    python3 -m venv my_env
    ```
3.  **Activate the environment:**
    * **Windows:**
        ```powershell
        .\my_env\Scripts\activate
        ```
    * **Linux/macOS:**
        ```bash
        source my_env/bin/activate
        ```
4.  **Install dependencies:**
    Navigate to the project root directory and run:
    ```bash
    pip install -r requirements.txt
    ```
    This will automatically install dependencies listed in `requirements.txt`.