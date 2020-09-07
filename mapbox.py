import numpy as np
import pandas as pd
import matplotlib as mpl 
import seaborn as sns
# sns.set()
sns.set(context='notebook', style='whitegrid', palette='deep', font='sans-serif', font_scale=1.3, color_codes=True, rc=None)
import matplotlib.pyplot as plt
import geopandas as gpd
import geoplot as gpl
import json
import mapclassify
import matplotlib.ticker as ticker

from mapboxgl.viz import *
from mapboxgl.utils import *

# %matplotlib inline

# Must be a public token, starting with `pk`
token = 'pk.eyJ1IjoiZGplZmZrYW5kYSIsImEiOiJja2VlMDR1aG0wZzdzMnlrZmhkMnRwMHgxIn0.uN2NmnZHgckSTzI28ZgCIg'

# Must be a public token, starting with `pk`
# token = os.getenv('MAPBOX_ACCESS_TOKEN')

# Create Choropleth with GeoJSON Source
viz = ChoroplethViz('./mobgen.geojson',
                     color_property='Volume_x',
                     color_stops=create_color_stops([0, 50, 100, 500, 1500], colors='YlOrRd'),
                     color_function_type='interpolate',
                     line_stroke='--',
                     line_color='rgb(128,0,38)',
                     line_width=1,
                     line_opacity=0.9,
                     opacity=0.8,
                     center=(-96, 37.8),
                     zoom=3,
                     below_layer='waterway-label')
viz.show()