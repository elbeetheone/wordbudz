import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from datetime import date
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Module1
#
#    Module1.say_hello()
#


_cached_data = {}

def get_user_info():
  today = date.today()


  if _cached_data.get('date') == today and _cached_data.get('user') not in [None, 'not found']:
    return _cached_data

  try:
    results = anvil.server.call('test_cookie')
    user_val = results[0]

    if user_val != 'not found':
      _cached_data.update({
        'user': user_val,
        'ratings': results[1] or [],  # Default to empty list
        'words': results[2],
        'user_data': results[3] or [],  # Default 
        'date': today
      })
      return _cached_data

  except anvil.server.AnvilError as e:
    print(f"Server call failed: {e}")
  except Exception as e:
    print(f"Unexpected client error: {e}")

    # Fallback for any failure path
  _cached_data['user'] = 'not found'
  return _cached_data

def update_cache(username, user_data=None):
  """Call this after registration to seed the cache immediately."""
  _cached_data.update({
    'user': username,
    'user_data': user_data,
    'date': date.today()
  })
