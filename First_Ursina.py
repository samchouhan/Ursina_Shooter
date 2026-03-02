#This code includes basic Grid Floor , basic movement(W,A,S,D  ) with mouse rotation 
from ursina import *

from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

player = FirstPersonController()

ground = Entity(
    model='plane',
    scale=(100,1,100),
    texture='white_cube',
    texture_scale=(100,100),
    collider='box'
)

app.run()
