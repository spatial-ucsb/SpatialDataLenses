# Author: ESRI
# documentation: http://help.arcgis.com/En/Arcgisdesktop/10.0/Help/index.html#//00170000003q000000
# Description: Use MinimumBoundingGeometry function to find an area for each multipoint input feature.
# Definition: "The smallest convex polygon enclosing an input feature."
# input features are not grouped by default
# requires ArcInfo license

## MinimumBoundingGeometry_management (in_features, out_feature_class, {geometry_type}, {group_option}, {group_field}, {mbg_fields_option})

# in_features (point, multipoint, line, polygon, multipatch) -> shapefile
# out_feature_class (polygon) -> shapefile
# geometry type (rectangle_by_area, rectangle_by_width, convex_hull, circle, envelope)
# group option (none, all, list)

# import system modules 
import arcpy
from arcpy import env

# Set environment settings
env.workspace = "/Users/saralafia/Documents/6_Winter_16/288WK/data"

# Create variables for the input and output feature classes
inFeatures = "Archaeological_Sites_Maya_Forest_GIS.shp"
outFeatureClass = "Archaeological_Sites_Hull.shp"

# Use MinimumBoundingGeometry function to get a convex hull area for each cluster of archaeological sites that are multipoint features
arcpy.MinimumBoundingGeometry_management(inFeatures, outFeatureClass, "CONVEX_HULL", "NONE")