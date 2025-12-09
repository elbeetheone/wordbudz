from ._anvil_designer import gameplayTemplate
from anvil import *
import anvil.server
from ..voice_rec import voice_rec
import time
from datetime import date
import re
from ..vidhtml import vidhtml
from ..sound_viz import sound_viz
from ..sound_viz_response import sound_viz_response




class gameplay(gameplayTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.link_1.text = anvil.server.call_s('test_cookie')
    self.link_1.visible = False
    self.nug = 10




  def change_sound_viz(self, **event_args):
    """This method is called when the button is clicked"""
    if self.nug%2 == 0:
      # self.card_2.visible = True
      # self.card_3.visible = False
      self.card_2.clear()
      self.card_2.add_component(sound_viz())
      self.refresh_data_bindings()
    else:
      # self.card_2.visible = False
      # self.card_3.visible = True
      self.card_2.clear()
      self.card_2.add_component(sound_viz_response())
      self.refresh_data_bindings()
    self.nug -=1

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.call_js('stopRecognition')
    time.sleep(5)
    self.card_1.clear()
    self.card_1.add_component(voice_rec(), full_width_row=True)


  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('ace_it')

  def speak_rec_1_button_click(self, **event_args):
    """This method is called handle-click"""
    self.change_sound_viz()












