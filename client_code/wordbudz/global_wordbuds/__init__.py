from ._anvil_designer import global_wordbudsTemplate
from anvil import *
import anvil.server
import time
import anvil.js.window as window
from ..vidhtml import vidhtml
from datetime import datetime, timezone
from ... import GlobalState


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
    data = GlobalState.get_user_info()
    self.link_1.text = data['user']
    self.data = data['user_data']
    self.words = data['words'] or []
    self.timer_2.interval = 0

    self.stage = str(datetime.now(timezone.utc))[:10] #universal time across zones

    if self.stage != self.check_playtime():
      #if today's date is not the last played date, upload new game
      self.user_words = self.words
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


    else:
      self.fail_safe()

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
    self.countdown.text = "Speak 💬"
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
        self.fallback_streamlit(self.username, self.foo, the_words)
      except Exception as e:
        print(e)
        anvil.server.call('seenonym', self.username, the_words, self.foo, 'word')

      self.timer_2_tick()

      

  def fallback_streamlit(self, user, foo, words):
    url = (
      f"https://speakeasi.streamlit.app/?embedded=true&bar=budz&route=word&user={user}&foo={foo}&user_words={words}"
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
______
🟥🟥 {"%.2f" %(sum(glo_score))}
Can you beat my score?
Download & Play @ https://rb.gy/api4sx'''
                )


  def timer_2_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.timer_2.interval = 3

    try:
      playtime, last_item = anvil.server.call("check_playtime", self.username, 'word')
      if self.stage == playtime:
        self.timer_2.interval = 0
        GlobalState.update_cache(username=self.username, user_data=last_item)
        open_form("wordbudz.global_wordbuds")
        # else:
        #   open_form('gameplay')
    except Exception as e:
      print(e)
      pass

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('wordbudz')

  def check_playtime(self):
    user_words = self.data

    # Loop backwards through the list to find the first dictionary with last_played
    for item in reversed(user_words):
      if isinstance(item, dict) and "last_played" in item:
        return item["last_played"]

    return 0  # Return 0 if no valid last_played found



  def check_words(self):
    words = self.data.copy()
    words.pop(-1)
    return words

  def fail_safe(self):
    items = self.check_words()
    self.repeating_panel.items = items
    self.record.visible, self.countdown.visible, self.card_1_copy.visible = False, False, True
    # Calculate total from the cached items
    self.total.text = "%.2f" % (sum([item["scores"] for item in items if "scores" in item]))
    return