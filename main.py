import pygame
import random 
import sys
from game_maps.demo_maps import DemoMaps
from pygame.locals import *

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)

# Loop until the user clicks the close button.
is_game_running = True

# Used to manage how fast the screen updates
FPS = 60
game_clock = pygame.time.Clock()

# Display Settings
game_screen_width = 1280
game_screen_height = 720
WINDOW_SIZE = (game_screen_width, game_screen_height)
zoom = 2


# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface((int((game_screen_width / zoom)),int((game_screen_height / zoom))))
pygame.display.set_caption('Empire Simulator')
clock = pygame.time.Clock()

camera = pygame.Rect(0, 0, 5, 16)
player_img = pygame.transform.scale(pygame.image.load('assets/player_20x20.png'), (16,16)).convert()
grass_img = pygame.transform.scale(pygame.image.load('assets/grass_20x20.png'), (16,16)).convert()
dirt_img = pygame.transform.scale(pygame.image.load('assets/dirt_20x20.png'), (16,16)).convert()
game_map = DemoMaps.dirt_platform

def collision_test(rect,tiles):
  collisions = []
  for tile in tiles:
    if rect.colliderect(tile):
      collisions.append(tile)
  return collisions
 
def move(rect, movement, tiles):
  collision_direction = {'up': False, 'down': False, 'right': False, 'left' : False}
  
  rect.x += movement[0]
  collisions = collision_test(rect, tiles)
  for tile in collisions:
    if movement[0] > 0:
      rect.right = tile.left
      collision_direction['right'] = True
    if movement[0] < 0:
      rect.left = tile.right
      collision_direction['left'] = True
          
  rect.y += round(movement[1])
  collisions = collision_test(rect, tiles)
  for tile in collisions:
    if movement[1] > 0:
      rect.bottom = tile.top
      collision_direction['down'] = True
    if movement[1] < 0:
      rect.top = tile.bottom
      collision_direction['up'] = True
          
  return rect, collision_direction

def scrollMap(x, y):
    scroll[0] = camera.x - int(WINDOW_SIZE[0]/ (zoom * 2)) + 2
    scroll[1] = camera.y - int(WINDOW_SIZE[1]/ (zoom * 2)) + 5

movement_speed = 2
moving_right = False
moving_left = False
moving_up = False
moving_down = False

ctrl_pressed = False
equals_pressed = False
minus_pressed = False
zero_pressed = False

player_y_momentum = 0

air_timer = 0
scroll = [0, 0]
running = True

# Game loop
while running:
  for event in pygame.event.get():
    if event.type == QUIT:
      print("Event Type => " + str(event.type))
      running = False
    if event.type == KEYDOWN:
      print("Event Type => " + str(event.type))
      if event.key == K_RIGHT or event.key == K_d:
        print("Event Key => " + str(event.key))
        moving_right = True
      if event.key == K_LEFT or event.key == K_a:
        print("Event Key => " + str(event.key))
        moving_left = True
      if event.key == K_UP or event.key == K_w:
        print("Event Key => " + str(event.key))
        if air_timer < 3:
          player_y_momentum = -4
      if event.key == K_DOWN or event.key == K_s:
        print("Event Key => " + str(event.key))
        moving_down = True
              
    if event.type == KEYUP:
      print("Event Type => " + str(event.type))
      if event.key == K_RIGHT or event.key == K_d:
        print("Event Key => " + str(event.key))
        moving_right = False
      if event.key == K_LEFT or event.key == K_a:
        print("Event Key => " + str(event.key))
        moving_left = False
      if event.key == K_UP or event.key == K_w:
        print("Event Key => " + str(event.key))
        moving_up = False
      if event.key == K_DOWN or event.key == K_s:
        print("Event Key => " + str(event.key))
        moving_down = False

    # Proccess to register Mouse clicks Down
    if event.type == MOUSEBUTTONDOWN:
      print("Event Key => " + str(event))
      if event.button == 1:
        scrollMap(event.pos[0],event.pos[1])

      
    # Proccess to register Mouse click Up
    if event.type == MOUSEBUTTONUP:
      print("Event Key => " + str(event))
      

    # ZOOM IN and OUT process
    if event.type == MOUSEWHEEL:
      print("Event Key => " + str(event))
      if event.y > 0:
        zoom += 0.15
        print('Zooming In | Current Zoom = ' + str(zoom))
      if event.y < 0:
        zoom -= 0.15
        print('Zooming Out | Current Zoom = ' + str(zoom))
      if event.y == 0:
        zoom = 2
        print('Zoom Reset | Current Zoom = ' + str(zoom))
      
  try:   
    display = pygame.Surface((int(WINDOW_SIZE[0] / zoom), int(WINDOW_SIZE[1] / zoom)))
  except:
    zoom = 0.1

  display.fill((5, 195, 225))

  tile_rect = []
  y = 0
  for layer in game_map:
    x = 0
    for tile in layer:
      if tile == '1':
        display.blit(grass_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
      if tile == '2':
        display.blit(dirt_img, (x * 16 - scroll[0], y * 16 - scroll[1]))
      if tile != '0':
        tile_rect.append(pygame.Rect(x * 16, y * 16, 16, 16))
        x += 1
      y += 1

  # scroll[0] += ((camera.x - int(WINDOW_SIZE[0]/ (zoom * 2)) + 2) - scroll[0]) / 12
  # scroll[1] += ((camera.y - int(WINDOW_SIZE[1]/ (zoom * 2)) + 5) - scroll[1]) / 12

  
  player_movement = [0, 0]
  
  if moving_right:
    player_movement[0] += movement_speed
  if moving_left:
    player_movement[0] -= movement_speed
  if moving_down:
    player_movement[1] += 5    
  player_y_momentum += 0.2
  if player_y_momentum > 5:
    player_y_momentum = 5
      
  player_movement[1] += player_y_momentum
  
  camera, collision_direction = move(camera, player_movement, tile_rect)

  if collision_direction['down']:
    air_timer = 0
    player_y_momentum = 0
  else:
    air_timer += 1
      
  if collision_direction['up']:
    player_y_momentum = 0
                    
  display.blit(player_img, (camera.x - scroll[0], camera.y - scroll[1]))
  #pygame.draw.rect(display,(255, 255, 255),camera)

  #print(air_timer)      
  screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
  pygame.display.update()
  clock.tick(FPS)
    

pygame.quit()
sys.exit()