import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.users
import anvil.media
import random
import requests
from datetime import timedelta, date

@anvil.server.callable
def get_wordcloud(text):
  resp = requests.post("https://mealy-expensive-bone.anvil.app/_/api/anchors_simi", json={'user_dets': text})
  image_bytes = resp.content
  return anvil.BlobMedia("image/png", image_bytes, name="word_cloud.png")

@anvil.server.callable
def get_user_anc(user):
  row = app_tables.users.get(username='anchors')
  text = row['user_words'][user][0]['text']
  return text

@anvil.server.callable
def user_media():
  row = app_tables.users.get(username='anchors')
  return row['anc_media']


def get_user_row(route):
  # username = 'admin' if route == 'unlimited' else 'daily'
  return app_tables.users.get(username=route)

@anvil.server.callable
def get_story():
  row = app_tables.users.get(username='anchors')
  return row['today_words'][0]

@anvil.server.callable
def check_your_speech(user):
  row = app_tables.users.get(username='your_speech')
  nu_dict = row['user_words']
  if user in nu_dict.keys():
    score = nu_dict[user][-1].get('current_score', 0)
    del nu_dict[user]
    return True, score
  else:
    return False
    

@anvil.server.callable
def similarity_index(route, user, passage1, passage2):
  # Convert passages to lowercase and split into words
  row = app_tables.users.get(username=route)
  if user in row['user_words'].keys():
    Played_time = row['user_words'][user][0].get('Played_time', 0) 
    avg_score = row['user_words'][user][0].get('avg_score', 0) 
    total_score = row['user_words'][user][0].get('total_score', 0) 
  else:
    Played_time = 0
    avg_score = 0
    total_score = 0
  nu_list = [{'text': passage2}]
  words1 = set(passage1.lower().split())
  words2 = set(passage2.lower().split())

  # Count the total words in passage1 and common words in both passages
  total_words = len(words1)
  common_words = words1.intersection(words2)

  # Calculate similarity index
  similarity = len(common_words) / total_words
  nu_list.append({"Played_time": Played_time+1, 'current_score': similarity, "total_score": total_score + similarity,
                  "avg_score": calculate_new_average(similarity, avg_score, Played_time), 'last_played': str(date.today())})
  nu_dict = row['user_words']
  nu_dict[user] = nu_list
  row['user_words'] = nu_dict
  print('200 OK')
  task = anvil.server.launch_background_task('attach_pos', route, user)
  return similarity

def calculate_new_average(current_score, average_rating, no_of_times_played):
  new_average_rating = ((average_rating * no_of_times_played) + current_score) / (no_of_times_played + 1)
  return new_average_rating




# @anvil.server.background_task
# def anchor_cancel():
#   row = app_tables.users.get (username='anchor')
#   row['ranked_table'] = []
#   nu_list = row['story']
#   nu_list.pop(0)
#   row['story'] = nu_list
#   text = nu_list[0]
#   stopwords= set(STOPWORDS)
#   new_words = []
#   new_stopwords=stopwords.union(new_words)
#   plt.rcParams["figure.figsize"] = (15,15)
#   wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white",stopwords=new_stopwords, colormap='flag').generate(text)
#   plt.plot()
#   plt.imshow(wordcloud, interpolation="bilinear")
#   plt.axis("off")
#   row['anc_media'] = anvil.mpl_util.plot_image()


