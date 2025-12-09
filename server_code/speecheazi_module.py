# import anvil.stripe
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


@anvil.server.http_endpoint('/savescore', methods=["POST"], authenticate_users=False)
def savescore():
  score = anvil.server.request.body_json["score"]
  user = anvil.server.request.body_json["user"]
  row = app_tables.users.get(username='admin')
  score = float(score.strip('"')) * 10

  if user in row['user_words'].keys():
    Played_time = row['user_words'][user][-1].get('Played_time', 0) 
    avg_score = row['user_words'][user][-1].get('avg_score', 0) 
    total_score = row['user_words'][user][-1].get('total_score', 0) 
  else:
    Played_time = 0
    avg_score = 0
    total_score = 0
  nu_list = []
  nu_list.append({"Played_time": Played_time+1, 'current_score': score, "total_score": total_score + score,
                  "avg_score": calculate_new_average(score, avg_score, Played_time), 'last_played': str(date.today())})

  nu_dict = row['user_words']
  nu_dict[user] = nu_list
  row['user_words'] = nu_dict
  task = anvil.server.launch_background_task('attach_pos', user)
  print('200 OK')

def calculate_new_average(current_score, average_rating, no_of_times_played):
  new_average_rating = ((average_rating * no_of_times_played) + current_score) / (no_of_times_played + 1)
  return new_average_rating


@anvil.server.callable
def get_score(user, route):
  row = app_tables.users.get(username=route)
  return row['user_words'][user][-1].get('current_score')


@anvil.server.callable
def get_topic_transcript(route):
  row = app_tables.users.get(username=route)
  input_string = row['today_words'][0][0]
  colon_index = input_string.find(':')
  if colon_index != -1:
    topic = input_string[:colon_index]
    transcript = input_string[colon_index:].replace(':','')
    return topic, transcript


# @anvil.server.background_task
# def attach_pos(user):
#   row = app_tables.users.get(username='admin')
#   data = row['user_words']   
#   score_key = 'avg_score'
#   sorted_users = sorted(
#     [(u, d) for u, d in data.items() if d[-1].get('last_played') == str(date.today())],
#     key=lambda x: x[1][-1][score_key],
#     reverse=True)
#   # Step 2: Assign ranks
#   ranked_list = []
#   for rank, (user, details) in enumerate(sorted_users, start=1):
#     total_score = details[-1][score_key]
#     played_time = details[-1]["Played_time"]
#     ranked_list.append({'user': user, 'score': total_score, 'rank': rank, 'played_time':played_time})   
#     row['ranked_table'] = ranked_list

@anvil.server.background_task
def speech_cancel():
  row = app_tables.users.get (username='speecheazi')
  # row['ranked_table'] = []
  nu_list = row['today_words']
  nu_list.pop(0)
  row['today_words'] = nu_list