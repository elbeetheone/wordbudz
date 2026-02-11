from ._anvil_designer import item_statusTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class item_status(item_statusTemplate):
  def __init__(self, user, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    item_list = anvil.server.call('item_info', user, 'item')
    if item_list is None:
      self.label_1.text = 'After Ordering, Track Your Items Here'
    else:
      self.repeating_panel_2.items = item_list

