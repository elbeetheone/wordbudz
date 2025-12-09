from ._anvil_designer import RowTemplate4Template
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate4(RowTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if self.label_4.text is not None:
      self.label_4.text = "%.2f" %(self.label_4.text)

    # Any code you write here will run before the form opens.
