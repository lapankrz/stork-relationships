import rasterio as rio
from pyproj import Proj

lat = [49.4538163,49.1893459,48.0996548,49.2103917,47.7683835]
long = [7.5293362,8.3806152,7.3811118,8.1805128,9.2178378]

tif = rio.open('landuse.tif', crs='epsg:3035')
band_id = 1
land_use = tif.read(band_id)

def convert_coords_to_xy(latitude, longitude):
    p1 = Proj("epsg:3035")
    px, py =  p1(longitude, latitude)
    px_pc = (px - tif.bounds.left) / (tif.bounds.right - tif.bounds.left)
    py_pc = (tif.bounds.top - py) / (tif.bounds.top - tif.bounds.bottom)
    return (round(px_pc * tif.width), round(py_pc * tif.height))

def get_land_use_category(id):
    category = 'N/A'
    if id in range(1,12):
        category = 'urban'
    if id in [12,13,14,19,20,21]:
        category = 'farm field'
    if id in [15,16,17]:
        category = 'orchard'
    if id == 18:
        category = 'pasture'
    if id in [22,23,24,25,29]:
        category = 'forest'
    if id in [26,27,28,31,32]:
        category = 'grassland'
    if id == 30:
        category = 'beach'
    if id in range(35,45):
        category = 'water'
    return category

for i in range(len(lat)):
    x, y = convert_coords_to_xy(lat[i], long[i])
    use = land_use[y][x]
    use_name = get_land_use_category(use)
    print("X,Y: %d, %d, Coordinates: %f, %f, Use ID: %d, Land use: %s" % (x, y, lat[i], long[i], use, use_name))