from ._anvil_designer import usernameTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from ..home import home


class username(usernameTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load = anvil.server.call('test_cookie')
    if self.load != 'not found':
      self.clear()
      self.add_component(home(), full_width_row=True)


    # Any code you write here will run before the form opens.

  def submit_click(self, **event_args):
    """This method is called when the button is clicked"""
    username = self.username.text
    email = self.email.text
    ans = anvil.server.call('generate_username', username, email)
    if ans != 'void':
      open_form('home')
    if ans == 'void':
      n = Notification("Please choose another username!")
      n.show()

  def username_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def email_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.submit_click()

