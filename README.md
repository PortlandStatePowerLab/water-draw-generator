# water_draw_events_generator

Based on the standard DHW sheets.

[**SOURCE**](https://www.energy.gov/eere/buildings/building-america-analysis-spreadsheets)

## Requirements:

- Python3 
- GridLAB-D (mandatory for testing)
  - GridLAB-D can be easily installed from [**here.**](https://github.com/gridlab-d/gridlab-d/releases)

## usage:
- Clone this repository to your local machine

- Go to the scripts folder:
    ```
    cd scripts/
    ```

- Run the unique.py script:
    
    ```python3 unique.py```

  - The above command will export several stacked water draw profiles.

- Run the resample_wd_profiles script:
    
    ```python3 resample_wd_profiles.py```

  - The above command will export full-day water draw profiles with a one-minute time resolution.
  - The time resolution can be adjusted from the script, as well as the starting time and ending time.
  - Instructions are available in the 'resample_wd_profiles' script.
---
## Testing:
The GridLAB-D file has already been executed and the output files are stored in the following directory:
  - ```populated_13_node_feeder_whs/glm/glm_output/```

Each water heater object within the GridLAB-D file is set as follows:

  - The initial water temperature is 120 F.
  - The thermostat dead-band is 2 F.
  - The tank setpoint is 120 F.
  - The tank volume is 50 gallons.

If the user is planning to change any of the above settings, then the main GridLAB-D file will need to be executed again. Follow the steps below:
  
  - Change directory to the glm file:
    - ```cd populated_13_node_feeder_whs/glm/```
  - Run the GridLAB-D file using the following command in your terminal:
    - ```gridlabd 13_node_feder_whs.glm```
  - The simulation may take some time, depending on your OS. Once the simulation is done, the output files can be found in the following directory:
    - ```cd glm_output/```
  - Within the above directory, you'll find 39 files. Each file contains data for 25 water heaters in one-minute resolution.

- To visualize the water heater objects responses to the newly generated Water Draw profiles:
  - change the directory to the plots_py.py script:
    - ```cd populated_13_node_feeder_whs/python/```
  - Run the plots_py.py script:
    - ```python3 plots_py.py```
  - The script will generate a plot for each water heater object response. 

If none of the water heater objects settings are changed, then you do not need to run the GridLAB-D file. You can go ahead and visualize the data directly by running the plots_py.py script as shown above.

---
## NOTES:
  - **The title for each plot is the directory and the name of the water draw profile that the water heater object uses**

  - **The GridLAB-D file is already executed for your convenience. To generate a new set of output files, you need to run the main GridLAB-D file, as mentioned above**