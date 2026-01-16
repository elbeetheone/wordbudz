from ._anvil_designer import usernameTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from ..wordbudz import wordbudz


class username(usernameTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load = anvil.server.call('test_cookie')
    if self.load != 'not found':
      self.clear()
      self.add_component(wordbudz(), full_width_row=True)


    # Any code you write here will run before the form opens.

  def submit_click(self, **event_args):
    """This method is called when the button is clicked"""
    username = self.username.text
    email = self.email.text
    ans = anvil.server.call('generate_username', username, email)
    try:
      if ans != 'void':
        open_form('wordbudz')
      if ans == 'void':
        n = Notification("Please choose another username!")
        n.show()
    except Exception as e:
      print(e)
      open_form('username')

  def username_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def email_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.submit_click()

