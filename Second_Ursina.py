from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Player
player = FirstPersonController()
player.gravity = 1

# Ground (solid cube, not plane)
ground = Entity(
    model='cube',
    scale=(30,1,30),
    position=(0,-0.5,0),
    color=color.gray,
    collider='box'
)

# Walls
wall_thickness = 1
wall_height = 5
arena_size = 30

wall1 = Entity(model='cube', scale=(arena_size, wall_height, wall_thickness),
               position=(0, wall_height/2, arena_size/2), collider='box')

wall2 = Entity(model='cube', scale=(arena_size, wall_height, wall_thickness),
               position=(0, wall_height/2, -arena_size/2), collider='box')

wall3 = Entity(model='cube', scale=(wall_thickness, wall_height, arena_size),
               position=(arena_size/2, wall_height/2, 0), collider='box')

wall4 = Entity(model='cube', scale=(wall_thickness, wall_height, arena_size),
               position=(-arena_size/2, wall_height/2, 0), collider='box')

app.run()

#It sets up a ground plane and four walls to create an enclosed arena. The player can move around freely within the arena using the first-person controls, and the walls prevent the player from leaving the area.
