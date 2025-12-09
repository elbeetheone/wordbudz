from ._anvil_designer import RowTemplate3Template
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if self.league_title.text != 'Vulcan League':
      self.league_title.enabled = False

    # Any code you write here will run before the form opens.


  def league_title_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.server.call_s('test_cookie')
    if anvil.server.call('join_league', self.league_title.text.replace(' ','_'), user) == 'reload':
      open_form('wordbudz.League')
