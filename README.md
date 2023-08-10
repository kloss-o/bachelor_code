# Bachelor Thesis: Entwicklung von Methoden zum Vergleich von Provenienzgraphen
- This repository contains the code of the bachelor thesis with said title. There are different algorithmus for graph matching and a gui to display the results.
- Oliver Kloss, Forschungszentrum Juelich, FH Aachen

Related publications:
- 1. Oliver Kloss. Visualisierung von heterogenen Provenienzdaten in der Neurowissenschaft. *Seminar paper*. (2023)


## Table of contents
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Code repository](#code-repository)
  - [How to run](#how-to-run)

## Prerequisites

### Requirements
Project requires Python 3.7, 3.8, 3.9 or 3.10, and the following packages:

- matplotlib == 2.0.1
- NetworkX
- numpy
- text_diff
- pip

## Installation

Create environment:

pip:
```bash
pip install -r requiremnts.txt
```

## Code repository

- `gui.py` the main script to run the gui
- `gexf_compare.py` contains the code for the Graph Edit Distance Array + Comparison functions
- `func_compare.py` contains the code the own algorithm for function comparison
- `comp_accumulated.py` contains the code to the comparison with the accumulated graph
- `extract_func.py` contains the code that converts non-linear function graph to linear ones + text_diff


Give a description of the folder structure
- `Benchmark` contains benchmark data for Graph Edit Distance
- `Code` contains all the code of the project 
- `Data` contains all data used in the project or for testing/examples

## How to run

1. For a specific algorithm, run the file the code is in.
2. For the gui, run the gui.py.


