from ._anvil_designer import wordbudzTemplate
from anvil import *
import anvil.server
# from ..username import username
from .Word_info import Word_info
import time
from datetime import date
from anvil.js.window import location
from ..avgs import avgs
from ..ratings import ratings
from .vidhtml import vidhtml


class wordbudz(wordbudzTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.timer_1.interval = 0
    self.load = anvil.server.call('test_cookie')
    self.ratings = anvil.server.call("test_ratings", 'word')
    self.date.text = str(date.today().strftime("%a, %b %d."))
    if self.ratings[0]['Played_time'] == 0:
      self.how_to.scroll_into_view()
      # self.timer_2_tick()
    self.label_1.text = f'👋 {self.load}'


  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('wordbudz.global_wordbuds')

  def stats_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(avgs('word'), large=True)

  def daily_game_click(self, **event_args):
    """This method is called when the link is clicked"""
    try:
      if anvil.server.call('len_league', 'word') == 0:
        url = '''https://speakeasi.streamlit.app/?embedded=true&bar=paste&route=word&foo=100'''
        self.card_1.add_component(vidhtml(url))
        self.timer_1_tick()
      else:
        open_form('wordbudz.global_wordbuds')
    except Exception as e:
      print(e)
      # pass

  def ranking_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(ratings('word'), large=True)

  def play_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.link_1_copy_click()

  def rank_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.ranking_click()

  def league_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('wordbudz.closed_league_sub')

  def link_1_copy_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.league_click()

  def how_to_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(Word_info(), large=True)

  def merch_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('merch')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('home')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.stats_click()

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.merch_click()

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.daily_game_click()

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.timer_1.interval = 5
    try:
      if anvil.server.call('len_league', 'daily') != 0:
        self.timer_1.interval = 0
        open_form('wordbudz.global_wordbuds')
        # else:
        #   open_form('gameplay')
    except Exception as e:
      print(e)
      pass


def error_handler(err):
  open_form('error')

set_default_error_handling(error_handler)