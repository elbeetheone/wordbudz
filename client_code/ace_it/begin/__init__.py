from ._anvil_designer import beginTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class begin(beginTemplate):
  def __init__(self, route, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.route = route
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.route == 'gameplay':
      open_form('ace_it.gameplay')
    else:
      open_form('ace_it.gameplay_copy')
