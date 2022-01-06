import pygame

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)

# Loop until the user clicks the close button.
is_game_running = True

# Used to manage how fast the screen updates
game_clock = pygame.time.Clock()
game_screen_width = 1280
game_screen_height = 720

screen = pygame.display.set_mode([game_screen_width, game_screen_height])

# -------- Main Program Loop -----------
while is_game_running:
  # --- Main event loop
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      is_game_running = False
      print("User asked to quit.")
    elif event.type == pygame.KEYDOWN:
      print("User pressed a key.")
    elif event.type == pygame.KEYUP:
      print("User let go of a key.")
    elif event.type == pygame.MOUSEBUTTONDOWN:
      print("User pressed a mouse button")  

  # --- Game logic should go here
  
  # --- Drawing code should go here

  # First, clear the screen to white. Don't put other drawing commands
  # above this, or they will be erased with this command.
  screen.fill(WHITE)

  # --- Go ahead and update the screen with what we've drawn.
  pygame.display.flip()

  # --- Limit to 60 frames per second
  game_clock.tick(60)
