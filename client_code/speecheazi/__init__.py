from ._anvil_designer import speecheaziTemplate
from anvil import *
import anvil.server
# from ..username import username
from ..avgs import avgs
import time
from ..ratings import ratings
from .speak_info import speak_info
from datetime import date

class speecheazi(speecheaziTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.route = get_url_hash()
    self.load = anvil.server.call('test_cookie')
    self.date.text = str(date.today().strftime("%a, %b %d."))
    self.label_1.text = f'👋 {self.load}'

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('speecheazi.gameplay')

  def play_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.link_1_click()

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(ratings('speecheazi'), large=True)

  def rank_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.link_3_click()

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(avgs('speecheazi'), large=True)

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.link_2_click()

  def how_to_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(speak_info(), large=True)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('home')


def error_handler(err):
  open_form('error')

set_default_error_handling(error_handler)