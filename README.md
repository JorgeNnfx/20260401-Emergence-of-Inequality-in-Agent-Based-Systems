Emergence of Inequality in Agent-Based Systems

This repository contains the source code and simulation framework for the study:"Inequality in Agent-Based Models under Stochastic Dynamics, Cumulative Advantage, and Network Structure" Currently under review [Index Journal]

Citation
If you use this code or the model in your research, please cite it as:
Nanfuñay-Chancafe, Jorge G. (2026). Inequality in Agent-Based Models under Stochastic Dynamics, Cumulative Advantage, and Network Structure [Manuscript under review].
https://orcid.org/my-orcid?orcid=0009-0004-2855-9751

Overview
This project implements an Agent-Based Model (ABM) to simulate how inequality emerges from the interplay between:
- Intrinsic Talent: Agents with talent $T_i \sim \mathcal{N}(0,1)$.
- Stochastic Performance: The impact of "luck" ($\sigma_{\text{luck}}$) on success.
- Network Topology: Comparison between Scale-Free (Barabási-Albert) and Random (Erdős–Rényi) networks.
- Nonlinear Accumulation: Cumulative advantage mediated by the parameter $\eta$.

Requirements
Python 3.13
Libraries: numpy, networkx, csv.

Repository Structure
/src: Core simulation scripts.
/notebooks: Data analysis and visualization (Gini coefficient, Talent-Success correlation).
/data: Sample outputs and configuration files.

License
This project is licensed under the MIT License - see the LICENSE file for details.
