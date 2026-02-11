from ._anvil_designer import closed_league_subTemplate
from anvil import *
import anvil.server
import stripe.checkout
import random
from ..vidhtml import vidhtml
from ..prices import prices




class closed_league_sub(closed_league_subTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.server.call_s("test_cookie")
    self.closer = anvil.server.call_s("check_closed_league", self.user)

    if self.closer != "proceed":
      open_form('wordbudz.League_copy')
    else:
      self.code.text = ''.join([random.choice('1234567890') for _ in range(6)])
      self.timer_1.interval = 0

    # Any code you write here will run before the form opens.

  def submit_click(self, **event_args):
    """This method is called when the button is clicked"""
    #alert to payment page. Pass No. of games * 9.99/30
    self.league_home.visible = False
    if self.name.text is None or self.games.text is None or self.date.date is None:
      self.league_home.visible = True
      alert('Please fill in the required fields.')
    else:
      # alert(stripe_payment(self.games.text), large=True)
      amount = self.games.text * (3.99/30)
      try:
        c = stripe.checkout.charge(currency="USD", amount=amount*100,
                                   icon_url="_/theme/download.png")
        if c['result'] == 'succeeded':
          self.create_game()
      except Exception as e:
        alert(e)
      


  def create_game(self, **event_args):
    user = anvil.server.call_s('test_cookie')
    url = f'''https://speakeasi.streamlit.app/?embedded=true&bar=paste&route={self.code.text}&foo={self.games.text}'''
    self.card_1.add_component(vidhtml(url))
    #api create list of provided league length
    anvil.server.call('add_league', user, self.name.text, self.code.text, self.date.date, anvil.server.call_s('test_cookie'))
    self.timer_1_tick()
    

  def games_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.games.text is not None:
      self.games.text = int(str(self.games.text).replace('.',''))
    if self.games.text is not None and self.games.text > 1000:
      self.games.text = 1000

      

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    
    self.timer_1.interval = 5
    self.label_1.visible = True
    try:
      if anvil.server.call('check_league_create', self.code.text, self.games.text) == 'proceed':
        self.timer_1.interval = 0
        open_form('wordbudz.League_copy')
        # else:
        #   open_form('gameplay')
    except Exception as e:
      print(e)
      pass

  def guide_payment_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(prices(), large=True)

  def home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('wordbudz')
