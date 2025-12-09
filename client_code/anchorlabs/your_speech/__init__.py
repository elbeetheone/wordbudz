from ._anvil_designer import your_speechTemplate
from anvil import *
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q




class your_speech(your_speechTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('anchorlabs')
