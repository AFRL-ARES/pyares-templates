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