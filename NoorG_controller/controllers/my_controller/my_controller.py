from controller import Robot, GPS, Compass
import csv
import math
import time

# إعداد الروبوت
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# أجهزة الاستشعار
gps = robot.getDevice('gps')
gps.enable(timestep)

compass = robot.getDevice('compass')
compass.enable(timestep)

# المحركات
motors = []
for i in range(4):
    motor = robot.getDevice('rotor' + str(i + 1))
    motor.setPosition(float('inf'))  # وضع السرعة غير محدودة
    motor.setVelocity(1.0)  # سرعة ابتدائية منخفضة
    motors.append(motor)

# تحميل المسار من CSV
waypoints = []
with open('D:/DRON2025/Webots/waypoints_EMRSO.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        x, y, z = map(float, row)
        waypoints.append((x, y, z))

# دالة لحساب المسافة
def distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

# الانتقال بين النقاط
current_wp_index = 0
target_reached_threshold = 1.0  # متر

while robot.step(timestep) != -1 and current_wp_index < len(waypoints):
    current_position = gps.getValues()
    target_position = waypoints[current_wp_index]

    dist = distance(current_position, target_position)
    
    if dist < target_reached_threshold:
        print(f"✅ Reached waypoint {current_wp_index + 1}/{len(waypoints)}")
        current_wp_index += 1
        continue

    # مثال بسيط للتحكم في السرعة (تحتاج تطوير أكثر)
    for motor in motors:
        motor.setVelocity(5.0)  # السرعة إلى الأمام (ثابتة)

    print(f"🔄 Moving to waypoint {current_wp_index + 1}: {target_position}")
