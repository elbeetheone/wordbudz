from ._anvil_designer import ace_itTemplate
from anvil import *
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import time
from datetime import date
from .text_area import text_area



class ace_it(ace_itTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.route = get_url_hash()
    user = anvil.server.call("test_cookie")
    self.line = anvil.server.call("get_name_amt", user)
    self.name.text, self.amount.text = user, f"Wallet Amount: ${self.line:,.2f}"
    self.timer_1.interval = 0

  # def error_handler(err):
  #   open_form('error')

  # set_default_error_handling(error_handler)

  def back_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.line >= 1.99:
      anvil.server.call('add_to_wallet', self.name.text, 1.99, 'not_add')
      open_form("ace_it.begin", 'gameplay')
    else:
      try:
        c = stripe.checkout.charge(amount=199, currency='USD',
                                  icon_url="_/theme/-high-resolution-logo-transparent.png")
        if c['result'] == 'succeeded':

          open_form('ace_it.begin', 'gameplay')
      except Exception as e:
        alert(e)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(text_area(), large=True)

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('home')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.job_title.text != '' and self.comp_name.text != '':
      if self.line >= 3.99:
        # minus from amount on record
        anvil.server.call('send_job_dets', self.name.text, self.job_title.text, self.comp_name.text)
        anvil.server.call('add_to_wallet', self.name.text, 3.99, 'not_add')
        self.timer_1_tick()
      else:
        try:
          c = stripe.checkout.charge(amount=399, currency='USD',
                                    icon_url="_/theme/-high-resolution-logo-transparent.png")
          if c['result'] == 'succeeded':
            anvil.server.call('send_job_dets', self.name.text, self.job_title.text, self.comp_name.text)
            self.timer_1_tick()
        except Exception as e:
          alert(e)

  def wallet_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.wallet_add_pressed_enter()

  def wallet_add_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    try:
      amount = float(self.wallet_add.text)
      c = stripe.checkout.charge(amount=amount*100, currency='USD',
                                 icon_url="_/theme/-high-resolution-logo-transparent.png")
      if c['result'] == 'succeeded' and self.wallet_add.text not in [0, None]:
        anvil.server.call('add_to_wallet', self.name.text, self.wallet_add.text, 'add')
        time.sleep(3)
        open_form('ace_it')

    except Exception as e:
      alert(e)

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.timer_1.interval = 1
    try:
      result = anvil.server.call('check_curated_status', self.name.text)
      if result:
        self.timer_1.interval = 0
        open_form('ace_it.begin', 'curated')

    except Exception as e:
      print(e)
        

def error_handler(err):
  try:
    open_form("error")
  except ("NotAllowedError", "NotSupportedError"):
    pass


set_default_error_handling(error_handler)
