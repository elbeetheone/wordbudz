
import anvil.tables as tables
# import anvil.email
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.users
import anvil.media
import anvil.http
from anvil.server import http_endpoint, request
import random
from datetime import timedelta, date
from anvil.google.drive import app_files


@anvil.server.http_endpoint('/budzscore', methods=["POST"], authenticate_users=False)
def budzscore():
  words = anvil.server.request.body_json["today_words"]
  score = [float(item.strip('"')) for item in words]
  user = anvil.server.request.body_json["user"]
  route = anvil.server.request.body_json["route"]
  row = app_tables.users.get (username=route)
  foo = anvil.server.request.body_json["foo"].split(',')
  user_words = anvil.server.request.body_json["user_words"].split(',')
  
  if user in row['user_words']:
    last_item = row['user_words'][user][-1]
    if isinstance(last_item, dict):
      Played_time = last_item.get('Played_time', 0)
      avg_score = last_item.get('avg_score', 0)
      total_score = last_item.get('total_score', 0)
    else:
      Played_time = avg_score = total_score = 0
  else:
    Played_time = avg_score = total_score = 0
  nu_list = []
  for num in range(5):
    nu_list.append({'word':foo[num], 'scores': score[num], 'synonym': user_words[num]})
  current_score = sum([item["scores"] for item in nu_list])
  nu_list.append({"Played_time": Played_time+1, 'current_score': current_score, "total_score": total_score + current_score,
                  "avg_score": calculate_new_average(current_score, avg_score, Played_time), 'last_played': str(date.today())})
  nu_dict = row['user_words']
  nu_dict[user] = nu_list
  row['user_words'] = nu_dict

  print('200 OK')
  task = anvil.server.launch_background_task('attach_pos', route, user)
  
def calculate_new_average(current_score, average_rating, no_of_times_played):
    new_average_rating = ((average_rating * no_of_times_played) + current_score) / (no_of_times_played + 1)
    return new_average_rating

@anvil.server.callable
def get_words(route):
  row = get_user_row(route)
  return row['today_words']

@anvil.server.callable
def get_avgs(route, user):
  row = get_user_row(route)
  if user in row['user_words'].keys():
    return row['user_words'][user]
  else:
    return [1,2,3,4,5,{'avg_score': 0, 'Played_time': 0, 'current_score': 0}]

@anvil.server.callable
def check_playtime(user, route):
  row = get_user_row(route)
  user_words = row['user_words'].get(user, [])

  # Loop backwards through the list to find the first dictionary with last_played
  for item in reversed(user_words):
    if isinstance(item, dict) and "last_played" in item:
      return item["last_played"]

  return 0  # Return 0 if no valid last_played found

@anvil.server.callable
def check_playtime_league(user, route):
  row = get_user_row(route)
  user_words = row['user_words'].get(user, [])
  if user_words:  # Check if the list is not empty
    return user_words[-1].get("Played_time", 0)
    return 0  # Return 0 if the list is empty or user not found

@anvil.server.callable
def len_league(route):
  row = get_user_row(route)
  # print(len(row['today_words']))
  return len(row['today_words'])

#Deleted daily stage. Will create scheduled task to delete daily rank and words
@anvil.server.background_task
def daily_cancel():
  row = app_tables.users.get (username='word')
  row['ranked_table'] = []
  nu_list = row['today_words']
  nu_list.pop(0)
  row['today_words'] = nu_list

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
  for _ in results:
    if _['finishes'] == date.today() - timedelta(days=1):
      db = app_files.team_info
      ws = db["Sheet1"] #keeping infromation of the leagues on a spread sheet incase info is needed
      row = ws.add_row(Admin=_['admin'], Rankings=_['ranked_table'])
      _.delete()
      
  results = app_tables.users.search(q.any_of(username=q.ilike('%League')))
  for _ in results:
    if _['finishes'] == date.today() - timedelta(days=1):
      #a day after league ends, clear so that a user can trigger new words
      _['today_words'] = []
      

@anvil.server.callable
def check_words(user, route):
  row = get_user_row(route)
  if user in row['user_words'].keys():
    words = row['user_words'][user]
    words.pop(-1)
    return words

@anvil.server.callable
def next_stage(user, ratings, route):  
    #code to update cookies played time in user's browser
    row = get_user_row(route)
    
    Played_time = row['user_words'][user][-1]['Played_time']
    avg_score = row['user_words'][user][-1]['avg_score']
    
    nu_dict = ratings
    nu_dict[0]['Played_time'] = Played_time
    nu_dict[0]['Avg_rating'] = avg_score
    
    cookie_key = 'ratings' if route == 'admin' else f'{route}_ratings'
    anvil.server.cookies.local.set(100, **{cookie_key: nu_dict})

