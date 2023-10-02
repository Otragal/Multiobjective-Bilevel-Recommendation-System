# Multi-Objective Diet Patching System

Author: Vítor de Oliveira Pochmann (Otragal)
Advisor: Fernando Von Zuben


## About

This work belongs to this author's Master's project at the Faculty of Electrical and Computer Engineering - Unicamp (2020 - 2022).

This work is a multi-objective dietary recommendation system (bi-level system) that uses two *solvers* algorithms to find a set of daily meal menus (breakfast, lunch, dinner and snack).

The search for finding the best menu solutions is carried out using the Pareto-Optimum method, by the [NSGA-II](https://ieeexplore.ieee.org/document/996017) algorithm using objectives of each candidate solution, calculated by [Gurobi](https://www.gurobi.com/) *solver*.

![System Structure](/sample/system.png)

Development environment used:

- Ubuntu 20.04 GNU Linux 64-bits


## Requirements

- Python Version 3.7 or greater (with virtual environment)
- SQLite3 (Database)
- [Gurobi Versão 9.1.0] or greater(https://www.gurobi.com/)

## Repository Map

- \Multiobjective-Bilevel-Recommendation-System 
    - \database (backup Database with all food information and original prices)
    - \dietprogram (\src of project)
        - \app.py (main of project)

## Installation

### Download

Performs `git clone` cloning or zip download from `master` repository.

### Environment Preparation

1. Create a virtual environment for this project (or just leave it on your machine).
2. Download the project's dependent libraries with `pip3 install <library_name>`
    - sqlite3
    - numpy
    - unicodedata
    - matplotlib
    - pandas
3. Have Gurobi and its license on your machine to use the libraries:
    - gurobipy

**NOTE**: The used version of the Gurobi tool was `Gurobi 9.1.0`. It is possible to download this version from the Official Site, but you can use the tool with the latest version.

### Getting Gurobi

Gurobi Solver is a proprietary tool from Gurobi Optimization company. It is possible to use this tool for free through the *Academic License*. If using it for other purposes, follow the procedures on the [Official Site](https://www.gurobi.com/).

#### Download Gurobi

1. Must log in and create an account in "Academic" view on [Gurobi Optimization Official Website](https://www.gurobi.com/).
2. Download the Gurobi tool from [Gurobi Optimizer](https://www.gurobi.com/downloads/gurobi-optimizer-eula/). É possível usar o Gurobi com Anaconda.
    - LINUX (Ubuntu): There is an installation guide made by [Unicamp](https://www.ic.unicamp.br/~cid/cursos/MC658/201901/tutorial-pacotes.pdf) or in the [Documentation on Official Site](https://www.gurobi.com/documentation/9.5/remoteservices/linux_installation.html).
    - WINDOWS 64-bits: There is an installation guide made by the [University of Mississippi](https://it.engr.msstate.edu/wp-content/uploads/2017/12/Gurobi-Installation_2017.pdf) or in [Documentation on Official Site](https://www.gurobi.com/documentation/9.5/remoteservices/windows_installation.html).
    - MAC OS: In [Documentation on Official Site](https://www.gurobi.com/documentation/9.5/remoteservices/macos_installation.html)

#### Gurobi license

After installing the gurobi library on your machine, a license is required.

1. Having accessed the account on the Official Website, the step of acquiring the [Academic License begins](https://www.gurobi.com/downloads/end-user-license-agreement-academic/).
2. Accept the conditions and get the license.
3. Accept the conditions and get the license.
3. Place the license in the default system directory. Click here to see the [Recommendation to put the license on your machine](https://support.gurobi.com/hc/en-us/articles/360013417211-Where-do-I-place-the-Gurobi-license-file-gurobi-lic-).

On Linux, it is recommended to place the license in the directory at `/opt/gurobi` or `opt/gurobiXXX` (XXX = version number).

Still on Linux, you must create a `PATH` so that python understands that the Gurobi library exists. In your `.bashrc` or `.profile_bash`, insert these lines of code and make the necessary changes:

```bash
export GUROBI_HOME="/opt/gurobiXXX/linux64"
export PATH="${PATH}:${GUROBI_HOME}/bin"
export LD_LIBRARY_PATH="${GUROBI_HOME}/lib"
export GRB_LICENSE_FILE="/opt/gurobiXXX/linux64/gurobi.lic"
```

## How to Use

