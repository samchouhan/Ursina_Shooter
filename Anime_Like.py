#This code is about giving anime like feel to the game
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# ---------------- ANIME SKY & LIGHTING ----------------

Sky(texture='sky_sunset')  # Try: sky_default or sky_sunset

AmbientLight(color=color.rgba(255, 200, 200, 0.4))

DirectionalLight().look_at(Vec3(1,-1,-1))

# ---------------- PLAYER ----------------
player = FirstPersonController()
player.gravity = 1

player.walk_speed = 5
player.sprint_speed = 16
player.speed = player.walk_speed
player.health = 100


# ---------------- CAMERA SHAKE ----------------
def camera_shake(intensity=0.2, duration=0.2):
    original_pos = camera.position

    camera.position = original_pos + Vec3(
        random.uniform(-intensity, intensity),
        random.uniform(-intensity, intensity),
        random.uniform(-intensity, intensity)
    )

    invoke(setattr, camera, 'position', original_pos, delay=duration)


# ---------------- ARENA ----------------
arena_size = 30
wall_height = 5
wall_thickness = 1

ground = Entity(
    model='cube',
    scale=(arena_size, 1, arena_size),
    position=(0, -0.5, 0),
    color=color.light_gray,
    collider='box'
)

Entity(model='cube', scale=(arena_size, wall_height, wall_thickness),
       position=(0, wall_height/2, arena_size/2), collider='box')

Entity(model='cube', scale=(arena_size, wall_height, wall_thickness),
       position=(0, wall_height/2, -arena_size/2), collider='box')

Entity(model='cube', scale=(wall_thickness, wall_height, arena_size),
       position=(arena_size/2, wall_height/2, 0), collider='box')

Entity(model='cube', scale=(wall_thickness, wall_height, arena_size),
       position=(-arena_size/2, wall_height/2, 0), collider='box')


