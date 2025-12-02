import numpy as np
import matplotlib.pyplot as plt

m0 = 39646.6
m_fuel = 28796.6
F_thrust = 1_004_146.3
Isp = 297.7
A = 79.3
Cd = 0.30

rho0 = 1.225
H = 8500
g = 9.81

dt = 0.1
t_max = 90
time = np.arange(0, t_max, dt)

velocity = np.zeros_like(time)
altitude = np.zeros_like(time)
mass = np.zeros_like(time)

velocity[0] = 0.0
altitude[0] = 72.9
mass[0] = m0

burn_time = m_fuel / (F_thrust / (Isp * g))

for i in range(1, len(time)):
    t = time[i]

    if t <= burn_time:
        dm_dt = F_thrust / (Isp * g)
        mass[i] = mass[i - 1] - dm_dt * dt
        thrust = F_thrust
    else:
        mass[i] = mass[i - 1]
        thrust = 0.0

    rho = rho0 * np.exp(-altitude[i - 1] / H)

    drag = 0.5 * rho * velocity[i - 1]**2 * Cd * A * np.sign(velocity[i - 1])

    acceleration = (thrust - drag - mass[i] * g) / mass[i]

    velocity[i] = velocity[i - 1] + acceleration * dt
    altitude[i] = altitude[i - 1] + velocity[i] * dt

plt.figure(figsize=(10, 5))
plt.plot(time, velocity, 'b-', linewidth=2.5)
plt.xlabel('Время, с', fontsize=12)
plt.ylabel('Скорость, м/с', fontsize=12)
plt.title('Зависимость скорости ракеты от времени (до 100 с)', fontsize=13)
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()