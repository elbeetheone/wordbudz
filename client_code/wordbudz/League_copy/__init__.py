from ._anvil_designer import League_copyTemplate
from anvil import *
import anvil.server
import anvil.js


class League_copy(League_copyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.server.call_s("test_cookie")
    self.closer = anvil.server.call_s("check_closed_league", self.user)
    self.admin = anvil.server.call('admin', self.closer[-1])
    if self.closer != "proceed":
      self.open.font_size, self.closed.font_size = 10, 18
      (
        self.card_6.visible
      ) = True
      self.label_closed.text = self.closer[0]
      if self.admin == self.user:
        self.card_7.visible = True
    else:
      self.open.font_size, self.closed.font_size = 10, 18

    # Any code you write here will run before the form opens.


  def closed_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.closer = anvil.server.call_s("check_closed_league", self.user)
    if self.closer != "proceed":
      self.open.font_size, self.closed.font_size = 10, 18
      (
        self.card_6.visible
      ) = True
      self.label_closed.text = self.closer[0]
      if self.admin == self.user:
        self.card_7.visible = True
    else:
      self.open.font_size, self.closed.font_size = 10, 18

  def open_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('wordbudz.League')


  def home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("wordbudz")


  def submit_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.label_3.text == anvil.server.call(
      "join_closed", self.label_3.text, self.user
    ):
      # reload page instead?
      open_form("wordbudz.league_play", self.label_3.text)
    else:
      self.label_3.text = ""
      alert("Please check the code and retry")


  def league_continue_closed_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("wordbudz.league_play", self.closer[-1])

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.js.call_js("copyclip", f'''
Hi there,

I'd love for you to join my WordBudz league, {self.label_closed.text}! Simply use the code {self.closer[-1]} to join the fun.

You can download the app here and join directly.

Looking forward to competing with you there!
    '''
                      )


