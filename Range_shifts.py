################################################################################
# Project: Range shifts for PBL
# Script: Range shifts
# --- Actions: forecasts range shifts for mountain plant species in Switzerland using a simple habitat suitability model
# --- Input: biodiversity field data from "Bio_data" folder and environmental variables from "Envr_data" folder
# --- Output: maps of future ranges under different climate change scenarios for a specified plant species
# Author: Christopher Johnson
################################################################################


# IMPORT PACKAGES AND SET WORKING DIRECTORY
from os import chdir
import geopandas as gpd
import pandas as pd
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx
from rasterio.plot import show
from matplotlib.colors import ListedColormap
from itertools import product

# Set working directory
chdir("Documents/GitHub/PBL_Range_Shifts")


# USER: Enter species name or set all_sp to True to run analyses for all species
species = "Calluna_vulgaris" # see sp_list on line 41 for other species names
all_sp = True

# USER: Set time period for analysis or set all_period to True to run analyses for all time periods (choices: "current", "2035", "2060", "2085")
period = "current"
all_period = True

# USER: Set Representative Concencration Pathway (RCP) or set all_rcp to True to run analyses for all RCP scenarios (choices: "RCP26", "RCP45", "RCP85")
rcp = "RCP85"
all_rcp = True


# DEFINE GLOBAL PARAMETERS
# Species
if all_sp == True:
    sp_list = [ "Calluna_vulgaris", "Lotus_corniculatus", "Nardus_stricta", "Potentilla_aurea", "Potentilla_erecta", "Vaccinium_myrtillus" ]
else:
    sp_list = [ species ]

# Time period
if all_period == True:
    period_list = [ "current", "2035", "2060", "2085" ]
else:
    period_list = [ period ]

# RCP scenarios
if all_period == True:
    rcp_list = [ "RCP26", "RCP45", "RCP85" ]
else:
    rcp_list = [ rcp ]


# LOAD CURRENT ENVIRONMENTAL RASTER DATA (1981-2015) TO CALIBRATE HABITAT SUITABILITY MODEL
raster_files_current = {
    "bio10": "Envr_data/bio10_current.tif", # mean summer temperature
    "bio18": "Envr_data/bio18_current.tif", # total summer precipitation
    "slope": "Envr_data/slope.tif",
    "aspect": "Envr_data/aspect.tif"
}


