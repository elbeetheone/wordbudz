from ._anvil_designer import ratingsTemplate
from anvil import *
import anvil.server
from anvil import js
from .. import GlobalState



class ratings(ratingsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    data = GlobalState.get_user_info()
    self.label_5.text = data['user']
    self.repeating_panel_1_copy.items = data['ratings']
    self.data_grid_1_copy.rows_per_page = 10
    user_rank = next((item['rank'] for item in data['ratings'] if item['user'] == self.label_5.text), "N/A")
    self.rank.text = f"Rank: {user_rank}"

