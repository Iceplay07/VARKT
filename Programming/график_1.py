import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import math

g = 9.81
M0 = 39646.6

T0 = 1004146.3
Isp = 297.7
k = T0 / (Isp * g)

A = 79.3
Cd = 0.30

p0 = 1.225
H = 8500

t_burn = 28796.6 / k

a = math.pi / 2
b = (math.pi / 4) / 120

def F(s, t, T0, p0, M0, k, a, b, H, g, A, Cd):
    x, y, vy, vx = s

    if t <= t_burn:
        m = M0 - k * t
        thrust = T0
    else:
        m = M0 - k * t_burn
        thrust = 0

    rho = p0 * math.exp(-y / H)

    speed = math.sqrt(vx ** 2 + vy ** 2)

    if speed > 0:
        F_drag = 0.5 * rho * speed ** 2 * A * Cd
        F_drag_x = -F_drag * (vx / speed)
        F_drag_y = -F_drag * (vy / speed)
    else:
        F_drag_x = 0
        F_drag_y = 0

    if t < 15:
        pitch_angle = math.pi / 2
    else:
        pitch_angle = a - b * (t - 15)

    pitch_angle = max(pitch_angle, math.pi / 4)

    dx = vx
    dy = vy
    dy1 = (thrust * math.sin(pitch_angle) + F_drag_y) / m - g
    dx1 = (thrust * math.cos(pitch_angle) + F_drag_x) / m

    return [dx, dy, dy1, dx1]

s0 = [0, 72.9, 0, 0]

t = np.linspace(0, 140, 2000)

sol = odeint(F, s0, t, args=(T0, p0, M0, k, a, b, H, g, A, Cd))

x = sol[:, 0]
y = sol[:, 1]
vy = sol[:, 2]
vx = sol[:, 3]

v_total = np.sqrt(vx ** 2 + vy ** 2)

plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
plt.plot(x, y, 'b-', linewidth=2)
plt.xlabel('Горизонтальное расстояние (м)')
plt.ylabel('Высота (м)')
plt.title('Траектория полета ракеты')
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(t, y, 'g-', linewidth=2)
plt.xlabel('Время (с)')
plt.ylabel('Высота (м)')
plt.title('Высота от времени')
plt.grid(True)

plt.tight_layout()
plt.show()