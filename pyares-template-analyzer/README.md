# Pyares Analyzer Template
## Introduction
This is a template for a PyAres Analyzer service. This template is intended for more complex code that cannot be cleanly defined in a single file, and is structured as a self contained python module than can be installed into your python PATH using pip. This approach helps keep code redistributable 

## Module Structure
The template is structured to produce a package that can be installed using pip for portablility and reuseability. 
### Package Outline
`pyares-template-analyzer/` - Top level module folder
    ├─ `start_analyzer_template.py` - Python script that starts the service. Service properties, inputs, and settings are defined here.
    ├─ `pyproject.toml` - TOML file that contains metadata about the module and its dependencies, allowing to easy installation of all dependencies with pip
    ├─ `setup.py` - Calls setuptools.setup to configure the package
    ├─ `src/`
        ├─ `your_module` - Folder containing your module code
            ├─ `__init__.py` - Python file that makes the folder act as a python package allowing for easier imports into other files, for example, the script that defines and starts the analyzer service.
            ├─ `your_analzyer.py` - This file serves as the "plumbing" between the PyAres service and your analysis code. Here you can map data and settings coming in from ARES OS to the inputs of your analysis logic. This also formats the output of your analysis logic into an objective score that is passed back to ARES OS. 
            ├─ `support_function1.py` - An example of how analyzer logic can be defined in other other scripts at in the same directory as the analyzer. Useful if you have all of your analyzer logic in 
            ├─ `support_function2.py` - A folder to illustrate how analyzer logic can loaded in from subfolders for better organization
                ├─ `__init__.py` - Makes functions defined in example_math.py accessibile from higher level packages.
                ├─ `example_math.py` - Defines some basic math functions used in the analyzer logic example.


### Using Pip to manage PyAres services

The complexity of scientifc code can vary widely from researcher to researcher, from a simple single file script that does some basic math on the input data, to sprawling projects with dozens of external dependences, logic spread across multiple files, and resoruces such as calibraiton data or settings files that need to be loaded. As ARES OS can require multiple projects of this scale operating in tandem it is easy to run in to dependency conflicts or issues resolving resource paths if everything is being run out of a single system python environment. This python envornment managment issue only becomes more pronoucned when atempting to move packages between host computers. 

One of the core ideas of PyAres is to make it easy to re-use existing code bases that already do what you want them to with minimal addtional effort needed to make things work with ARES OS.


# Getting Started & Environment Management

The complexity of scientific code can vary widely. To minimize dependency conflicts, it is highly recommended that each service be run in its own dedicated Python environment.

### Option A: Using Anaconda / Miniconda / Miniforge

1. **Create the environment:**
```bash
conda create -n pyares_env python=3.10 pip 

```

2. **Activate the environment:**
```bash
conda activate pyares_env

```

3. **Install dependencies:** Navigate to the specific template directory and run :
```bash
pip install -e .

```

### Option B: Using Python venv

1. **Create the virtual environment:**
```bash
python3 -m venv pyares_env

```

2. **Activate the environment:**
* **Windows:** `.\pyares_env\Scripts\activate`
* **Linux/macOS:** `source pyares_env/bin/activate`

3. **Install dependencies:** Navigate to the specific template directory and run:
```bash
pip install -r requirements.txt

```
