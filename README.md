# Resilience Assessment Framework for Interdependent Bus–Rail Transit Networks

This repository contains code used in the paper `"A resilience assessment framework toward interdependent bus–rail transit network: structure, critical components, and coupling mechanism analysis"`, **which has been submitted to the journal "Communications in Transportation Research" and is currently undergoing peer review**.

## Abstract
Understanding the interdependent nature of multimodal public transit networks (PTNs) is vital for ensuring the resilience and robustness of transportation systems. However, previous studies have predominantly focused on assessing the vulnerability and characteristics of single-mode PTNs, neglecting the impacts of heterogeneity in disturbance and shifts in travel behavior within multimodal PTNs. Therefore, this study introduces a novel resilience assessment framework that comprehensively analyzes the coupling mechanism, structural and functional characteristics of bus-rail transit networks (BRTNs). In this framework, a network performance metric is proposed by considering the passengers’ travel behaviors under various disturbances. Additionally, stations and subnetworks are classified using the K-means algorithm and resilience metric by simulating various disturbances occurring at each station or subnetwork. The proposed framework is validated via a case study of a BRTN in Beijing, China. Results indicate that the rail transit network (RTN) plays a crucial role in maintaining network function and resisting external disturbances in the interdependent BRTN. Furthermore, the coupling interactions between the RTN and bus transit network (BTN) exhibit distinct characteristics under infrastructure component disruption and functional disruption. These findings provide valuable insights into emergency management for PTNs and understanding the coupling relationship between BTN and RTN.




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

