from ._anvil_designer import anchorlabsTemplate
from anvil import *
import anvil.server
# from ..username import username
# from ..Word_info import Word_info
from ..avgs import avgs
from ..ratings import ratings
import time
from .anchor_info import anchor_info
from datetime import date


class anchorlabs(anchorlabsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load = anvil.server.call('test_cookie')
    self.ratings = anvil.server.call("test_ratings", 'anchors')
    print(self.ratings)
    self.date.text = str(date.today().strftime("%a, %b %d."))
    if self.ratings[0]['Played_time'] == 0:
      alert(anchor_info(), large=True)
    self.label_1.text = f'👋 {self.load}'



  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('anchorlabs.gameplay')

  def stats_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(avgs(), large=True)


  def ranking_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(ratings('anchors'), large=True)

  def play_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('anchorlabs.gameplay')

  def rank_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(ratings('anchors'), large=True)


  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('home')

  def how_to_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(anchor_info(), large=True)

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.link_2_click()

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(avgs('anchors'), large=True)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.rank_click()

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.play_click()

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('anchorlabs.your_speech')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.link_4_click()
