# Author: GDAL/OGR
# documentation: https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html#save-the-convex-hull-of-all-geometry-from-an-input-layer-to-an-output-layer
# Description: Save the convex hull of all geometry from an input Layer to an output Layer.
# Definition: "A new geometry object is created and returned containing the convex hull of the geometry on which the method is invoked."
# requires GDAL library, frameworks

## OGRGeometry::ConvexHull	(		)	const

# self

from osgeo import ogr
import os

# Get a Layer
inShapefile = "Archaeological_Sites_Maya_Forest_GIS.shp"
inDriver = ogr.GetDriverByName("ESRI Shapefile")
inDataSource = inDriver.Open(inShapefile, 0)
inLayer = inDataSource.GetLayer()

# Collect all Geometry
geomcol = ogr.Geometry(ogr.wkbGeometryCollection)
for feature in inLayer:
    geomcol.AddGeometry(feature.GetGeometryRef())

# Calculate convex hull
convexhull = geomcol.ConvexHull()

# Save extent to a new Shapefile
outShapefile = "Archaeological_Sites_Hull.shp"
outDriver = ogr.GetDriverByName("ESRI Shapefile")

# Create the output shapefile
outDataSource = outDriver.CreateDataSource(outShapefile)
outLayer = outDataSource.CreateLayer("states_convexhull", geom_type=ogr.wkbPolygon)
outLayer.CreateFeature(feature)