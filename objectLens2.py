import arcpy, os
from arcpy.sa import *

ST = 'NEW_SELECTION'
LYR = 'polys_lyr'
AT = 'CELL_CENTER'
KFIELD = 'count'
CELL = 25
STYPE = 'SUM'

polyfilename = 'District1_RectangleMerge.shp'

topfold = r'C:\Users\grad\Documents\ArcGIS\SBBG\Merges'
outfile = os.path.join(topfold,'D1_OverlapRaster'+str(CELL)+'.img')
razFold = os.path.join(topfold,'RazDumpD1'+str(CELL))
if not os.path.exists(razFold): os.makedirs(razFold)

### open the polygons as a layer
# set workspace
arcpy.env.workspace = topfold
arcpy.env.overwriteOutput = True
arcpy.env.snapRaster = r'C:\Users\grad\Documents\ArcGIS\SBBG\SnapRaster25.img'

print('Converting to rasters: '),

# make a layer from a shapefile
arcpy.MakeFeatureLayer_management(polyfilename,LYR)

# the key to making this work is to have a 'background' polygon coded as 0

# loop over selection and polygon to raster
for p in range(0,45):
    # file name
    outN = os.path.join(razFold,'raster'+str(p)+'.img')
    # selection criteria -- select polygon of interest AND background
    selstr = ' "Id" = ' + str(p) + ' OR "Id" = -1'
    # selection
    arcpy.SelectLayerByAttribute_management(LYR,ST,selstr)
    # convert to raster
    arcpy.PolygonToRaster_conversion(LYR,KFIELD,outN,AT,KFIELD,CELL)
    if p%10 == 0: print p

### add up the rasters
# get raster list
arcpy.env.workspace = razFold
razList = arcpy.ListRasters()
arcpy.CheckOutExtension('Spatial')
outCellStats = CellStatistics(razList,STYPE,"NODATA")
outCellStats.save(outfile)

### profit
