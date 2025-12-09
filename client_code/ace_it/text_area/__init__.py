from ._anvil_designer import text_areaTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class text_area(text_areaTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.server.call_s('test_cookie')
    # Any code you write here will run before the form opens.

  def text_area_1_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    anvil.server.call_s('user_jd', self.text_area_1.text, self.user)
