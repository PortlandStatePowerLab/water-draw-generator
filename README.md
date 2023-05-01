# water_draw_events_generator

Based on the standard DHW sheets.

[**SOURCE**](https://www.energy.gov/eere/buildings/building-america-analysis-spreadsheets)

## Requirements:

- Python3 
- GridLAB-D (mandatory for testing)
  - GridLAB-D can be easily installed from [**here.**](https://github.com/gridlab-d/gridlab-d/releases)

## usage:
- Clone this repository to your local machine
----
- Go to the scripts folder:
    ```
    cd scripts/
    ```
----
- Run the unique.py script:
    
    ```python3 dhw_daily.py```

  - The above command will export several stacked water draw profiles.
---
- Run the resample_wd_profiles script:
    
    ```python3 resample_wd_profiles.py```

  - The above command will export full-day water draw profiles with a one-minute time resolution.
  - The time resolution can be adjusted from the script, as well as the starting time and ending time.
  - Instructions are available in the 'resample_wd_profiles' script.
---
- To test the exported water draw profiles on water heater objects using GridLAB-D:
  
  - Change the directory to the glm file:
    - ```cd populated_13_node_feeder_whs/glm/```
  - Run the GridLAB-D file using the following command in your terminal:
    - ```gridlabd 13_node_feder_whs.glm```
  - The simulation may take some time, depending on your OS. Once the simulation is done, the output files can be found in the following directory:
    - ```cd glm_output/```
  - Within the above directory, you'll find 39 files. Each file contains data for 25 water heaters in one-minute resolution.