@anvil.server.callable
def generate_username(username, email):
    row = app_tables.users.get (username='word')
    if any(char in username for char in '#$&@-*%$!+=') or len(username) < 4 or '@' not in email:
      return 'void'
    if username in row['user_words'].keys():
      return 'void'
    else:
      anvil.server.cookies.local.set(300, name=username, ratings=[{"Avg_rating": 0,"Played_time": 0}], daily_ratings=[{"Avg_rating": 0,"Played_time": 0}],
                                     anchor_ratings =[{"Avg_rating": 0,"Played_time": 0}], speecheazi_ratings=[{"Avg_rating": 0,"Played_time": 0}])

    nu_dict = row['user_words']
    nu_dict[username] = [0, email]
    row['user_words'] = nu_dict    

@anvil.server.callable
def test_cookie():
  return anvil.server.cookies.local.get('name', 'not found')
  # return anvil.server.cookies.local.get('310312_ratings')

@anvil.server.callable
def test_ratings(route):
  if route == 'daily':
    return anvil.server.cookies.local.get('daily_ratings', 'not found')
  elif route == 'admin':
    return anvil.server.cookies.local.get('ratings', 'not found')
  else:
    if anvil.server.cookies.local.get(f'{route}_ratings') is None:
      key = f'{route}_ratings'
      anvil.server.cookies.local.set(100, **{key: [{"Avg_rating": 0, "Played_time": 0}]})
      return anvil.server.cookies.local.get(f'{route}_ratings', 'not found')
    else:
      return anvil.server.cookies.local.get(f'{route}_ratings', 'not found')


@anvil.server.background_task
def attach_pos(route, user):
  row = get_user_row(route)
  data = row['user_words']

  def rank_users(score_key, extra_fields=None):
    if score_key == 'current_score':
      sorted_users = sorted(
        [(u, d) for u, d in data.items() if isinstance(d, list) and len(d) > 2 and isinstance(d[-1], dict) and d[-1].get('last_played') == str(date.today())],
        key=lambda x: x[1][-1][score_key],
        reverse=True
      )
    else:
      sorted_users = sorted(
        [(u, d) for u, d in data.items() if isinstance(d, list) and len(d) > 2 and isinstance(d[-1], dict) and d[-1].get('Played_time', 0) != 0],
        key=lambda x: x[1][-1][score_key],
        reverse=True
      )

    ranked = []
    for rank, (u, details) in enumerate(sorted_users, start=1):
      entry = {
        'user': u,
        'score': details[-1][score_key],
        'rank': rank
      }
      if extra_fields:
        for field in extra_fields:
          entry[field] = details[-1].get(field)
      ranked.append(entry)
    return ranked

  if 'league' in route.lower() or route.isdigit():
    row['ranked_table'] = rank_users('total_score', extra_fields=['Played_time'])
  else:
    row['ranked_table'] = rank_users('current_score', extra_fields=['Played_time'])
    row['avg'] = rank_users('avg_score')


    
@anvil.server.callable
def get_rank(route, when):
  row = get_user_row(route)

  if when == 'daily':
    return row['ranked_table']
  else:
    return row['avg']

@anvil.server.callable
def get_rank_pos(route, user, when):
  row = get_user_row(route)

  key = 'ranked_table' if when == 'daily' else 'avg'
  for entry in row[key]:
    if entry['user'] == user:
      return entry['rank']

  return 0



def get_user_row(route):
    # username = 'admin' if route == 'unlimited' else 'daily'
    return app_tables.users.get (username=route)

@anvil.server.callable
def get_league():
    results = app_tables.users.search(q.any_of(name=q.ilike('%League')))
    # filtered_results = [row for row in results if row['Signed'] < row['Max']]
    return results


@anvil.server.callable
def league_control(user, route):
  row = get_user_row(route)
  if row['user_words'][user][-1].get('Played_time') == 0:
    #essentially, this is for when a new league starts. To update their cookies played time to 0
    cookie_key = f'{route}_ratings'
    anvil.server.cookies.local.set(100, **{cookie_key: [{"Avg_rating": 0,"Played_time": 0}]})
  
@anvil.server.callable
def league_len(user, route):
  row = get_user_row(route)
  if len(row['today_words']) == 0:
    return 'new'
  if row['user_words'][user][-1].get('Played_time') == len(row['today_words']):
    #essentially for controlling for when user has played maximum amount of games on the backend
    return 'alert'

@anvil.server.callable  
def message(user, name, email, message):
  row= get_user_row('admin')
  text = row['name']
  text = f'{user} {name} {email} \n{message}'
  row['name'] = text