# ---------------- ENEMY ----------------
class Enemy(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(position=position)

        self.health = 100
        self.speed = random.uniform(1.5, 3)

        self.body = Entity(parent=self, model='cube',
                           scale=(1,1.5,0.5),
                           color=color.red,
                           y=1,
                           collider='box')

        self.head = Entity(parent=self, model='cube',
                           scale=(0.6,0.6,0.6),
                           color=color.orange,
                           y=2.2,
                           collider='box')

        self.left_arm = Entity(parent=self, model='cube',
                               scale=(0.3,1.2,0.3),
                               position=(-0.8,1.2,0),
                               color=color.red,
                               collider='box')

        self.right_arm = Entity(parent=self, model='cube',
                                scale=(0.3,1.2,0.3),
                                position=(0.8,1.2,0),
                                color=color.red,
                                collider='box')

        self.left_leg = Entity(parent=self, model='cube',
                               scale=(0.4,1.2,0.4),
                               position=(-0.3,0,0),
                               color=color.blue,
                               collider='box')

        self.right_leg = Entity(parent=self, model='cube',
                                scale=(0.4,1.2,0.4),
                                position=(0.3,0,0),
                                color=color.blue,
                                collider='box')

    def update(self):

        direction = player.position - self.position
        direction.y = 0

        distance = direction.length()

        if distance > 1.5:
            self.position += direction.normalized() * self.speed * time.dt

        self.look_at_2d(player.position, 'y')

    def take_damage(self, amount):
        self.health -= amount
        print("Enemy Health:", self.health)

        if self.health <= 0:
            enemies.remove(self)
            destroy(self)


# ---------------- SPAWN ENEMIES ----------------
enemies = []

for i in range(5):
    enemy = Enemy(
        position=(random.randint(-10,10),0,random.randint(-10,10))
    )
    enemies.append(enemy)


# ---------------- CROSSHAIR ----------------
thickness = 0.003
length = 0.02
gap = 0.015

Entity(parent=camera.ui, model='quad',
       scale=(thickness,length),
       position=(0,gap),
       color=color.black)

Entity(parent=camera.ui, model='quad',
       scale=(thickness,length),
       position=(0,-gap),
       color=color.black)

Entity(parent=camera.ui, model='quad',
       scale=(length,thickness),
       position=(-gap,0),
       color=color.black)

Entity(parent=camera.ui, model='quad',
       scale=(length,thickness),
       position=(gap,0),
       color=color.black)


# ---------------- EXPLOSION ----------------
class Explosion(Entity):
    def __init__(self, position):
        super().__init__(
            model='sphere',
            color=color.rgb(255,140,0),
            scale=0.5,
            position=position
        )
        self.duration = 0.3
        self.timer = 0

    def update(self):
        self.timer += time.dt
        self.scale += Vec3(5,5,5) * time.dt

        self.color = color.rgba(
            255,140,0,
            int(255 * (1 - self.timer/self.duration))
        )

        if self.timer >= self.duration:
            destroy(self)


# ---------------- FIREBALL ----------------
class Fireball(Entity):
    def __init__(self, position, direction):
        super().__init__(
            model='sphere',
            color=color.rgb(255,80,0),
            scale=0.6,
            position=position
        )

        self.direction = direction.normalized()
        self.speed = 25
        self.lifetime = 2

    def update(self):

        move_amount = self.direction * self.speed * time.dt

        hit_info = raycast(
            self.position,
            self.direction,
            distance=move_amount.length(),
            ignore=(self,)
        )

        if hit_info.hit:

            if hit_info.entity and hit_info.entity.parent in enemies:
                hit_info.entity.parent.take_damage(50)

            Explosion(position=hit_info.point)
            camera_shake(0.15, 0.15)

            destroy(self)
            return

        self.position += move_amount

        self.lifetime -= time.dt
        if self.lifetime <= 0:
            destroy(self)


# ---------------- WEAPONS ----------------
class Weapon:
    def __init__(self, name):
        self.name = name

    def shoot(self):
        pass


class FireballWeapon(Weapon):
    def __init__(self):
        super().__init__("Fireball")

    def shoot(self):
        Fireball(
            position=camera.world_position + camera.forward * 1.5,
            direction=camera.forward
        )


class HitscanWeapon(Weapon):
    def __init__(self):
        super().__init__("Rifle")

    def shoot(self):
        hit_info = raycast(camera.world_position, camera.forward, distance=100)

        if hit_info.hit:
            if hit_info.entity and hit_info.entity.parent in enemies:
                hit_info.entity.parent.take_damage(25)

            Explosion(position=hit_info.point)
            camera_shake(0.1,0.1)


class ShotgunWeapon(Weapon):
    def __init__(self):
        super().__init__("Shotgun")

    def shoot(self):

        for i in range(6):

            spread = Vec3(
                random.uniform(-0.05,0.05),
                random.uniform(-0.05,0.05),
                0
            )

            direction = (camera.forward + spread).normalized()

            hit_info = raycast(camera.world_position, direction, distance=50)

            if hit_info.hit:
                if hit_info.entity and hit_info.entity.parent in enemies:
                    hit_info.entity.parent.take_damage(15)

                Explosion(position=hit_info.point)

        camera_shake(0.2,0.2)


weapons = [
    FireballWeapon(),
    HitscanWeapon(),
    ShotgunWeapon()
]

current_weapon_index = 0
current_weapon = weapons[current_weapon_index]


# ---------------- INPUT ----------------
def input(key):

    global current_weapon_index, current_weapon

    if key == 'left mouse down':
        current_weapon.shoot()

    if key == '1':
        current_weapon_index = 0
        current_weapon = weapons[current_weapon_index]

    if key == '2':
        current_weapon_index = 1
        current_weapon = weapons[current_weapon_index]

    if key == '3':
        current_weapon_index = 2
        current_weapon = weapons[current_weapon_index]

    if key == 'shift':
        player.speed = player.sprint_speed

    if key == 'shift up':
        player.speed = player.walk_speed



app.run()

