from ._anvil_designer import global_wordbudsTemplate
from anvil import *
import anvil.server
import time
import anvil.js.window as window
from ..vidhtml import vidhtml
from datetime import datetime, timezone


SpeechRecognition = window.get("SpeechRecognition") or window.get(
  "webkitSpeechRecognition"
)
SpeechGrammarList = window.get("SpeechGrammarList") or window.get(
  "webkitSpeechGrammarList"
)



class global_wordbuds(global_wordbudsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.link_1.text = anvil.server.call_s("test_cookie")
    self.timer_2.interval = 0

    self.stage = str(datetime.now(timezone.utc))[:10] #universal time across zones

    if self.stage != anvil.server.call_s("check_playtime", self.link_1.text, 'word'):
      print('here')
      #if today's date is not the last played date, upload new game
      self.user_words = anvil.server.call_s("get_words", 'word')[0]
      self.foo = ", ".join(self.user_words).replace(" ", "")
      self.messages = []
      self.repeating_panel.items = self.messages
      recognition = SpeechRecognition()
      recognition.continuous = False
      recognition.lang = "en-US"
      recognition.interimResults = False
      recognition.maxAlternatives = 1

      def on_result(event):
        transcribed_text = event.results[0][0].transcript
        self.messages[-1]["synonym"] = transcribed_text.capitalize()
        self.repeating_panel.items = self.messages

      def on_speech_end(e):
        recognition.stop()
        self.record.icon = "fa:microphone"
        self.record.enabled = True

      def on_no_match(e):
        self.messages[-1]["synonym"] = ""
        self.repeating_panel.items = self.messages

      recognition.onresult = on_result
      recognition.onspeechend = on_speech_end
      recognition.onnomatch = on_no_match
      self.recognition = recognition


    if self.stage == anvil.server.call_s("check_playtime", self.link_1.text, 'word'):
      # important logic. If today's date and last played are the same, show below
      self.repeating_panel.items = anvil.server.call_s("check_words", self.link_1.text, 'word')
      self.record.visible, self.countdown.visible, self.card_1_copy.visible = False,False,True
      self.total.text = "%.2f" % (sum([item["scores"] for item in self.repeating_panel.items if "scores" in item]))

  def record_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.recognition.stop()
    self.record.visible, self.link_1.visible = False, False
    self.countdown.text = ""
    self.countdown.visible = True
    self.messages.append({"word": self.user_words[0].capitalize(), "synonym": ""})
    self.repeating_panel.items = self.messages
    self.user_words.pop(0)
    for num in range(5, 0, -1):
      self.countdown.text = str(num)
      time.sleep(1)

    self.recognition.start()
    self.countdown.text = "Speak"
    self.record.icon = "fa:stop"
    self.record.enabled = False
    time.sleep(5)

    if len(self.user_words) != 0:
      self.record_click()
    else:
      self.countdown.text = "Processing"
      self.messages = [
        {**item, "synonym": "_" if item["synonym"] in ["", " "] else item['synonym'].replace('.','')}
        for item in self.messages
      ]
      the_words = ", ".join([item["synonym"] for item in self.messages]).replace(
        " ", ""
      )
      try:
        anvil.server.call('seenonym', self.link_1.text, the_words, self.foo, 'word')
      except Exception as e:
        print(e)
        self.fallback_streamlit(self.link_1.text, self.foo, the_words)

      self.timer_2_tick()

      

  def fallback_streamlit(self, user, foo, words):
    url = (
      "https://speakeasi.streamlit.app/?embedded=true"
      f"&bar=budz&route=word&user={user}&foo={foo}&user_words={words}"
    )
    self.card_1.add_component(vidhtml(url))

  def share_click(self, **event_args):
    """This method is called when the link is clicked"""
    glo_score = [item["scores"] for item in self.repeating_panel.items]
    self.call_js("copyclip", f'''WordBudz
⬛🟦 {"%.2f" %(glo_score[0])}
⬛🟦 {"%.2f" %(glo_score[1])}
⬛🟦 {"%.2f" %(glo_score[2])}
⬛🟦 {"%.2f" %(glo_score[3])}
⬛🟦 {"%.2f" %(glo_score[4])}
____________
🟥🟥 {"%.2f" %(sum(glo_score))}
____________
Can you beat my score?
Download & Play @ https://rb.gy/api4sx'''
                )


  def timer_2_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.timer_2.interval = 1

    try:
      if self.stage == anvil.server.call("check_playtime", self.link_1.text, 'word'):
        self.timer_2.interval = 0
        anvil.server.call('next_stage', self.link_1.text, [{"Avg_rating": 0,"Played_time": 0}], 'word')
        open_form("wordbudz.global_wordbuds")
        # else:
        #   open_form('gameplay')
    except Exception as e:
      print(e)
      pass

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('wordbudz')

