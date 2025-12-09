from ._anvil_designer import reports_pageTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import base64
import time
from ..vidhtml import vidhtml

class reports_page(reports_pageTemplate):
  def __init__(self, user, answers, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.answers = ' '.join(answers.values())
    self.user = user
    url = f"""https://speakeasi.streamlit.app/?embedded=true&bar=aceit&user={user}""" #send for report
    self.add_component(vidhtml(url))
    self.timer_1.interval = 5
    media_obj_1 = anvil.server.call('get_wordcloud', self.answers)
    self.image_1.source = media_obj_1
    test = self.answers.lower()
    like = test.count('like')
    uh = test.count('uh')
    um = test.count('um')
    self.plot_1.data = [
      go.Bar(
        x=['like', 'uh', 'um'],
        y=[like, uh, um],
        name='Filler Words Count'
      )
    ]
    
    
    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('ace_it')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""

    base64_str = anvil.server.call('get_pdf_data', self.user)
    if not base64_str or base64_str == 'Try again':
      self.timer_1.interval = 5
      self.timer_1_tick()
      return

    file_bytes = base64.b64decode(base64_str)
    blob = anvil.js.window.Blob([file_bytes], { "type": "application/pdf" })
    url = anvil.js.window.URL.createObjectURL(blob)

    link = anvil.js.window.document.createElement("a")
    link.href = url
    link.download = f"{self.user}_report.pdf"
    link.click()

    anvil.js.window.URL.revokeObjectURL(url)

    

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.timer_1.interval = 0
    self.button_1_click()
