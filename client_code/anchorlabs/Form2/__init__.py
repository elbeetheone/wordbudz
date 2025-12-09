from ._anvil_designer import Form2Template
from anvil import *
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go
import time
from ..voice_rec_2 import voice_rec_2
from datetime import date



class Form2(Form2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.user = anvil.server.call_s('test_cookie')
    self.timer_1.interval = 0
    self.foo = None


    #means user has played today


  def button_1_click(self, **event_args):
    """This method is called when transcribe button is pressed"""
    self.card_1.visible = False
    # self.link_1.visible = False
    self.call_js('startRecognition')
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
    text = self.text_area_1.text

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
    foo = self.call_js('getAllTexts')
    self.foo = foo
    self.call_js('stopRecognition')
    anvil.server.call('similarity_index', 'your_speech',self.user, self.label_1.text, foo)

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
      check_speech = anvil.server.call('check_your_speech', self.user)
      if check_speech[0]:
        self.timer_1.interval = 0
        self.button_1.visible = False
        self.label_5.visible, self.slow.visible, self.medium.visible, self.fast.visible = False, False, False, False
        media_obj_1 = anvil.server.call('get_wordcloud', self.text_area_1.text)
        media_obj_2 = anvil.server.call('get_wordcloud', self.foo)
        self.index.visible = True
        self.image_1.source = media_obj_1
        self.image_2.source = media_obj_2
        self.label_2.text = f'''Similarity Index: {"%.2f" %(check_speech[-1])}'''
    except Exception as e:
      print(e)
      pass

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('anchorlabs')

    # Any code you write here will run before the form opens.
