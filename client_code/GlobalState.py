import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import date


_cached_data = {}

def get_user_info():
  today = date.today()

  if _cached_data.get('date') == today and _cached_data.get('user') not in [None, 'not found']:
    return _cached_data

  attempts = 0
  max_attempts = 3

  while attempts < max_attempts:
    try:
      results = anvil.server.call('test_cookie')
      user_val = results[0]

      if user_val != 'not found':
        _cached_data.update({
          'user': user_val,
          'ratings': results[1] or [],
          'words': results[2],
          'user_data': results[3] or [],
          'date': today
        })
        return _cached_data

        # If user_val is 'not found', we don't need to retry
      break

    except Exception as e:
      attempts += 1
      print(f"Attempt {attempts} failed: {e}")
      if attempts < max_attempts:
        import time
        time.sleep(1)  # Brief pause before retrying
      else:
        print("Max attempts reached for test_cookie.")

    # Fallback if loop finishes without returning or finding a user
  _cached_data['user'] = 'not found'
  return _cached_data

def update_cache(username, user_data=None):
  """Call this after registration to seed the cache immediately."""
  _cached_data.update({
    'user': username,
    'user_data': user_data,
    'date': date.today()
  })
