from ._anvil_designer import Form3Template
from anvil import *
import anvil.server
import time
from datetime import date
from ..tips import tips
import re
from ..vidhtml import vidhtml


class Form3(Form3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.server.call_s('test_cookie')
    self.share.visible = False
    self.timer_1.interval = 0
    self.topic, self.transcript = anvil.server.call_s('get_topic_transcript', 'speecheazi')

    self.today = str(date.today())

    if anvil.server.call('check_playtime', self.user, 'speecheazi') is self.today:
      #if user has recorded...

      self.label_4.text, self.label_4.visible, self.link_2.visible= self.topic, True, False
      self.generate.visible, self.share.visible = False, True
      self.image_1.visible = True
      self.label_5.font_size = 30
      self.label_5.text = f'''Rating: {"%.2f" %(anvil.server.call('get_score', self.user))}'''


  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(tips(), large= True)

  def generate_click(self, **event_args):
    """This method is called when transcribe button is pressed"""
    self.generate.visible = False
    self.label_4.visible = True
    self.label_4.text, self.link_2.visible = self.topic, True
    #alert function here
    for num in range(11, 5, -1):
      time.sleep(1)
      self.label_2.text = f'You have {str(num)} seconds to prep'

    for num in range(5, -1, -1):
      time.sleep(1)
      self.label_2.text = f'Begin your speech in {str(num)} seconds'
    # self.call_js('beep')
    self.image_1.visible, self.card_6.visible  = False, True
    self.call_js('startRecognition')
    self.label_2.text = 'Begin!!!'
    time.sleep(1)
    for num in range(121, -1, -1):
      time.sleep(1)
      self.label_2.text = f'{str(num)} seconds remaining in your speech'

    self.recording_1_button_click()

  def recording_1_button_click(self, **event_args):
    """This method is called when clicked in gameplay"""
    user_words = self.call_js('getAllTexts')
    print(user_words)
    self.call_js('stopRecognition')
    user_words = re.sub(r'''[?\'"-]''', '', user_words)
    user_words = ','.join(word for word in user_words.split())
    foo = self.transcript
    foo = re.sub(r'''[?\'"-]''', '', foo)
    foo = ','.join(word for word in foo.split())
    url = f'''https://speakeasi.streamlit.app/?embedded=true&bar=speak&user={self.user}&user_words={user_words}&foo={foo}'''
    # print(url)
    time.sleep(3)
    self.content_panel.add_component(vidhtml(url))
    self.card_6.visible = False
    self.label_2.visible = False
    #some code here to alert the backend that recording is done
    self.image_1.visible= True
    self.label_5.visible  = True
    self.label_5.text = 'Processing!!!'
    self.timer_1_tick()


  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.timer_1.interval = 10
    try:
      if anvil.server.call('check_playtime', self.user) is self.today:
        self.timer_1.interval = 0
        open_form('gameplay')
        # else:
        #   open_form('gameplay')
    except Exception as e:
      print(e)
      pass


  def share_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.call_js("copyclip", f'''SpeechEazi
🗣️💬
⬛⬛ 
{self.label_5.text}
Can you beat my score?
Become a better public speaker @ https://rb.gy/dfzb5p/#speak'''
                )


  def stop_rec_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.recording_1_button_click()
    # Any code you write here will run before the form opens.
