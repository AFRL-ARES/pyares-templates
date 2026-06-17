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



# Using PyPi to manage PyAres services

One of the core ideas of PyAres is to make it easy to re-use existing code bases that already do what you want them to with minimal addtional effort needed to make things work with ARES OS.

 The complexity of scientifc code can vary widely from researcher to researcher, from a simple single file script that does some basic math on the input data, to sprawling projects with dozens of external dependences, logic spread across multiple files, and resoruces such as calibraiton data or settings files that need to be loaded. As ARES OS can require multiple projects of this scale operating in tandem it is easy to run in to dependency conflicts or issues resolving resource paths if everything is being run out of a single system python environment. This python envornment managment issue only becomes more pronoucned when atempting to move packages between host computers. 

To address this issue we recomend that each service be run in its own dedicated Python environment. These environments can easily be created though python package managers such as anaconda/miniconda/miniforge.

```
conda create -n my_service_env python=3.1X
conda activate my_service_env
```

TODO: How to do this in virtualenv?

This fresh python environment will not have any of the dependencies needed for the actual service logic to run. While the necessary modules can be installed manually or from a list of dependecies, a more portable method is the format the module logic as a `pip` installable package. In this case, setting up the analyzer is as simple as navigating to the source folder and doing a local, editable pip installation with `pip install -e .` This approach will automatically handle retreiving external dependences and ensure that all files and resources are approriately handed within the environment python path.

This directory incudes basic templates for pip installable version of planner, analyzer, and device pyares service.