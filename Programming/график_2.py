import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Параметры
m0 = 41650
m_fuel = 28796.6
F_thrust = 1_004_146.3
Isp = 300
A = 79.3
Cd = 0.30
rho0 = 1.225
H = 8500
g = 9.81

# Время работы двигателя
burn_time = m_fuel / (F_thrust / (Isp * g))


# Система уравнений
def rocket_eq(state, t):
    h, v = state

    # Масса и тяга
    if t <= burn_time:
        m = m0 - (F_thrust / (Isp * g)) * t
        thrust = F_thrust
    else:
        m = m0 - (F_thrust / (Isp * g)) * burn_time
        thrust = 0

    # Сопротивление
    rho = rho0 * np.exp(-h / H)
    drag = 0.5 * rho * v ** 2 * Cd * A * (1 if v >= 0 else -1)

    # Уравнения
    dh_dt = v
    dv_dt = (thrust - drag - m * g) / m

    return [dh_dt, dv_dt]


# Решение
time = np.linspace(0, 90, 900)
sol = odeint(rocket_eq, [72.9, 0], time)

# График скорости
plt.plot(time, sol[:, 1], 'b-', linewidth=2)
plt.xlabel('Время, с')
plt.ylabel('Скорость, м/с')
plt.title('Скорость ракеты от времени')
plt.grid(True)
plt.show()