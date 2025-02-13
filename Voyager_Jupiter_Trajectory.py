import spiceypy as spice
import numpy as np
import matplotlib.pyplot as plt 



print(spice.tkvrsn("TOOLKIT"))

# # load the kernels file in
spice.furnsh("VoyagerOne_Kernels/pck00011.tpc")
spice.furnsh("VoyagerOne_Kernels/naif0012.tls")
spice.furnsh("VoyagerOne_Kernels/de432s.bsp")
spice.furnsh("VoyagerOne_Kernels/vg1_v02.tf")
spice.furnsh("VoyagerOne_Kernels/vg100050.tsc")
spice.furnsh("VoyagerOne_Kernels/vg1_v02.tf")
spice.furnsh("VoyagerOne_Kernels/Voyager_1.a54206u_V0.2_merged.bsp")
spice.furnsh("VoyagerOne_Kernels/vgr1_jup230.bsp")

# # # Converting datetime strings to ephemeris time 
step = 4000
utc = ['Jan 14, 1979', 'Apr 24, 1979']

etOne = spice.str2et(utc[0])
etTwo = spice.str2et(utc[1])

print("ephemeris time one: {}, ephemeris time two: {}".format(etOne, etTwo))

# Calculate time ranges
times = [x*(etTwo - etOne)/step + etOne for x in range(step)]
print(times[0:3])

positions, lightTimes = spice.spkpos('Voyager 1', times, 'J2000', 'NONE', 'JUPITER BARYCENTER')
jupiter_pos, _ = spice.spkpos('JUPITER BARYCENTER', times, 'J2000', 'NONE', 'JUPITER BARYCENTER')

# Print out Positioning (X, Y, Z)
print("Positions: ", positions[2])

# Print out Light Times
print("Light Times: ", lightTimes[0])

spice.kclear()

# Create plots
plt.style.use('dark_background')
positions = np.asarray(positions).T # positions is a list, make it an ndarray for easier indexing
fig = plt.figure(figsize=(10, 10))
ax  = fig.add_subplot(111, projection='3d')
ax.plot(positions[0], positions[1], positions[2])

ax.scatter(positions[0][0], positions[1][0], positions[2][0], color='green', label='Start (Jan 14, 1979)')
ax.scatter(positions[0][-1], positions[1][-1], positions[2][-1], color='red', label='End (Apr 24, 1979)')
ax.legend()

# Shows the position of Jupiter 
ax.scatter(jupiter_pos[0], jupiter_pos[1], jupiter_pos[2], color='orange', label='Jupiter')
ax.legend()

plt.title('Voyager 1 Positioning Visualization made with SpiceyPy')
plt.show(block=True)