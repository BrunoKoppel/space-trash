class limb:
  name = ""
  limb_type = ""
  condition = 0

class Chest:
  condition = 0

class Head:
  condition = 0

class Body:
  head = Head
  chest = Chest
  limbs = []
  physical_stats = []
