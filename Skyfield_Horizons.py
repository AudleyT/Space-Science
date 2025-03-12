from astroquery.jplhorizons import Horizons
from skyfield.api import Star, load, wgs84
from skyfield.data import hipparcos
from skyfield.projections import build_stereographic_projection
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle

# Obtaining ephemeride data for a celestial object
jupiter = Horizons(id='599', location='568', epochs={'start':'2000-01-10', 'stop':'2024-01-10', 'step':'1y'})
eph = jupiter.ephemerides()
print(eph)

# ------------------------------------------------

ts = load.timescale()

# input timescale
t = ts.utc(2021, 2, 26, 15, 19)

# input geographic coardinates
lat, long = 51.146, 0.875

# load planetrary data
planets = load('de421.bsp') # Planetary constants kernels, size, shape and orientation of bodies
jupiter = planets['Jupiter Barycenter']
earth = planets['Earth Barycenter']
barycentric = jupiter.at(t)

# load star data
with load.open(hipparcos.URL) as f:
    stars = hipparcos.load_dataframe(f)

# Define observer location at specific latitude & longitude in the world geodetic system 
observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=long).at(t)

# Define position in the sky the observer will look at 
position = observer.from_altaz(alt_degrees=90, az_degrees=0)

# Centre the observer 
ra, dec, distance = observer.radec()
center_object = Star(ra=ra, dec=dec)

# Find position of Jupiter relative to Earth and build a 180 deg projection
center = earth.at(t).observe(center_object)
projection = build_stereographic_projection(center)
field_of_view_degrees = 180.0

# Star positions calculation
star_positions = earth.at(t).observe(Star.from_dataframe(stars))
stars['x'], stars['y'] = projection(star_positions)

chart_size = 10
max_star_size = 100
limiting_magnitude = 10

# Create a filter that only shows stars of a specific magnitude or greater
bright_stars = (stars.magnitude <= limiting_magnitude)
magnitude = stars['magnitude'][bright_stars]

# Size of the star depends on the star size and magnitude of brightness
marker_size = max_star_size * 10 ** (magnitude / -2.5)

# Figure plot
fig, ax = plt.subplots(figsize=(chart_size, chart_size))
    
border = plt.Circle((0, 0), 1, color='black', fill=True)
ax.add_patch(border)

ax.scatter(stars['x'][bright_stars], stars['y'][bright_stars],
           s=marker_size, color='white', marker='.', linewidths=0, 
           zorder=2)

horizon = Circle((0, 0), radius=1, transform=ax.transData)
for col in ax.collections:
    col.set_clip_path(horizon)

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
plt.title(f"Sky Map of Jupyter Barycenter relative to ({lat}, {long})")
plt.show()