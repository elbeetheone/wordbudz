import anvil.stripe
# import anvil.email
# # import anvil.google.auth, anvil.google.drive, anvil.google.mail
# from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import timedelta, date

@anvil.server.http_endpoint('/paste_budz', methods=["POST"], authenticate_users=False)
def paste_budz():
  league = anvil.server.request.body_json["league"]
  user_words = anvil.server.request.body_json["user_words"]
  print(league)
  row = app_tables.users.get(username=league)
  row['today_words'] = user_words
  print('200 OK')


@anvil.server.callable
def join_league(league, user):
  row = app_tables.users.get (username=league)
  row['players'] += 1
  nu_dict = row['user_words']
  nu_dict[user] = [{"avg_score": 0,"Played_time": 0,"total_score": 0}]
  row['user_words'] = nu_dict
  return 'reload'

@anvil.server.callable
def check_league(user):
    results = app_tables.users.search(q.any_of(username=q.ilike('%League')))
    for row in results:
        if user in row['user_words'].keys():
            return row['name']

    return 'proceed'


@anvil.server.callable
def check_closed_league(user):
    results = app_tables.users.search(q.any_of(username=q.any_of(
            q.ilike('%0%'),
            q.ilike('%1%'),
            q.ilike('%2%'),
            q.ilike('%3%'),
            q.ilike('%4%'),
            q.ilike('%5%'),
            q.ilike('%6%'),
            q.ilike('%7%'),
            q.ilike('%8%'),
            q.ilike('%9%')
        )))
    for row in results:
        if user in row['user_words'].keys():
            return row['name'], row['username']

    return 'proceed'
  


@anvil.server.callable
def join_closed(id, user):
    row = app_tables.users.get (username=id)
    if row is not None:
        join_league(id, user)
        return row['username']
    else:
        return 'User not found'

@anvil.server.callable
def league_name(league):
  row = app_tables.users.get (username=league)
  return row['name'], row['username'], str(row['finishes'])

@anvil.server.callable
def add_league(user, name, code, date, admin):
  app_tables.users.add_row(name=name,
                          username=code,
                          finishes=date,
                          today_words=[],
                          user_words={},
                          ranked_table=[],
                          admin = admin,
                          players=0)
  join_league(code, user)
  
@anvil.server.callable
def check_league_create(league, foo):
  row = app_tables.users.get (username=league)
  if len(row['today_words']) == int(foo): #length of league words and user length provided are same
    return 'proceed'

@anvil.server.callable
def order_fill(user, item, id):
  row = app_tables.users.get(username='admin')
  nu_dict = row['merch']

  # Determine color based on item description
  if 'Black' in item:
    color_key = 'black'
  elif 'White' in item:
    color_key = 'white'
  else:
    color_key = 'white'  # Default fallback

  if user not in row['merch'].keys():
    nu_dict[user] = [{
      'item_description': item,
      'status': 'Added to Cart',
      'price': row['Prices'][color_key],
      'trans_id': id,
      'num_item': 1,
      'date': str(date.today())
    }]
    row['merch'] = nu_dict
  elif user in row['merch'].keys():
    nu_dict[user].append({
      'item_description': item,
      'status': 'Added to Cart',
      'price': row['Prices'][color_key],
      'trans_id': id,
      'num_item': 1,
      'date': str(date.today())
    })
    row['merch'] = nu_dict



@anvil.server.background_task
def promotion_n_relegation():
  results = app_tables.users.search(q.any_of(username=q.ilike('%League')))
  def promote_and_relegate(league):
      # Sort users by score in descending order
      row = app_tables.users.get (username=league)
      users = row['ranked_table']
      users_sorted = sorted(users, key=lambda x: x['score'], reverse=True)
      # Calculate the number of users to promote and relegate
      num_users = len(users_sorted)
      top_1_percent_count = max(1, int(num_users * 0.01))  # At least one user
      bottom_1_percent_count = max(1, int(num_users * 0.01))  # At least one user  
      # Get the top 1% and bottom 1%
      top_1_percent = users_sorted[:top_1_percent_count]
      bottom_1_percent = users_sorted[-bottom_1_percent_count:] 
      # Remove promoted and relegated users from the original list
      remaining_users = [user for user in users_sorted if user not in top_1_percent and user not in bottom_1_percent]
      row['Promote'], row['Relegate'], row['user_words'] = transform_data(top_1_percent), transform_data(bottom_1_percent), transform_data(remaining_users)
      row['ranked_table'] = []
  for _ in results:
    promote_and_relegate(_['username'])
  append_rel_pro()


