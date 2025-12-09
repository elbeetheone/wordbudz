from ._anvil_designer import avgsTemplate
from anvil import *
import anvil.server


class avgs(avgsTemplate):
  def __init__(self, route,**properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_5.text = anvil.server.call_s('test_cookie')
    dict = anvil.server.call('get_avgs', route, self.label_5.text)
    self.avg.text = "%.2f" %(dict[-1]['avg_score'])
    self.played.text = dict[-1]['Played_time']
    self.today.text = "%.2f" %(dict[-1]['current_score'])






    

