# GravelScape: Grain Size Fining Dynamics within a Landscape Evolution Model
GravelScape is a package for grain size fining based on the equations of Fedele and Poala (2007) that is coupled with the landscape evolution model Fastscape (https://fastscape.readthedocs.io/en/latest/). Further information on the model and it's application is described in the Wild et al. 2025 ESurf publicaitons (https://doi.org/10.5194/egusphere-2024-351). 

## Instalation
Install and run locally (Conda)

Assuming that you have git and conda installed, you can install all the packages required to run the notebooks in a new conda environment using the following commands:

$ git clone https://github.com/fastscape-lem/GravelScape
$ cd GravelScape
$ conda env create -f environment.yml
$ conda activate GravelScape
Note: you could use mamba instead of conda. mamba is a faster alternative to conda.

Finally run the command below to start the Jupyterlab application. It should open a new tab in your browser where you can open and run the notebook (.ipynb) files.

$ jupyter lab

All necessary packages are already included in the environment.yml file. For transparency and in case of issue, the notebooks and packages depend on Python (3.9 or later is recommended), numpy, scipy, pandas, fastscape, flexure, and multiflow packages. 

## Usage
GravelScape is a .py package (along with otheer packages used in the ESURF publication) that runs coupled to the FastScape Model. Some example applications, couplings, and validation of the code as jupyer notebooks are in the notebooks folder.

