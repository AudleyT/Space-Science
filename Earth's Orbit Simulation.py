import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# Constants (SI units)
G = 6.674e-11  # m^3 kg^-1 s^-2
M_sun = 1.989e30  # kg

# Initial conditions (SI units)
r0 = np.array([147.1e9, 0])  # meters (147.1 million km) Earth to Sun
v0 = np.array([0, -30290])  # meters/second (30.29 km/s)

state0 = np.concatenate((r0, v0))  # Combine position and velocity into a single state vector    [147100000000, 0, 0, -30290]
t_span = (0, 3.154e7)  # 1 year in seconds

def ODE(t, state):
    r = state[:2]  # Position vector (x, y)
    v = state[2:]  # Velocity vector (vx, vy)

    drdt = v  # Change in position is velocity
    dvdt = (-G * M_sun / np.linalg.norm(r)**3) * r  # Gravitational acceleration

    return np.concatenate((drdt, dvdt))

# Solve the ODE
y = solve_ivp(ODE, t_span, state0,
              rtol=1e-12,  # Reduced relative tolerance
              atol=1e-12,  # Reduced absolute tolerance
              t_eval=np.linspace(t_span[0], t_span[1], 3600))

# Plot the orbit
plt.style.use('dark_background')
plt.plot(y.y[0], y.y[1])  # Plot y vs x
plt.xlabel('X (meters)')
plt.ylabel('Y (meters)')
  # Make the axes scaled equally


fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection = '3d')

ax.plot(y.y[0], y.y[1], color='blue', label='Earth')
ax.scatter(0, 0, 0, color='yellow', marker='o', s=100, label='Sun')
plt.title('Earths Orbit around the Sun')
plt.axis('off')
ax.legend()
plt.show()