def transform_data(data):
  result = {}
  for item in data:
    user = item['user']
    if user not in result:
      result[user] = []
    result[user].append({
      "avg_score": 0,
      "Played_time": 0,
      "total_score": 0
    })
  return result

def append_rel_pro():
    results = app_tables.users.search(q.any_of(username=q.ilike('%League')))
    def update_user_words(num, target_tier, transfer_key):
        target_row = app_tables.users.get (tier=target_tier)
        if target_row is None:
            nu_dict = num['user_words']
            for item in num[transfer_key]:
                nu_dict[item] = num[transfer_key][item]
            num['user_words'] = nu_dict
            return        
        if num[transfer_key] is None:
            return
        if not target_row['user_words']:
            target_row['user_words'] = num[transfer_key]
        else:
            nu_dict = target_row['user_words']
            for item in num[transfer_key]:
                nu_dict[item] = num[transfer_key][item]
            target_row['user_words'] = nu_dict
    # Promotion
    for num in results:
        update_user_words(num, num['tier'] - 1, 'Promote')
    # Relegation
    for num in results:
        update_user_words(num, num['tier'] + 1, 'Relegate')
    for num in results:
      num['players'] = len(num['user_words'])
      num['finishes'] = date.today() + timedelta(days=6)
      num['Promote'], num['Relegate'] = {}, {}

def item_global():
  row = app_tables.users.get (username='admin')
  return row['merch']

@anvil.server.callable
def item_info(user, stat):
  row = app_tables.users.get(username='admin')
  if user in row['merch'].keys():
    # Filter items with "Added to Cart" status
    if stat == 'cart':
      cart_items = [item for item in row['merch'][user] if item.get('status') == 'Added to Cart']
      return cart_items
    else:
      cart_items = [item for item in row['merch'][user]]
      return cart_items
  else:
    return None
  

@anvil.server.callable
def trash_item(user, id):
  row = app_tables.users.get (username='admin')
  nu_dict = row['merch']
  for num in nu_dict[user][:]:  # Iterate over a shallow copy of the list
      if num['trans_id'] == id:
          nu_dict[user].remove(num)
  if len(nu_dict[user]) == 0:
    del nu_dict[user] 
  row['merch'] = nu_dict


@anvil.server.callable
def add_minus_item(user, id, func):
  row = app_tables.users.get(username='admin')
  nu_dict = row['merch']

  if func == 'add':
    for num in nu_dict[user]:
      if num['trans_id'] == id:
        num['num_item'] += 1
        break  # Exit loop once found

  elif func == 'minus':
    for num in nu_dict[user][:]:  # Shallow copy needed here for removal
      if num['trans_id'] == id:
        num['num_item'] -= 1
        if num['num_item'] == 0:
          nu_dict[user].remove(num)
        break

  elif func == 'charge':
  # Update ALL items with "Added to Cart" status to "Paid"
    for num in nu_dict[user]:
      if num.get('status') == 'Added to Cart':  
        num['status'] = 'Paid'  
    # OR if you only want to update one specific item:
    # for num in nu_dict[user]:
    #   if num['trans_id'] == id:
    #     num['Status'] = 'Paid'
    #     break

  # Clean up empty user entries
  if user in nu_dict and len(nu_dict[user]) == 0:
    del nu_dict[user]

  row['merch'] = nu_dict
    

@anvil.server.callable
def get_price():
  row = app_tables.users.get(username='admin')
  return row['Prices']
  
  

@anvil.server.callable
def admin(league):
  row = app_tables.users.get (username=league)
  return row['admin']
  
@anvil.server.callable
def get_addy():
  return anvil.server.cookies.local.get('address', '')

@anvil.server.callable
def store_addy(user, addy, country):
  anvil.server.cookies.local.set(100, address=addy)
  row = app_tables.users.get (username='admin')
  nu_dict = row['merch']
  for num in nu_dict[user][:]:
    num['address'] = addy+ ' '+ country
  row['merch'] = nu_dict


@anvil.server.wellknown_endpoint("/assetlinks.json")
def assetlinks():
  return [{
      "relation": ["delegate_permission/common.handle_all_urls"],
      "target": {
        "namespace": "android_app",
        "package_name": "app.admin.wordbudz.twa",
        "sha256_cert_fingerprints": ["46:8F:67:57:97:86:BF:37:F8:2F:C5:6D:C3:D8:DC:EF:10:61:6D:1F:92:12:C6:1E:72:F6:2B:6B:B1:37:10:72"]
      }
    }]

