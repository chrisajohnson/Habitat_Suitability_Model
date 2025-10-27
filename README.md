# Habitat_Suitability_Model
This repository contains the data and scripts for generating a basic habitat suitability model in Python for projecting plant range shifts under future climate change scenarios for teaching purposes

## Folder Structure:
* Bio_data: data files containing latitude and longitude for biodiversity data for six mountain plant species
* Envr_data: environmental rasters for different predictor variables, years, and Representative Concentration Pathways (RCP) scenarios
* Range_maps: projected plant geographical distributions (ranges) for different species, time periods, and RCP scenarios
* Range_shifts.py: Python script for running habitat suitability models
* Suitability: habitat suitability maps for different species, time periods, and RCP scenarios

## To run
* Download Range_shifts.py, Bio_data, and Envr_data into common folder
* Open Range_shifts.py and set directory to location with Python script (line 24)
* Write in species name (line 28) and set "all_sp" to False to run script for specified species or set "all_sp" to true to run script for all species (line 29)
* Write in time period (line 28) and set "all_sp" to False to run script for specified species or set "all_sp" to true to run script for all species (line 29)
* Write in species name (line 28) and set "all_sp" to False to run script for specified species or set "all_sp" to true to run script for all species (line 29)

## Environmental predictor variables
* BIO10 - mean temperature of warmest quarter
* BIO18 - total precipitation during warmest quarter
* Aspect
* Slope

## Time periods
* Current = 1981 - 2015 (used for model calibration and projecting species' current ranges)
* 2035 (mean year of data spanning 2020 - 2050)
* 2060 (mean year of data spanning 2045 - 2075)
* 2085 (mean year of data spanning 2070 - 2100)

## Representative Concentration Pathways (RCP) scenarios
* RCP26 (Optimistic: carbon dioxide emissions start declining by 2020 and go to zero by 2100)
* RCP45 (Intermediate: carbon dioxide emissions in RCP 4.5 peak around 2040, then decline)
* RCP85 (Worst-case: emissions continue to rise throughout the 21st century)
