from living_being import LivingBeing
from ..world_objects.meta_data import Location

class FactionMember(LivingBeing):
  rank_title = ""
  rank = 0


class Faction:
  name = ""
  capital_location = Location
  towns = []
  members = []
  allies = []
  enemies = []
