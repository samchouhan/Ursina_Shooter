#This is the Base Game code and now we can make alterations to it to make it more fun and enjoyable. We can add more enemies, different types of enemies, power-ups, and more.
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
    color=color.yellow,
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


##Enemy Spawning

class Enemy(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            position=position,
            collider='box'
        )

        # Body (Torso)
        self.body = Entity(
            parent=self,
            model='cube',
            scale=(1,1.5,0.5),
            color=color.red,
            y=1
        )

        # Head
        self.head = Entity(
            parent=self,
            model='cube',
            scale=(0.6,0.6,0.6),
            color=color.orange,
            y=2.2
        )

        # Left Arm
        self.left_arm = Entity(
            parent=self,
            model='cube',
            scale=(0.3,1.2,0.3),
            color=color.red,
            position=(-0.8,1.2,0)
        )

        # Right Arm
        self.right_arm = Entity(
            parent=self,
            model='cube',
            scale=(0.3,1.2,0.3),
            color=color.red,
            position=(0.8,1.2,0)
        )

        # Left Leg
        self.left_leg = Entity(
            parent=self,
            model='cube',
            scale=(0.4,1.2,0.4),
            color=color.blue,
            position=(-0.3,0,0)
        )

        # Right Leg
        self.right_leg = Entity(
            parent=self,
            model='cube',
            scale=(0.4,1.2,0.4),
            color=color.blue,
            position=(0.3,0,0)
        )
        
enemies = []
for i in range(5):
    enemy = Enemy(position=(random.randint(-10,10),0,random.randint(-10,10)))
    enemies.append(enemy)    
    
        
## Raycasting 
def input(key):
    if key == 'left mouse down':
        hit_info = raycast(
            camera.world_position,
            camera.forward,
            distance=50
        )

        if hit_info.hit:
            if hit_info.entity in enemies:
                destroy(hit_info.entity)
                enemies.remove(hit_info.entity)   

##Crosshair
crosshair_parts = []

thickness = 0.002
length = 0.02
gap = 0.01

# Top
crosshair_parts.append(Entity(parent=camera.ui, model='quad',
    scale=(thickness, length),
    position=(0, gap, -0.1)))

# Bottom
crosshair_parts.append(Entity(parent=camera.ui, model='quad',
    scale=(thickness, length),
    position=(0, -gap, -0.1)))

# Left
crosshair_parts.append(Entity(parent=camera.ui, model='quad',
    scale=(length, thickness),
    position=(-gap, 0, -0.1)))

# Right
crosshair_parts.append(Entity(parent=camera.ui, model='quad',
    scale=(length, thickness),
    position=(gap, 0, -0.1)))



app.run()
