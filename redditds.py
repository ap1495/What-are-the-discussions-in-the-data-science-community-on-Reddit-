# -*- coding: utf-8 -*-
"""
Created on Tue Sep 03 11:34:51 2019

@author: Abhishek
"""

from psaw import PushshiftAPI

api = PushshiftAPI()
import datetime as dt
import pandas as pd

#The date upto which posts are going to be scraped starting from date of running this script.
start_epoch=int(dt.datetime(2017, 8, 31).timestamp())

new_subreddit=api.search_submissions(after=start_epoch,
                            subreddit='datascience', #Subreddit 
                            limit=10000000)


topics_dict = { 'title':[], 'author':[], 'score':[], 'id':[], 'url':[], 'comms_num':[], 'created': [], 'body':[]}

for submission in new_subreddit:
    topics_dict['title'].append(submission.title)
    topics_dict['author'].append(submission.author)
    topics_dict['score'].append(submission.score)
    topics_dict['id'].append(submission.id)
    topics_dict['url'].append(submission.url)
    topics_dict['comms_num'].append(submission.num_comments)
    topics_dict['created'].append(submission.created)
    
    try:
        topics_dict['body'].append(submission.selftext)
    except:
        topics_dict['body'].append("N/A")
    
    
topics_data = pd.DataFrame(topics_dict)

#Converting date & time of posts to human readable form. 
def get_date(created):
    return dt.datetime.fromtimestamp(created)

timestamp = topics_data['created'].apply(get_date)
topics_data = topics_data.assign(timestamp = timestamp)

#Writing dataframe to a .csv file.
topics_data.to_csv('datascience2.csv', index=False) 

#Getting the comments of posts.
gen = api.search_comments(after=start_epoch,subreddit='datascience',filter=['url','author', 'topic','id','title','score','body'])
comms_dict = { 'body':[], 'created':[], 'score':[], 'author':[], 'id':[] }
for top_level_comment in gen:
        comms_dict['author'].append(top_level_comment.author)
        comms_dict['body'].append(top_level_comment.body)
        comms_dict['id'].append(top_level_comment.id)
        comms_dict['created'].append(top_level_comment.created)
        comms_dict['score'].append(top_level_comment.score)
        
comms_data = pd.DataFrame(comms_dict)

#Converting date & time of posts to human readable form. 
timestamps = comms_data['created'].apply(get_date)
comms_data = comms_data.assign(timestamp = timestamps)

#Writing dataframe to a .csv file.
comms_data.to_csv('datasciencecomments2.csv', index=False)   
