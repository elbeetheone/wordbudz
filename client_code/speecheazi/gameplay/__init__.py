from ._anvil_designer import gameplayTemplate
from anvil import *
import anvil.server
from ..voice_rec import voice_rec



class gameplay(gameplayTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('speecheazi')


