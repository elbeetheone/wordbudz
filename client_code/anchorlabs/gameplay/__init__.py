from ._anvil_designer import gameplayTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go
import time
from ..voice_rec_2 import voice_rec_2
from datetime import datetime, timezone



class gameplay(gameplayTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.link_1.text = anvil.server.call_s('test_cookie')
    self.timer_1.interval = 0
    self.text = anvil.server.call('get_story')

    self.today = str(datetime.now(timezone.utc))[:10]
    if anvil.server.call('check_playtime', self.link_1.text, 'anchors') == self.today:
      #means user has played today
      self.button_1.visible = False
      self.label_5.visible, self.slow.visible, self.medium.visible, self.fast.visible = False, False, False, False
      anc = anvil.server.call_s('get_user_anc', self.link_1.text)
      media_obj_1 = anvil.server.call('get_wordcloud', self.text)
      media_obj_2 = anvil.server.call('get_wordcloud', anc)
      self.index.visible = True
      self.image_1.source = media_obj_1
      self.image_2.source = media_obj_2
      self.label_2.text = f'''Similarity Index: {"%.2f" %(anvil.server.call('get_score', self.link_1.text, 'anchors'))}'''

  def button_1_click(self, **event_args):
    """This method is called when transcribe button is pressed"""
    self.button_1.visible = False
    self.link_1.visible = False
    self.add_component(voice_rec_2(), full_width_row=True)
    time.sleep(3)
    if self.slow.selected:
      spaces = 0.75
    if self.medium.selected:
      spaces = 0.5
    if self.fast.selected:
      spaces = 0.15
    else:
      self.medium.selected = True
      spaces = 0.5
    self.label_5.visible, self.slow.visible, self.medium.visible, self.fast.visible = False, False, False, False
    self.label_1.visible = True

    """This method is called when the button is clicked"""
    text = self.text

    paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by two newlines


    # Stream each paragraph
    for paragraph in paragraphs:
      lines = paragraph.split('\n')
    
      for line in lines:
        words = line.split()
    
        for word in words:
          self.label_1.text += word + ' '
          time.sleep(spaces) # Freeze the browser tab for this duration
    
          # After all words in a line are added, append a newline
        self.label_1.text += '\n'
        time.sleep(spaces) # Freeze the browser tab again
    
        # Add an extra newline for paragraph spacing
      self.label_1.text += '\n'
    time.sleep(7)
    self.label_1.visible = False
    foo = self.call_js('getAllTexts1')
    self.call_js('stopRecognition1')
    anvil.server.call('similarity_index', 'anchors', self.link_1.text, self.label_1.text, foo)

    self.timer_1_tick()

  def share_click(self, **event_args):
    """This method is called when the link is clicked"""
    text = self.label_2.text.replace('Similarity Index: ', '')
    self.call_js("copyclip", f'''AnchorsLab
📽️📺
🟩🟩
⬛⬛ 
{text}
Can you beat my score?
Download & Play @ https://rb.gy/dfzb5p/#anchor'''
                )

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.timer_1.interval = 3
    try:
      if anvil.server.call('check_playtime', self.link_1.text) is self.today:
        self.timer_1.interval = 0
        open_form('anchorlabs.gameplay')
        # anvil.server.call('update_anchor', user['username'])
        # open_form('global_anchorslab')
        # else:
        #   open_form('gameplay')
    except Exception as e:
      print(e)
      pass

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('anchorlabs')
