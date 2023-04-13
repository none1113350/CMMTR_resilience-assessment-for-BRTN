# Resilience Assessment Framework for Interdependent Bus–Rail Transit Networks

This repository contains code used in the paper `"A resilience assessment framework toward interdependent bus–rail transit network: structure, critical components, and coupling mechanism analysis"`, **which has been submitted to the journal "Communications in Transportation Research" and is currently undergoing peer review**.

## Environment Setup

To use the code in this project, you will need to configure the following environment and libraries:

- Python 3.7
- networkx
- Geopandas (version 0.12.1)
- k-shortest-paths
- requests
- Other common third-party libraries, such as pandas, numpy, matplotlib, seaborn, etc.

Note that geopandas must be version 0.12.1, but we do not have any additional version requirements for the other third-party libraries.

## Usage

To use this project, follow these steps:

1. Use existing geographic data for bus and subway stations to generate their line network files, which are used to construct the interdependent network. This can be done in the files `step 1.ipynb` and `step 2.ipynb`.
2. The topology and structure analysis of the interdependent network of subways and buses can be found in `step3.ipynb` to `step 5.ipynb`.
3. The evaluation of the importance of interdependent network nodes can be found in `step 6.ipynb`.
4. The code for resilience assessment is in `step 7.py`. Note that due to network size limitations, it is necessary to use multiprocessing for processing. Therefore, you can use the provided `.py` file and set the number of processes to be executed according to your computer's CPU configuration. Also, note that jupyter notebook cannot be used for multiprocessing, so we only provide the `.py` file here.
5. The remaining `.py` files are used for importance analysis results.

