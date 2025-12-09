from ._anvil_designer import adsTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time


class ads(adsTemplate):
  def __init__(self, **properties): #add HTML variable here
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.button_1.enabled = False
    self.timer_1.interval = 30
    self.timer_2.interval = 0.05
    # self.html = HTML

    
    
    # Any code you write here will run before the form opens.

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""

    self.timer_1.interval = 0
    self.button_1.enabled = True

  def timer_2_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.timer_2.interval = 0
    for num in range(30, 0, -1):
      self.button_1.text = str(num)
      time.sleep(1)
    self.button_1.text = 'close'

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event("x-close-alert", value=42)
