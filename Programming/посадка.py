import krpc
import time

conn = krpc.connect(name='Lunar Landing Autopilot')
vessel = conn.space_center.active_vessel

altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
vertical_speed = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'vertical_speed')

vessel.control.sas = True
time.sleep(0.1)
vessel.control.sas_mode = conn.space_center.SASMode.retrograde
time.sleep(2)

vessel.control.throttle = 1
while vessel.orbit.periapsis_altitude > 11000:
    time.sleep(0.5)
vessel.control.throttle = 0

vessel.control.sas = False
while altitude() > 8000:
    time.sleep(5)

vessel.control.sas = True
time.sleep(0.1)
vessel.control.sas_mode = conn.space_center.SASMode.retrograde
time.sleep(2)

vessel.control.sas_mode = conn.space_center.SASMode.retrograde
time.sleep(2)

while altitude() > 50:
    current_alt = altitude()
    current_vs = vertical_speed()

    if current_alt > 1500:
        target_vs = -20
        if current_vs < -100:
            throttle = 0.8
        elif current_vs < -50:
            throttle = 0.6
        elif current_vs < -30:
            throttle = 0.4
        else:
            throttle = 0.2
    else:
        target_vs = -7
        if current_vs < -30:
            throttle = 0.6
        elif current_vs < -15:
            throttle = 0.4
        else:
            throttle = 0.2

    if current_vs < target_vs:
        vessel.control.throttle = throttle
    else:
        vessel.control.throttle = 0
        time.sleep(7)

    time.sleep(0.5)

while altitude() > 10:
    current_vs = vertical_speed()
    target_vs = -3

    if current_vs < -10:
        throttle = 0.4
    elif current_vs < -5:
        throttle = 0.3
    else:
        throttle = 0.2

    if current_vs < target_vs:
        vessel.control.throttle = throttle
    else:
        vessel.control.throttle = 0

    time.sleep(0.5)

while altitude() > 1:
    current_vs = vertical_speed()
    target_vs = -0.5

    if current_vs < -3:
        throttle = 0.3
    elif current_vs < -1:
        throttle = 0.2
    else:
        throttle = 0.1

    if current_vs < target_vs:
        vessel.control.throttle = throttle
    else:
        vessel.control.throttle = 0

    time.sleep(0.2)

vessel.control.throttle = 0.05
while vertical_speed() < -0.1 and altitude() > 0.5:
    time.sleep(0.1)

vessel.control.throttle = 0