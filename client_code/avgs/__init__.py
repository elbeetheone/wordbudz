from ._anvil_designer import avgsTemplate
from anvil import *
import anvil.server
from .. import GlobalState


class avgs(avgsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    data = GlobalState.get_user_info()

    self.label_5.text = data['user']
    user_data_list = data['user_data']

    if user_data_list: # Check if list is NOT empty
      try:
        last_entry = user_data_list[-1]
        self.avg.text = "%.2f" % (last_entry.get('avg_score', 0))
        self.played.text = last_entry.get('Played_time', 0)
        self.today.text = "%.2f" % (last_entry.get('current_score', 0))
      except (TypeError, KeyError, IndexError):
        self.set_default_display()
    else:
      self.avg.text = "0.00"
      self.played.text = "0"
      self.today.text = "0.00"
      Notification('Your averages will be displayed here once you begin playing', timeout=3).show()




    

