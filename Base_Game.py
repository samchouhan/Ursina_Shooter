from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# ---------------- PLAYER ----------------
player = FirstPersonController()
player.gravity = 1


# ---------------- ARENA ----------------
ground = Entity(
    model='cube',
    scale=(30,1,30),
    position=(0,-0.5,0),
    color=color.gray,
    collider='box'
)

wall_thickness = 1
wall_height = 5
arena_size = 30

Entity(model='cube', scale=(arena_size, wall_height, wall_thickness),
       position=(0, wall_height/2, arena_size/2), collider='box')

Entity(model='cube', scale=(arena_size, wall_height, wall_thickness),
       position=(0, wall_height/2, -arena_size/2), collider='box')

Entity(model='cube', scale=(wall_thickness, wall_height, arena_size),
       position=(arena_size/2, wall_height/2, 0), collider='box')

Entity(model='cube', scale=(wall_thickness, wall_height, arena_size),
       position=(-arena_size/2, wall_height/2, 0), collider='box')


# ---------------- ENEMY CLASS ----------------
class Enemy(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(position=position)

        self.health = 100

        # Body
        self.body = Entity(parent=self, model='cube',
                           scale=(1,1.5,0.5),
                           color=color.red,
                           y=1,
                           collider='box')

        # Head (important: name it clearly)
        self.head = Entity(parent=self, model='cube',
                           scale=(0.6,0.6,0.6),
                           color=color.orange,
                           y=2.2,
                           collider='box')

        # Arms
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

        # Legs
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

    def take_damage(self, amount):
        self.health -= amount
        print("Enemy Health:", self.health)

        if self.health <= 0:
            destroy(self)
            enemies.remove(self)

# ---------------- SPAWN ENEMIES ----------------
enemies = []

for i in range(10):
    enemy = Enemy(
        position=(random.randint(-10,10),0,random.randint(-10,10))
    )
    enemies.append(enemy)


# ---------------- CROSSHAIR ----------------
# ---------------- CLASSIC CROSSHAIR ----------------
thickness = 0.003
length = 0.02
gap = 0.015

# Top
Entity(parent=camera.ui, model='quad',
       scale=(thickness, length),
       position=(0, gap, -0.1),
       color=color.black)

# Bottom
Entity(parent=camera.ui, model='quad',
       scale=(thickness, length),
       position=(0, -gap, -0.1),
       color=color.black)

# Left
Entity(parent=camera.ui, model='quad',
       scale=(length, thickness),
       position=(-gap, 0, -0.1),
       color=color.black)

# Right
Entity(parent=camera.ui, model='quad',
       scale=(length, thickness),
       position=(gap, 0, -0.1),
       color=color.black)


# ---------------- SHOOTING SYSTEM ----------------
def input(key):

    if key == 'left mouse down':

        hit_info = raycast(
            camera.world_position,
            camera.forward,
            distance=50
        )

        if hit_info.hit:

            target = hit_info.entity

            if target.parent in enemies:

                enemy = target.parent

                # HEADSHOT
                if target == enemy.head:
                    print("HEADSHOT!")
                    enemy.take_damage(100)

                # BODY / LIMB SHOT
                else:
                    enemy.take_damage(25)
app.run()
