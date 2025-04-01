from vpython import *

# Константы
g = 9.81  # ускорение свободного падения (м/с²)
dt = 0.01  # шаг времени

# Начальная скорость шара
ball_velocity = vector(10, 0, 0)  # начальная скорость: покой
reflect_ball = 0.8
rotation_velocity = 2*pi
# Создание сцены
scene1 = canvas(title='Test', x=0, y=0, width=800,
                height=500, background=color.black)
ball = sphere(pos=vector(-100, 20, 0), radius=5,
              color=color.red, texture=textures.metal)
table = box(pos=vector(0, -10, 0), length=200, height=10,
            width=100, color=color.yellow, texture=textures.wood)

# Основной цикл
while True:
    rate(100)  # 100 кадров в секунду

    # Обновление скорости с учётом ускорения тяжести
    ball_velocity += vector(1, -g, 0) * dt

    # Обновление положения
    ball.pos += ball_velocity * dt
    ball.rotate(angle=rotation_velocity*dt,
                axis=vector(0, 0, -1), origin=ball.pos)
    # Проверка столкновения с верхней поверхностью стола
    if ball.pos.y - ball.radius < table.pos.y + table.height / 2:
        # инверсия вертикальной скорости (отскок)
        ball_velocity.y = -ball_velocity.y*reflect_ball
