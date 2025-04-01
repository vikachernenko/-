from vpython import *
import math

# Константы
dt = 0.1
rate_multiplier = 1000  # Оставил как было, но можем уменьшить, если виснет
rotation_velocity = 2 * pi
radius_pow = 2
mu = 398600441800000

# Сцена 1: 3D-вид
scene1 = canvas(title='Test', x=0, y=0, width=900,
                height=600, background=color.black)
planet = sphere(pos=vector(0, 0, 0), radius=6000000,
                opacity=1, texture=textures.earth)
satellite = sphere(pos=vector(0, 7000000, 0), radius=300000,
                   color=color.yellow, texture=textures.stones, make_trail=True)

# Сцена 2: 2D-карта
scene2 = canvas(title='Orbit', x=0, y=0, width=400,
                height=400, background=color.black)
# Добавил камеру, чтобы карта была видна
scene2.camera.pos = vector(0, 0, 20000)
scene2.camera.axis = vector(0, 0, -20000)
table = box(pos=vector(0, 0, -5001), length=40000,
            height=20000, width=10000, texture=textures.wood)
mapbox = box(pos=vector(0, 0, 0), length=37699,
             height=18850, width=1, texture=textures.earth)
trace = curve(color=color.red, width=10)

# График радиуса
oscillation = graph(title='Radius', xtitle='time',
                    ytitle='value', fast=False, width=800)
funct1 = gcurve(color=color.blue, width=4, markers=True,
                marker_color=color.orange, label='radius')

# Начальные параметры
satellite.velocity = vector(8000, 0, 0)
zero_meridian = 0
ddd = 0
xxx = 0
lng_map_old = 0

while True:
    rate(rate_multiplier / dt)

    # Гравитация и движение спутника
    radius_vector = planet.pos - satellite.pos
    radius_vector_norm = radius_vector / radius_vector.mag
    g = mu / (radius_vector.mag ** radius_pow)
    g_vector = radius_vector_norm * g
    satellite.velocity += g_vector * dt
    satellite.pos += satellite.velocity * dt

    # Вращение планеты (перенёс сюда, чтобы было на каждом шаге)
    planet_rot_angle = rotation_velocity * dt / 86400
    planet.rotate(angle=planet_rot_angle, axis=vector(0, 1, 0))
    zero_meridian = zero_meridian - planet_rot_angle

    # Исправил условие для zero_meridian
    if zero_meridian < -pi:  # Нормализация в [-pi, pi]
        zero_meridian += 2 * pi

    # Широта и долгота
    latitude = asin(satellite.pos.y / satellite.pos.mag)
    longitude = atan2(satellite.pos.x, satellite.pos.z) + zero_meridian

    # Исправил логику карты
    lng_map = (longitude / pi) * mapbox.length / 2
    lat_map = (latitude / (pi / 2)) * mapbox.height / 2  # Добавил широту

    if ddd % 50 == 0:  # Добавляем точки чаще, без строгого условия
        lng_map = max(min(lng_map, mapbox.length / 2), -
                      mapbox.length / 2)  # Ограничение
        lat_map = max(min(lat_map, mapbox.height / 2), -mapbox.height / 2)
        # Используем append вместо пересоздания
        trace.append(pos=vector(lng_map, lat_map, 0))

    ddd += 1
    if ddd == 1000:
        ddd = 0
        xxx += 1
        funct1.plot(xxx, radius_vector.mag)
