from ._anvil_designer import league_playTemplate
from anvil import *
import anvil.server
from datetime import date
from ..vidhtml import vidhtml



class league_play(league_playTemplate):
  def __init__(self, league, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.timer_1.interval = 0
    self.link_1.text = anvil.server.call('test_cookie')
    self.league = league
    self.league_title = anvil.server.call('league_name', league)
    self.label_1.text, self.label_2.text = self.league_title[0], self.league_title[-1]
    anvil.server.call('league_control', self.link_1.text, league)
    self.rank.text = f"Rank: {anvil.server.call('get_rank_pos', league, self.link_1.text, 'daily')}"
    self.repeating_panel_1.items = anvil.server.call_s('get_rank', league, 'daily')
    if str(date.today()) == self.label_2.text:
      self.play.visible = False
      alert('The league has officially concluded. Kindly view your rank and points below!', large=True)
    # Any code you write here will run before the form opens.

  def play_click(self, **event_args):
    """This method is called when the button is clicked"""
    #if player game times and length of games are same. alert
    if anvil.server.call('league_len', self.link_1.text, self.league) == 'alert':
      alert('Seems you have played the maximum games available. Please wait for the league to finish')
    elif anvil.server.call('league_len', self.link_1.text, self.league) == 'new':
      self.label_1.text, self.label_1.background = '🤔 First one here, please hold while we build the new league', '#FF0000'
      url = f'''https://speakeasi.streamlit.app/?embedded=true&bar=paste&route={self.league}&foo=100'''
      #just made it fully automatic. This way first user to sign in will trigger word list creation
      self.card_1.add_component(vidhtml(url))
      self.timer_1_tick()
    else:
      open_form('wordbudz.global_wordbuds_league', self.league_title)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('wordbudz')

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    self.timer_1.interval = 10
    try:
      if anvil.server.call('check_league_create', self.league, 100) == 'proceed':
        self.timer_1.interval = 0
        open_form('wordbudz.global_wordbuds_league', self.league_title)
        # else:
        #   open_form('gameplay')
    except Exception as e:
      print(e)
      pass
