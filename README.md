# Habitat_Suitability_Model
This repository contains the data and scripts for generating a basic habitat suitability model in Python for projecting plant range shifts under future climate change scenarios for teaching purposes

## Folder Structure:
* Bio_data: data files containing latitude and longitude for biodiversity data for six mountain plant species
* Envr_data: environmental rasters for environmental different predictor variables, years, and Representative Concentration Pathways (RCP) scenarios
* Range_maps: projected plant geographical ranges for different species, time periods, and RCP scenarios
* Range_shifts.py: Python script for running the habitat suitability models
* Suitability: habitat suitability maps for different species, time periods, and RCP scenarios

## To run
* Download Range_shifts.py and Bio_data into a common folder
* Create folders "Envr_data", "Suitability" and "Range_maps" in the comomon folder (with Range_shifts.py), these will initially be empty folders
* Download environmental data from Zenodo: https://zenodo.org/records/17458011
  * Go to "Files" -> "Download all"
  * Open the Zip file and move all files (ten BIO10 files, ten BIO18 files, aspect.tif, and slope.tif) into "Envr_data" (the BIO10 and BIO18 files must be directly in the "Envr_data" folder and not in the "BIO10" and "BIO18" folders)
* Open Range_shifts.py
  * Set directory to the location with Range_shifts.py (line 24)
  * Write in species name (line 28) and set "all_sp" to False to run the script for a specified species or set "all_sp" to True to run the script for all species (line 29)
  * Write in time period (line 32) as a string within quotes (e.g., "2035") and set "all_period" to False to run the script for a specified time period or set "all_period" to True to run the script for all time periods (line 33)
  * Write in RCP scenario (line 36) and set "all_rcp" to False to run the script for a specified RCP scenerio or set "all_rcp" to True to run the script for all RCP scenarios (line 37)
  * Run the script, suitability maps are saved in the "Suitability" folder and distribution range maps are saved in the "Range_maps" folder
* Note that the "Suitability" TIFF files can be fairly large. After the model is run, it is safe to delete these files if desired.

## Environmental predictor variables
* BIO10 - mean temperature of warmest quarter
* BIO18 - total precipitation during warmest quarter
* Aspect
* Slope

## Time periods
* Current = 1981 - 2015 (used for model calibration and projecting species' current ranges)
* 2035 (denoting data spanning 2020 - 2050)
* 2060 (denoting data spanning 2045 - 2075)
* 2085 (denoting data spanning 2070 - 2100)

## Representative Concentration Pathways (RCP) scenarios
* RCP26 (Optimistic: carbon dioxide emissions start declining by 2020 and go to zero by 2100)
* RCP45 (Intermediate: carbon dioxide emissions in RCP 4.5 peak around 2040, then decline)
* RCP85 (Worst-case: emissions continue to rise throughout the 21st century)
