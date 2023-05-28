# Analysis of methanol retention in reversed micelles formed by AOT/isooctane/water

<p align="center">
<img src="build-of-rms.png" alt="RM39">
</p>

This repository is a technical guide to reproduce the results in
our [paper](https://github.com/antadlp/rms-aot-methanol). 

## Table of contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Guide](#guide)
- [License](#license)
- [Citation](#citation)

## Requirements
Here are some general requirements, but to give the exact
requirements and dependencies, i created an anaconda environment
file [environment.yml](environment.yml). Instructions of how to
use it are in the [installation](#installation) section.

- python (version>=3.7.4)
- pandas (version>=1.3.1)
- matplotlib (version>=3.4.2)
- numpy (version>=1.20.3)
- nglview (version>=3.0.3)

## Installation
There is no formal installation since this is a technical guide
to the [article](https://github.com/antadlp/rms-aot-methanol).
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

Remember to be positioned at the level where the rms-aot-methanol
folder is located when you run jupyter notebook to be able to see
all the files inside this repository.

## Guide
- Build of the systems
   - [Molecules information etc](./notebooks/Molecules_information_etc.ipynb)
   <!-- - Upgrade forcefield parameters for isooctane -->
   - [Molecular self-assembly of RMs](./notebooks/Molecular_self-assembly_of_RMs.ipynb)
   - Treatment due to periodic conditions 
   - Placement of RM into isooctane
   - Placement of methanol into RM/isooctane
- (Production) Runs of dynamics
   - Relaxation process
   - Runs
- (Post-production) Data analysis
   - Extract trayectories
   - Treatment due to periodic conditions
   - Temperature
   - Potential energy
   - Radius of gyration
   - Principal axis of inertia

## License
See the [LICENSE](LICENSE) file for more details.

## Citation
If this helps you in any way, cite this as described below.

```
@article{alvarez2022rmsMetanol,
  title={Analysis of methanol retention in reversed micelles formed by aot isooctane water},
  author={antonio, sarah and hector},
  year={2022}
}
```
------



