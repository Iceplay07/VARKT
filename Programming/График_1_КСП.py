import krpc
import time
import matplotlib.pyplot as plt
import math


conn = krpc.connect(name='')
vessel = conn.space_center.active_vessel


real_times = []
altitudes = []
horizontal_distances = []


start_time = conn.space_center.ut
start_position = vessel.position(vessel.orbit.body.reference_frame)
prev_position = start_position

while True:

    current_time = conn.space_center.ut - start_time

    altitude = vessel.flight().mean_altitude

    current_position = vessel.position(vessel.orbit.body.reference_frame)

    dx = current_position[0] - start_position[0]
    dz = current_position[2] - start_position[2]
    horizontal_distance = math.sqrt(dx ** 2 + dz ** 2)

    real_times.append(current_time)
    altitudes.append(altitude)
    horizontal_distances.append(horizontal_distance)

    if current_time >= 140:
        break


    time.sleep(0.2)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# График 1: Высота от времени
ax1.plot(real_times, altitudes, 'g-', linewidth=3)
ax1.set_xlim(0, 140)
ax1.set_ylim(bottom=0)
ax1.set_xlabel('Время (с)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Высота (м)', fontsize=12, fontweight='bold')
ax1.set_title('Зависимость высоты от времени', fontsize=14, fontweight='bold')
ax1.set_xticks(range(0, 141, 20))
ax1.grid(True, linestyle='--', alpha=0.7)

# График 2: Траектория (высота от горизонтального расстояния)
ax2.plot(horizontal_distances, altitudes, 'r-', linewidth=3)
ax2.set_xlim(0, max(horizontal_distances) * 1.05)
ax2.set_ylim(bottom=0)
ax2.set_xlabel('Горизонтальное расстояние (м)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Высота (м)', fontsize=12, fontweight='bold')
ax2.set_title('Траектория полета', fontsize=14, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()

plt.show()

