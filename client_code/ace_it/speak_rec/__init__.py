from ._anvil_designer import speak_recTemplate
from anvil import *
import anvil.server
import anvil.users
import time
import re


class speak_rec(speak_recTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.server.call_s('test_cookie')
    self.questions = anvil.server.call('get_questions')
    print(self.questions)
    self.timer_1.interval = 0.005
    self.answers = {value[0]: None for key, value in self.questions[:-1]}
    self.control = 10 #lazy way to control get all texts
    self.ans_loc = None

    # Any code you write here will run before the form opens.


  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.timer_1.interval = 0
    self.button_2_click()


  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event('button_click')
    self.call_js('startRecognition')
    # self.button_1.enabled = False
    self.button_2.enabled = True
    self.button_1.enabled = False
    if len(self.questions) == 1:
      self.button_2.text = 'Generate Report'

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event('button_click')
    if self.button_2.text == 'Generate Report':
      first_item = list(self.answers.items())[self.ans_loc]
      self.answers[first_item[0]] = self.call_js('getAllTexts')
      anvil.server.call_s('transcript_api',self.answers, self.user)
      # url = f"""https://speakeasi.streamlit.app/?embedded=true&bar=aceit&user={self.user}""" #send for report
      # print(url)
      # self.card_1.add_component(vidhtml(url))
      self.button_1.enabled, self.button_2.enabled = False, False
      url = anvil.server.call_s('get_sound', self.questions[0], 'no') #closing speech
      self.call_js('loadClip', url)
      open_form('ace_it.reports_page', self.user, self.answers)

    else:
      self.button_2.enabled = False
      self.button_1.enabled = False
      url = anvil.server.call_s('get_sound', self.questions[0], 'no')
      self.call_js('loadClip', url)
      time.sleep(self.questions[0][-1][-1])
      if self.control != 10: #button_2_click is called when page loads
        first_item = list(self.answers.items())[self.ans_loc]
        self.answers[first_item[0]] = self.call_js('getAllTexts')
        self.questions = self.questions[1:]
        self.button_1.enabled = True
        self.control -= 1
        self.ans_loc += 1

      else:
        self.questions = self.questions[1:]
        self.button_1.enabled = True
        self.control -= 1
        self.ans_loc = 0




