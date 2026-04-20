from ._anvil_designer import ratingsTemplate
from anvil import *
import anvil.server
from anvil import js



class ratings(ratingsTemplate):
  def __init__(self, route, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.route = route
    self.label_5.text = anvil.server.call_s('test_cookie')
    self.repeating_panel_1.items = anvil.server.call_s('get_rank', route, 'daily')
    self.data_grid_1.rows_per_page = 10
    self.rank.text = f"Rank: {anvil.server.call('get_rank_pos', route, self.label_5.text, 'daily')}"


    # Any code you write here will run before the form opens.

  def avg_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.avg.font_size = 22
    self.daily.font_size = 14
    self.daily.enabled = True
    self.data_grid_1_copy.visible = True
    self.data_grid_1.visible = False
    self.avg.enabled = False
    self.repeating_panel_1_copy.items = anvil.server.call_s('get_rank', self.route, 'avg')
    self.data_grid_1_copy.rows_per_page = 10
    self.rank.text = f"Rank: {anvil.server.call('get_rank_pos', self.route, self.label_5.text, 'avg')}"

    

  def daily_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.avg.font_size = 14
    self.daily.font_size = 22
    self.daily.enabled = False
    self.data_grid_1_copy.visible = False
    self.data_grid_1.visible = True
    self.avg.enabled = True
    self.repeating_panel_1.items = anvil.server.call_s('get_rank', self.route, 'daily')
    self.data_grid_1.rows_per_page = 10
    self.rank.text = f"Rank: {anvil.server.call('get_rank_pos', self.route, self.label_5.text, 'daily')}"


  def is_mobile(self):
    return js.window.innerWidth < 768