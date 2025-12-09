from ._anvil_designer import global_wordbuds_leagueTemplate
from anvil import *
import anvil.server
import time
import anvil.js.window as window
from ..Word_info import Word_info
from ..vidhtml import vidhtml


SpeechRecognition = window.get("SpeechRecognition") or window.get(
  "webkitSpeechRecognition"
)
SpeechGrammarList = window.get("SpeechGrammarList") or window.get(
  "webkitSpeechGrammarList"
)


class global_wordbuds_league(global_wordbuds_leagueTemplate):
  def __init__(self, league, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.server.call('test_cookie')
    self.timer_1.interval, self.timer_2.interval = 0, 0
    self.league = league
    self.route, self.link_1.text = self.league[1], self.league[0] #route has _ key
    self.ratings = anvil.server.call_s("test_ratings", self.route)
    self.stage = self.ratings[0]["Played_time"]
    # print(self.stage)
    # print(anvil.server.call_s("check_playtime_league", self.user, self.route))


    if self.stage == anvil.server.call_s("check_playtime_league", self.user, self.route):
      self.user_words = anvil.server.call_s("get_words", self.route)[
        self.stage
        ]  # change to 0 in the future
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

    if self.stage != anvil.server.call_s("check_playtime_league", self.user, self.route):
      # important logic. If stage and played time are different, show the below vars
      self.stage_button.visible = True
      self.repeating_panel.items = anvil.server.call_s(
        "check_words", self.user, self.route
      )
      self.record.visible, self.countdown.visible, self.card_1_copy.visible = (
        False,
        False,
        True,
      )
      self.total.text = "%.2f" % (
        sum([item["scores"] for item in self.repeating_panel.items if "scores" in item])
      )

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
      url = f"""https://speakeasi.streamlit.app/?embedded=true&bar=budz&route={self.route}&user={self.user}&foo={self.foo}&user_words={the_words}"""
      self.card_1.add_component(vidhtml(url))
      self.timer_2_tick()

  def wordbud_info_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(Word_info(), large=True)

  def share_click(self, **event_args):
    """This method is called when the link is clicked"""
    glo_score = [item["scores"] for item in self.repeating_panel.items]
    self.call_js(
      "copyclip",
      f"""WordBudz
⬛🟦 {"%.2f" %(glo_score[0])}
⬛🟦 {"%.2f" %(glo_score[1])}
⬛🟦 {"%.2f" %(glo_score[2])}
⬛🟦 {"%.2f" %(glo_score[3])}
⬛🟦 {"%.2f" %(glo_score[4])}
🟥🟥 {"%.2f" %(sum(glo_score))}
Can you beat my score?
Download & Play @ https://rb.gy/dfzb5p/#word""",
    )

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.timer_1.interval = 1
    self.instruct.visible = True
    try:
      if self.stage == anvil.server.call("check_playtime_league", self.user, self.route):
        # important logic. If stage & played time are same then update page
        self.timer_1.interval = 0
        time.sleep(3)
        open_form("wordbudz.global_wordbuds_league", self.league)
      # else:
      #   self.timer_1_tick()
    except Exception as e:
      pass

  def stage_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if anvil.server.call('league_len', self.user, self.route) == 'alert':
      alert('Seems you have played the maximum games available. Please wait for the league to finish')
      open_form('wordbudz.league_play', self.route)
    else:
      anvil.server.call("next_stage", self.user, self.ratings, self.route)
      self.stage_button.visible = False
      self.stage += 1
      self.timer_1_tick()

  def timer_2_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.timer_2.interval = 1

    try:
      if self.stage != anvil.server.call("check_playtime_league", self.user, self.route):
        self.timer_2.interval = 0
        open_form("wordbudz.global_wordbuds_league", self.league)
        # else:
        #   open_form('gameplay')
    except Exception as e:
      pass

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('wordbudz.league_play', self.route)
