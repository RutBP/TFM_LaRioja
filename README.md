# TFM_LaRioja
This repository contains the codes and resources needed to run and analyse three cellular automata: Soil Erosion, Population Movement with and without migration, and Water Flow. These models simulate different geospatial processes and provide tools to explore and understand their dynamics.

## The work
Rural areas in Spain are experiencing unprecedented environmental and social changes. Climate change and biodiversity loss are occurring alongside depopulation and the abandonment and intensification of rural landscapes. To analyse this problem and move from qualitative accounts of interactions into a more systematic understanding, it is proposed to use the cellular automata (CA) approach to model the impact of climate change and depopulation on the socio-ecological system of La Rioja (Spain), considering the physical characteristics of the terrain, climatic constraints and population variation. This could provide valuable information for policy and strategy development, addressing the lack of systematic knowledge about how these hazards interact with people's decisions and reactions.
To this end, three CA models have been developed focusing on climatology, population and infrastructure, using different inputs and different transition functions. The results obtained will be validated with a rural vulnerability index developed in the SUSTAIN project.

## Requirements
This project requires the following libraries `numpy`, `rasterio`, `tifffile` and `scipy`. To install these libraries, you can use the provided `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Repository structure
The repository is organised as follows:
- `requirements.txt`: File containing the necessary dependencies to run the codes.
- `SoilErosion.py`: Source code to simulate soil erosion.
- `PopulationMigration.py`: Source code to simulate population movement with migration.
- `Population.py`: Source code to simulate population movement without migration.
- `WaterFlow.py`: Source code to simulate water flow.
- `RasterMaps`: Folder containing all the maps used as input in the different codes.

## Use
To run the cellular automata, follow these steps:
1. Make sure you have the above requirements installed.
2. Browse to the RasterMaps/ folder and run the code corresponding to the cellular automaton you want to simulate. For example, to simulate soil erosion, run SoilErosion.py.
3. The simulation results will be saved in the ResultsPopulation/, ResultsErosion/ or ResultsFlux/ folders, depending on which cellular automaton you ran.
