from ._anvil_designer import message_usTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class message_us(message_usTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.server.call('test_cookie')

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert('Sent. Thanks for your message')
    anvil.server.call('message', self.user, self.text_box_1.text, self.email.text, self.message.text)
    self.button_1.enabled = False
    self.text_box_1.text = ''
    self.email.text = ''
    self.message.text = ''