# LOOP OVER ALL SPECIFIED SPECIES, TIME PERIODS, AND RCP SCENARIOS
for species, period, rcp in product(sp_list, period_list, rcp_list):
    
    # Skip RCP scenarios for current time period (2025)
    if (period == "current" and all_rcp == True and rcp in ["RCP45", "RCP85"]):
        continue
    
    # Print run information
    if period == "current":
        print(species, period)
    else:
        print(species, period, rcp)
    
    
    # HABITAT SUITABILITY MODEL
    # Load biodiversity data
    bio = pd.read_csv("Bio_data/Data_" + species + ".csv" ) # this file gives the latitude and longitudes of all observed occurrences for the species in Switzerland
    
    # Convert to GeoDataFrame with WGS84 coordinates (EPSG:4326)
    points = gpd.GeoDataFrame(
        bio,
        geometry=gpd.points_from_xy(bio["Longitude"], bio["Latitude"]),
        crs="EPSG:4326"
    )
    
    # Extract raster values for each environmental layer
    for name, path in raster_files_current.items():
        with rasterio.open(path) as src: 
            # Set coordinates
            coords = [(x, y) for x, y in zip(points.geometry.x, points.geometry.y)]
            
            # Extract raster value at each coordinate
            values = [val[0] if val[0] is not None else None for val in src.sample(coords)]
            points[name] = values
            
    # Compute min and max for each environmental variable
    env_vars = ["bio10", "bio18", "slope", "aspect"] 
    env_ranges = points[env_vars].agg(["min", "max"]) 
    Min_bio10, Max_bio10 = env_ranges.loc["min", "bio10"], env_ranges.loc["max", "bio10"] 
    Min_bio18, Max_bio18 = env_ranges.loc["min", "bio18"], env_ranges.loc["max", "bio18"] 
    Min_slope, Max_slope = env_ranges.loc["min", "slope"], env_ranges.loc["max", "slope"] 
    Min_aspect, Max_aspect = env_ranges.loc["min", "aspect"], env_ranges.loc["max", "aspect"]
    
        
    # PROJECT MODEL TO FUTURE SCENERIO
    # Load environmental raster data for projection scenarion
    if period == "current":
        raster_files = raster_files_current
    else:
        raster_files = {
            "bio10": "Envr_data/bio10_" + rcp + "_" + period +".tif", # mean summer temperature
            "bio18": "Envr_data/bio18_" + rcp + "_" + period +".tif", # total summer precipitation
            "slope": "Envr_data/slope.tif",
            "aspect": "Envr_data/aspect.tif"
        }
    
    # Re-project points to raster CRS
    #with rasterio.open(next(iter(raster_files.values()))) as src:
    #    raster_crs = src.crs
    #    transform = src.transform
    #    bounds = src.bounds
    #points = points.to_crs(raster_crs)
    
    # Extract raster values for each environmental layer
    arrays = {}
    meta = None
    for name, path in raster_files.items():
        with rasterio.open(path) as src:
            arrays[name] = src.read(1)
            if meta is None:
                meta = src.meta.copy()
        
    # Assume NoData values are represented as nan or negative values in original rasters
    valid_mask = np.ones_like(arrays["bio10"], dtype=bool)
    for name in arrays:
        valid_mask &= ~np.isnan(arrays[name])
    
    # Create binary suitability maps
    bio10_suit = ((arrays["bio10"] >= Min_bio10) & (arrays["bio10"] <= Max_bio10)).astype(np.uint8)
    bio18_suit = ((arrays["bio18"] >= Min_bio18) & (arrays["bio18"] <= Max_bio18)).astype(np.uint8)
    slope_suit = ((arrays["slope"] >= Min_slope) & (arrays["slope"] <= Max_slope)).astype(np.uint8)
    aspect_suit = ((arrays["aspect"] >= Min_aspect) & (arrays["aspect"] <= Max_aspect)).astype(np.uint8)
    
    # Combine suitability layers
    suitability = (bio10_suit & bio18_suit & slope_suit & aspect_suit & valid_mask).astype(np.float32) # use float to handle NaN
    
    # Replace invalid cells with NAN
    suitability[~valid_mask] = np.nan
    
    # Plot suitability map
    #plt.figure(figsize=(6, 5))
    #plt.imshow(suitability, cmap='gray')
    #plt.title(name)
    #plt.colorbar(label='Value')
    #plt.axis('off')
    #plt.show()
    
    # Update metadata for the output file
    meta.update(dtype=rasterio.float32, count=1, nodata=np.nan)
    
    # Save the suitability map
    if period == "current":
        suitability_tif = f"Suitability/Suitability_{species}_{period}.tif"
    else:
        suitability_tif = f"Suitability/Suitability_{species}_{period}_{rcp}.tif"
    with rasterio.open(suitability_tif, "w", **meta) as dst:
        dst.write(suitability, 1)
    
    
    # PLOT AND SAVE SPECIES RANGE MAP
    with rasterio.open(suitability_tif) as src:
        suitability = src.read(1)
        bounds = src.bounds
        crs = src.crs
        transform = src.transform
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Define colors and plot
    cmap = ListedColormap(["white", "green"])  # unsuitable = white, suitable = green
    cmap.set_bad(color='white', alpha=1.0)  # set NaN to opaque white to block basemap
    if period == "current":
        show(suitability, transform=transform, ax=ax, cmap=cmap, title=f"Range: {species}, {period}")
    else:
        show(suitability, transform=transform, ax=ax, cmap=cmap, title=f"Range: {species}, {period}, {rcp}")
        
    # Add basemap
    ax.set_xlim(bounds.left, bounds.right)
    ax.set_ylim(bounds.bottom, bounds.top)
    ctx.add_basemap(ax, crs=crs, source=ctx.providers.Esri.WorldShadedRelief, alpha=0.7)
    
    # Create mask layer to exclude areas beyond Switzerland
    mask_layer = np.where(np.isnan(suitability), 1, np.nan)  # 1 when beyond Switzerland, NaN elsewhere
    mask_cmap = ListedColormap(['white'])
    mask_cmap.set_bad(alpha=0)  # Make areas within Switzerland transparent
    show(mask_layer, transform=transform, ax=ax, cmap=mask_cmap)
    
    # Plot
    plt.tight_layout()
    if period == "current":
        plt.savefig(f"Range_maps/Range_map_{species}_{period}.tif", dpi=300)
    else:
        plt.savefig(f"Range_maps/Range_map_{species}_{period}_{rcp}.tif", dpi=300)
    plt.show()
    
    
