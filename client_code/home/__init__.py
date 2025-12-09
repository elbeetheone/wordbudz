from ._anvil_designer import homeTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import date
import time
from ..message_us import message_us
from anvil.js.window import location


class home(homeTemplate):
  def __init__(self, route=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.date.text = str(date.today().strftime("%a, %b %d."))
    self.load = anvil.server.call('test_cookie') 
    if route is None:
      self.label_1.text = 'Hi '
      self.timer_1.interval = 1
    else:
      self.timer_1.interval = 0
      self.label_1.text = f'👋 {self.load}'

    # Any code you write here will run when the form opens.

  def word_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('wordbudz')

  def anchor_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('anchorlabs')

  def speech_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('speecheazi')

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""

    initial_delay = 0.2  # Start with a slower speed
    final_delay = 0.05   # End with a faster speed
    steps = len(self.load)
    colors = ["#344D7C", "#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1", "#034F84", "#F0E68C", "#B565A7", "#FFA07A"]

    for num in range(steps):
      self.label_1.text += self.load[num]
      self.label_1.foreground = colors[num % len(colors)]

      # Calculate the delay, decreasing it as the loop progresses
      delay = initial_delay - (initial_delay - final_delay) * (num / (steps - 1))
      time.sleep(delay)
    self.timer_1.interval = 0
    self.label_1.text, self.label_1.foreground = f'👋 {self.load}', 'theme:Primary 500'

  def ace_it_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('ace_it')

  def message_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(message_us(), large=True)
