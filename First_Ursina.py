#This code includes basic Grid Floor , basic movement(W,A,S,D  ) with mouse rotation 
from ursina import *

from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

player = FirstPersonController()

ground = Entity(
    model='cube',
    scale=(100,10,100),
    position=(0,-5,0),
    texture='white_cube',
    texture_scale=(100,100),
    collider='box'
)

app.run()
