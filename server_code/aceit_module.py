# import anvil.stripe
import anvil.tables as tables
# import anvil.email
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.media
import anvil.http
from anvil.server import http_endpoint, request
import random
from datetime import timedelta, date
import requests
import time


@anvil.server.callable
def get_name_amt(name):
  row = app_tables.users.get (username='ace_it')['user_words']
  return row[name][0]

@anvil.server.callable
def send_job_dets(user, title, comp_name):
  title = title.strip().title()
  try:
    user_folder = app_files.curated_q.get(title)
    if user_folder:
      for num in range(10):
        row = app_tables.curated_q.add_row(User=f'{user}')
        row['job_title'] = title
        row['Position'] = num
        row['question_list'] = app_tables.curated_q.search(User='admin')[0]['question_list'][title][num] #so fucking stupid logic
        
        row['recordings'] = user_folder.get(f'{num}.wav')
        
    else:
      row = app_tables.users.get (username='ace_it')
      nu_dict = row['Promote']
      if user in nu_dict.keys():
        jd = nu_dict[user]
      else:
        jd = ''
      resp = requests.post("https://mealy-expensive-bone.anvil.app/_/api/log_resp", json={'user': user,
              'title':title,'comp_name':comp_name, 'jd':jd})
      print(f"Request made. Status Code: {resp.status_code}") 
  except Exception as e:
    print(e)

@anvil.server.callable
def check_curated_status(user):
  return len({row for row in app_tables.curated_q.search(User=user)}) == 10

@anvil.server.callable
def get_sound(key, route):
  # if key[0] in ['intro', 'closing']:
  #   row = app_tables.questions.get (unique_key=key[0])
  #   return row['General'].get_url()
  # else:
  if route == 'curated':
    row = app_tables.curated_q.get (Position=key[0])
    return row['recordings'].get_url()    
  else:
    row = app_tables.questions.get (position=key[0])
    return row['recordings'].get_url()

@anvil.server.callable
def get_ai_questions(user):
  question_lookup = {row['Position']: row['question_list'] for row in app_tables.curated_q.search(User=user)}
  nu_list = []
  for _,num in question_lookup.items():
    nu_list.append((_,num))
  sorted_data = sorted(nu_list, key=get_sort_key)
  return sorted_data


def get_sort_key(item):
  value = item[0] # This gets the first element of the tuple
  return value

@anvil.server.callable
def get_questions():  # later pass interview type
  question_lookup = {row['position']: row['question_list'] for row in app_tables.questions.search()}

  random_items = [
    (0, question_lookup[0])  # Opening
  ] + random.sample(
    [(key, question_lookup[key]) for key in question_lookup if key in range(1, 10)], 
    3
  ) + random.sample(
    [(key, question_lookup[key]) for key in question_lookup if key in range(11, 31)], 
    3
  ) + random.sample(
    [(key, question_lookup[key]) for key in question_lookup if key > 30 and key != 100], 
    3
  ) + [
    ('closing', question_lookup[100])  # Closing
  ]

  return random_items


@anvil.server.http_endpoint('/getpdf', methods=["POST"], authenticate_users=False)
def get_pdf():
  pdf = anvil.server.request.body_json["pdf"]
  user = anvil.server.request.body_json["user"]
  row = app_tables.users.get (username='ace_it')
  nu_dict = row['avg']
  nu_dict[user] = pdf
  row['avg'] = nu_dict


@anvil.server.callable
def get_pdf_data(user):
  row = app_tables.users.get (username='ace_it')
  if user in row['avg'].keys():
    pdf_data = row['avg'][user] #encryption for pdf is whats one here
    nu_dict = row['avg']
    del nu_dict[user]
    row['avg'] = nu_dict
    return pdf_data
  else:
    return 'Try again'

@anvil.server.callable
def user_jd(item, user):
  row = app_tables.users.get (username='ace_it')
  #using promote column to conserve space
  nu_dict = row['Promote']
  nu_dict[user] = item
  row['Promote'] = nu_dict


@anvil.server.callable
def transcript_api(trans_dict, user):
  row = app_tables.users.get (username='ace_it')
  nu_dict = row['today_words']
  nu_dict[user] = trans_dict
  # create a row on a google sheet for the transcription. Transpose
  row['today_words'] = nu_dict

@anvil.server.http_endpoint('/get_user_tr', methods=["GET"], authenticate_users=False)
def get_user_transcript(username: str = None):
  row = app_tables.users.get (username='ace_it')
  nu_dict = row['today_words'] #if they use again, no logs
  if username in nu_dict.keys():
    transcript = nu_dict[username]
    del nu_dict[username]
    row['today_words'] = nu_dict
    return transcript
  else:
    get_user_transcript(username)


@anvil.server.callable
def add_to_wallet(user, value, task):
  row = app_tables.users.get (username='ace_it')
  nu_dict = row['user_words']
  if task == 'add':    
    nu_dict[user][0] += value
    row['user_words'] = nu_dict
  else:
    nu_dict[user][0] -= value
    row['user_words'] = nu_dict    


@anvil.server.background_task
def save_recordings_to_drive(user):
  # Get your Google Drive folder from App Files
  folder = app_files.curated_q
  pos = ''
  nu_list = []

  # Fetch rows from your curated_q data table
  rows = app_tables.curated_q.search(User=user)
  for row in rows:
    pos = row['job_title'] #lazy way to get the job title as opposed to passing it around in the client code
    break
  try:
    my_folder = folder.get(pos)
    if my_folder:
      pass #if there's already a folder for job title, pass
    else:
      folder.create_folder(pos) # else, create one
      time.sleep(5)
      user_folder = folder.get(pos)
      for row in rows:
        if row['recordings']:   # Assuming the column is named 'recording' and stores Media objects
          # Save recording into the Google Drive folder
          user_folder.create_file(f'{row["Position"]}.wav', row['recordings'])
          nu_list.append(row['question_list'])
          row.delete()
      row = app_tables.curated_q.search(User='admin')
      nu_dict = row[0]['question_list']
      nu_dict[pos] = nu_list
      row[0]['question_list'] = nu_dict
      
  except Exception as e:
    print(e)


  
@anvil.server.callable
def save_n_del(user):
  task = anvil.server.launch_background_task('save_recordings_to_drive', user)
  