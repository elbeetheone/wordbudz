from ._anvil_designer import ItemTemplate2Template
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate2(ItemTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if self.label_3.text is not None:
      self.card_6.visible = True
      self.label_3.text = "%.2f" %(self.label_3.text)
      self.background = 'theme:Gray 300'
    elif self.label_3.text is None:
      self.card_6.visible = False

    # Any code you write here will run before the form opens.
