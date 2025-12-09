from ._anvil_designer import anchor_infoTemplate
from anvil import *
import anvil.server
import anvil.js.window as window

SpeechRecognition = window.get("SpeechRecognition") or window.get(
  "webkitSpeechRecognition"
)
SpeechGrammarList = window.get("SpeechGrammarList") or window.get(
  "webkitSpeechGrammarList"
)
recognition = SpeechRecognition()

class anchor_info(anchor_infoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    recognition = SpeechRecognition()
    recognition.continuous = False
    recognition.lang = "en-US"
    recognition.interimResults = False
    recognition.maxAlternatives = 1

    def on_result(event):
      transcribed_text = event.results[0][0].transcript
      if 'hello' in transcribed_text.lower():
        self.speak.foreground = 'theme:Primary 700'
        self.speak.text = f"👍 You said '{transcribed_text.capitalize()}', you're good to go"
      else:
        self.test.visible = True
        self.speak.text = "Try Again, Say 'Hello'"

    def on_speech_end(e):
      recognition.stop()

    def on_no_match(e):
      self.test.visible = True
      self.speak.text = "Try Again, Say 'Hello'"


    recognition.onresult = on_result
    recognition.onspeechend = on_speech_end
    recognition.onnomatch = on_no_match
    self.recognition = recognition

  def test_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.test.visible = False
    self.recognition.start()
    self.speak.visible = True