from ._anvil_designer import RowTemplate6Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...black_tee import black_tee
from ...white_tee import white_tee
import re


class RowTemplate6(RowTemplate6Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.server.call('test_cookie')
    # if self.label_3.text == 0:
    #   self.trash_click()

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    match = re.search(r"inscription\s+(.*?),(.*)", self.link_1.text)
    first_part = match.group(1).strip()
    second_part = match.group(2).strip()
    if 'Black' in self.link_1.text:
      alert(black_tee(first_part, second_part), large=True)
    else:
      alert(white_tee(first_part, second_part), large=True)

  def trash_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.server.call('trash_item', self.user, self.label_1.text)
    self.parent.raise_event('x-refresh-list')

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.server.call('add_minus_item', self.user, self.label_1.text, 'add', None)
    self.parent.raise_event('x-refresh-list')

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.server.call('add_minus_item', self.user, self.label_1.text, 'minus', None)
    self.parent.raise_event('x-refresh-list')
