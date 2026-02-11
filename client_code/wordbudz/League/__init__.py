from ._anvil_designer import LeagueTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.js



class League(LeagueTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.server.call_s('test_cookie')
    self.league = anvil.server.call('check_league', self.user)
    self.closed_click()
    
    # if self.league != 'proceed':
      
    #   self.card_5.visible, self.card_1.visible, self.label_5.text = True, False, self.league

    # self.nu_dict = {'Odin League': '1st Tier',
    #                 'Apollo League': '2nd Tier',
    #                 'Ra League': '3rd Tier',
    #                 'Xango League': '4th Tier',
    #                 'Shiva League': '5th Tier',
    #                 'Hera League': '6th Tier',
    #                 'Hades League': '7th Tier',
    #                 'Anubis League': '8th Tier',
    #                 'Osiris League': '9th Tier',
    #                 'Vulcan League': '10th Tier'}

    # if len(self.label_5.text) > 1:
    #   self.label_6.text = self.nu_dict[self.label_5.text] #arbitrary code, probably better ways to logicalize this
    # self.repeating_panel_1.items = anvil.server.call('get_league')
    # self.data_grid_1.rows_per_page = 10
    # self.open.font_size, self.closed.font_size = 18, 10

    # Any code you write here will run before the form opens.

  def zero_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.text = self.label_3.text + '0'

  def one_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.text = self.label_3.text + '1'

  def two_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.text = self.label_3.text + '2'

  def three_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.text = self.label_3.text + '3'

  def four_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.text = self.label_3.text + '4'

  def five_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.text = self.label_3.text + '5'

  def six_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.text = self.label_3.text + '6'

  def seven_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.text = self.label_3.text + '7'

  def eight_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.text = self.label_3.text + '8'

  def nine_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.text = self.label_3.text + '9'

  def back_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.label_3.text = self.label_3.text[:-1]

  def closed_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.closer = anvil.server.call_s('check_closed_league', self.user)
    if self.closer != 'proceed':
      self.open.font_size, self.closed.font_size = 10, 18
      self.card_6.visible, self.card_1.visible, self.card_2.visible, self.card_5.visible = True, False, False, False
      self.label_closed.text = self.closer[0]
      admin = anvil.server.call('admin', self.closer[-1])
      if admin == self.user:
        self.card_7.visible = True
    else:      
      self.card_5.visible = False
      self.card_1.visible, self.card_2.visible = False, True
      self.open.font_size, self.closed.font_size = 10, 18


  def open_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.league != 'proceed':
      self.card_5.visible, self.card_1.visible, self.label_5.text = True, False, self.league
      self.card_2.visible, self.card_6.visible = False, False
      self.open.font_size, self.closed.font_size = 18, 10
    else:
      self.card_6.visible = False
      self.card_2.visible, self.card_1.visible = False, True
      self.open.font_size, self.closed.font_size = 18, 10

  def home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('wordbudz')

  def league_continue_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('wordbudz.league_play', self.label_5.text.replace(' ','_')) #at some point, u gats do what u gats do

  def submit_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.label_3.text == anvil.server.call('join_closed', self.label_3.text, self.user):
      #reload page instead?
      open_form('wordbudz.league_play',self.label_3.text)
    else:
      self.label_3.text = ''
      alert('Please check the code and retry')

  def new_closed_league_click(self, **event_args):
    """This method is called when the button is clicked"""
    # c = stripe.checkout.charge(currency="USD", amount=100)
    open_form('wordbudz.closed_league_sub')
    #for now, will redirect to payment page

  def league_continue_closed_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('wordbudz.league_play', self.closer[-1])

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.js.call_js("copyclip", f'''
Hi there,

I'd love for you to join my WordBudz league, {self.label_closed.text}! Simply use the code {self.closer[-1]} to join the fun.

You can download the app here and join directly.

Looking forward to competing with you there!
    '''
                      )

      
