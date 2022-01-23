import rasterio as rio
from pyproj import Proj


class LandUse:
    def __init__(self):
        # https://land.copernicus.eu/pan-european/corine-land-cover/clc2018?tab=download - raster data  
        self.tif = rio.open('land-data/landuse.tif', crs='epsg:3035')
        band_id = 1
        self.data = self.tif.read(band_id)

    def get_land_use_id(self, latitude, longitude):
        x, y = self.convert_coords_to_xy(latitude, longitude)
        if 0 <= x < self.tif.width and 0 <= y < self.tif.height:
            use = self.data[y][x]
        else:
            use = -1
        return use

    def get_land_use(self, latitude, longitude):
        id = self.get_land_use_id(latitude, longitude)
        use_name = self.get_land_use_category(id)
        return use_name

    def get_land_use_color(self, category):
        color = 'white'
        if category == 'urban':
            color = 'brown'
        if category == 'farm field':
            color = 'gold'
        if category == 'orchard':
            color = 'plum'
        if category == 'pasture':
            color = 'yellowgreen'
        if category == 'forest':
            color = 'forestgreen'
        if category == 'grassland':
            color = 'lawngreen'
        if category == 'beach':
            color = 'palegoldenrod'
        if category == 'water':
            color = 'royalblue'
        return color

    def convert_coords_to_xy(self, latitude, longitude):
        try:
            p1 = Proj("epsg:3035")
            px, py = p1(longitude, latitude)
            bounds = self.tif.bounds
            px_pc = round(self.tif.width * (px - bounds.left) / (bounds.right - bounds.left))
            py_pc = round(self.tif.height * (bounds.top - py) / (bounds.top - bounds.bottom))
        except:
            px_pc = py_pc = 0
        return (px_pc, py_pc)

    # http://clc.gios.gov.pl/doc/clc/CLC_Legend_EN.pdf - "Grid_Code" column
    def get_land_use_category(self, id):
        category = 'N/A'
        if id in range(1, 12):
            category = 'urban'
        if id in [12, 13, 14, 19, 20, 21]:
            category = 'farm field'
        if id in [15, 16, 17]:
            category = 'orchard'
        if id == 18:
            category = 'pasture'
        if id in [22, 23, 24, 25, 29]:
            category = 'forest'
        if id in [26, 27, 28, 31, 32]:
            category = 'grassland'
        if id == 30:
            category = 'beach'
        if id in range(35, 45):
            category = 'water'
        return category
