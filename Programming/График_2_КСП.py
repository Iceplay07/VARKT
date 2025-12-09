import krpc
import time
import matplotlib.pyplot as plt


conn = krpc.connect(name='')
vessel = conn.space_center.active_vessel


real_times = []
speeds = []
start_time = conn.space_center.ut
while True:

    current_time = conn.space_center.ut - start_time

    speed = vessel.flight(vessel.orbit.body.reference_frame).speed

    real_times.append(current_time)
    speeds.append(speed)


    if current_time >= 90:
        break

    time.sleep(0.2)




graph_times = [t  for t in real_times]


plt.plot(graph_times, speeds, 'b-', linewidth=3)

plt.xlim(0, 90)
plt.ylim(bottom=0)


plt.xlabel('Время (с)', fontsize=14, fontweight='bold')
plt.ylabel('Скорость (м/с)', fontsize=14, fontweight='bold')
plt.title('Зависимость скорости от времени ', fontsize=16, fontweight='bold')


plt.xticks(range(0, 91, 10), fontsize=12)
plt.yticks(fontsize=12)


plt.grid(True, linestyle='--', alpha=0.7)


plt.show()


