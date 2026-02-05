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
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label1.text = 'text'
    self.label2.text = 'text2'

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    card_element = self.card_7.dom_nodes[0]

    def on_complete(png_url):
      # Download the PNG
      window.downloadPNG(png_url, 'my_card.png')

      # Or display it
      self.image_1.source = png_url

      # Or convert to blob for server upload
      blob = window.dataURLToBlob(png_url)
      window.logDebug('PNG generated', {'size': blob.size})

    window.convertCardToPNG(card_element, {
      'scale': 2,
      'quality': 0.95,
      'backgroundColor': '#ffffff'
    }).then(on_complete)


