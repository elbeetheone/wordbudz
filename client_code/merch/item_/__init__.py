from ._anvil_designer import item_Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class item_(item_Template):
  def __init__(self, user, item_list, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.set_event_handler('x-refresh-list', self.reload)
    self.item_list = item_list
    self.user = user
    self.label_1.text = 'Total: $' + "%.2f" % (sum([item["price"] * item['num_item'] for item in item_list if "price" in item]))
    self.repeating_panel_1.items = item_list
    self.address.text = anvil.server.call_s('get_addy')
    

  def reload(self, **event_args):
    self.item_list = anvil.server.call('item_info', self.user)
    try:
      if self.item_list is not None:
        self.label_1.text = 'Total: $' + "%.2f" % (sum([item["price"] * item['num_item'] for item in self.item_list if "price" in item]))
        self.repeating_panel_1.items = self.item_list
      if self.item_list is None:
        self.raise_event("x-close-alert", value=42)
        
      # Any code you write here will run before the form opens.
    except Exception as e:
      pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    #take sum of items and pass to stripe. Update dict to paid afterwards if successful
    if self.address.text in [None, '']:
      alert('Please supply a delivery address')
    else:
      try:
        anvil.server.call_s('store_addy', self.user, self.address.text, self.country.selected_value)
        c = stripe.checkout.charge(
          currency="USD", 
          amount=sum([item["price"] for item in self.item_list if "price" in item]) * 100,
          icon_url="_/theme/download.png"
        )
        if c['result'] == 'succeeded':
          open_form('merch')
      except Exception as e:
        alert(e)
        


