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
from anvil.js import window


class black_tee(black_teeTemplate):
  def __init__(self, text = 'tesd', text2='test', **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label1.text = text
    self.label2.text = text2

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    # This component becomes the reference point
    from anvil.js import get_dom_node
    element = get_dom_node(self.card_7)
    window.cardToPNG(element, 'my_card.png')


