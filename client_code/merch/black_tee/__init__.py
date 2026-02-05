from ._anvil_designer import black_teeTemplate
from anvil import *
import anvil.server
# import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class black_tee(black_teeTemplate):
  def __init__(self, text, text2, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label1.text = text
    self.label2.text = text2


