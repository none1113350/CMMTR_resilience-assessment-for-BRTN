# Resilience Assessment Framework for Interdependent Bus–Rail Transit Network

This repository contains the code used in the paper "A resilience assessment framework toward interdependent bus–rail transit network: structure, critical components, and coupling mechanism analysis" published in the journal "Communications in Transportation Research".

## Environment Setup

To use this project, you need to set up the following environment and libraries:

- Python 3.7
- NetworkX
- Geopandas (version 0.12.1)
- k-shortest-paths
- requests
- Other common third-party libraries, such as Pandas, NumPy, Matplotlib, Seaborn, etc.

Note that the Geopandas library should be version 0.12.1. We haven't found the need to limit the version of other third-party libraries.

## Usage

Follow these steps to use this project:

1. Generate the line network file of the existing bus and subway stations using the geographical information data, which will be used to construct the interdependent network. The files are located in `step 1.ipynb` and `step 2.ipynb`.
2. Analyze the topology and structure of the interdependent network between the subway and bus stations, which are in `step3.ipynb` to `step 5.ipynb`.
3. Evaluate the importance of interdependent network stations, which is in `step 6.ipynb`.
4. Evaluate the resilience of the network using the code in `step 7.py`. Note that due to the size of the network, multiprocessing is required for processing. Therefore, you can use the provided Python file and set the number of processes according to the CPU configuration of your computer. Since Jupyter Notebook cannot perform multiprocessing programming, we only provide a Python file.
5. Other Python files are for importance results analysis.

