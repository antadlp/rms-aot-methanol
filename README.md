# The Influence of Temperature on the Retention of Methanol by AOT Reverse Micelles: A Molecular Dynamics and First-Principles Study

<p align="center">
<img src="build-of-rms.png" alt="RM39">
</p>

This repository is a technical guide to reproduce the results in
our [paper](https://doi.org/10.1021/acs.jpcb.5c01224). 

## Table of contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Guide](#guide)
- [License](#license)
- [Citation](#citation)

## Requirements
Here are some general requirements, but for the exact
dependencies and package versions, see the provided
[environment.yml](environment.yml) file. Setup instructions are
available in the [installation](#installation) section.

- python (version>=3.7.4)
- pandas (version>=1.3.1)
- matplotlib (version>=3.4.2)
- numpy (version>=1.20.3)
- nglview (version>=3.0.3)

## Installation
There is no formal installation since this is a technical guide
to the [article](https://doi.org/10.1021/acs.jpcb.5c01224).
Nonetheless, you can follow these instructions to use and
interact with the notebooks and code that
is presented.

```
git clone https://github.com/antadlp/rms-aot-methanol
cd rms-aot-methanol
conda env create -f environment.yml
conda activate paperenv.yml
cd ..
jupyter notebook --no-browser
```

Make sure to run Jupyter Notebook from the directory that
contains the rms-aot-methanol folder so that all files and paths
within the repository are accessible.

## Guide (🚧 Under Construction)
This section of the project is currently being worked on. Stay tuned for updates!

### System Preparation
- [Molecular information, composition, etc.](./notebooks/Molecules_information_etc.ipynb)
<!-- - Upgrade forcefield parameters for isooctane -->
- [Molecular self-assembly of reverse micelles (RMs)](./notebooks/Molecular_self-assembly_of_RMs.ipynb)
- Correction for periodic boundary conditions
- Placement of RMs into isooctane
- Placement of methanol into RM/isooctane system

### Production: Molecular Dynamics Runs
- Relaxation process
- Production simulations

### Post-production Data Analysis
- Extract trajectories
- Self-assembled RMs analysis
- Methanol retention analysis

## License
See the [LICENSE](LICENSE) file for more details.

## Citation
If this helps you in any way, cite this as described below.

**The Influence of Temperature on the Retention of Methanol by AOT Reverse Micelles: A Molecular Dynamics and First-Principles Study**  
*Antonio Alvarez de la Paz, Ana Mizrahim Matrecitos-Burruel, Amir Maldonado, and Héctor Domínguez*  
*The Journal of Physical Chemistry B*, **2025**, *129*(18), 4569–4580  
[https://doi.org/10.1021/acs.jpcb.5c01224](https://doi.org/10.1021/acs.jpcb.5c01224)

```
@article{doi:10.1021/acs.jpcb.5c01224,
author = {Alvarez de la Paz, Antonio and Matrecitos-Burruel, Ana Mizrahim and Maldonado, Amir and Domínguez, H{\'e}ctor},
title = {The Influence of Temperature on the Retention of Methanol by AOT Reverse Micelles: A Molecular Dynamics and First-Principles Study},
journal = {The Journal of Physical Chemistry B},
volume = {129},
number = {18},
pages = {4569-4580},
year = {2025},
doi = {10.1021/acs.jpcb.5c01224},
note ={PMID: 40273342},
URL = {https://doi.org/10.1021/acs.jpcb.5c01224},
eprint = {https://doi.org/10.1021/acs.jpcb.5c01224}
}

```
------



