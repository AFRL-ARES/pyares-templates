# Pyares Simple Planner Template
## Introduction
This is a template for a simple random with exclusion, single file [PyAres](https://github.com/AFRL-ARES/PyAres) planner service. This Planner is designed to generate random numbers outside of a calculated exclusion zone.

## Using this Template
1. Clone this repository to your local machine.
2. Edit `requirements.txt` to specify the any dependencies for your planner. These can then be installed using pip with by running `pip install -r requirements.txt` from the parent directory.
3. Edit `start_simple_planner.py` to customize your planner.
4. Run your analyzer with `python start_simple_planner.py` from within the parent directory.

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
