from ._anvil_designer import word_videoTemplate
from anvil import *
import anvil.server


class word_video(word_videoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
