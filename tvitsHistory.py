#===============================================================================
# http://stackoverflow.com/questions/28267640/tweepy-get-old-tweets-now-possible-with-twitter-search-api
# how to get old tweets 
#===============================================================================

from tweepy.models import Status
import tweepy
from pprint import pprint
import json

from mysqlUtilities import connectMySQL

db = connectMySQL(db='crolections', port=3366)

ckey = "YaV9e065RrS7GDG7ZPOeCHl3c"
csecret = "ttfJ3oaGuViY2QnrB4AjtY259ow5uDef5CiK0GMOTVQW1kNDyF"
atoken = "2926971581-qhxdUJThotm8Jpmy9Ks5P2XWivDcYSeCtvaDCpj"
asecret = "eLd0UWqoFt5riom4hzKukk1jVrpK6zFdm5dPLVSJnfnz9"

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)
query = '#izboriRH OR #izborirh OR #izbori2015 OR #izbori15'

nrItem = 1
for tvit in tweepy.Cursor(api.search, q=query).items():
    tagsUsed = u', '.join([item['text'] for item in tvit.entities['hashtags']])
    
    sqlQuery = '''
    INSERT INTO crolections.izbori2015
    (izbori2015_tweet_id,
    izbori2015_user,
    izbori2015_user_id,
    izbori2015_text,
    izbori2015_created_at,
    izbori2015_geo,
    izbori2015_hashtags,
    izbori2015_in_reply_to_screen_name,
    izbori2015_in_reply_to_status_id,
    izbori2015_in_reply_to_user_id,
    izbori2015_retweet_count,
    izbori2015_retweeted)
    VALUES
    ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');
    '''%(tvit.id,
         tvit.user.screen_name,
         tvit.user.id, 
         tvit.text, 
         tvit.created_at,
         tvit.geo, 
         tagsUsed,
         tvit.in_reply_to_screen_name, 
         tvit.in_reply_to_status_id, 
         tvit.in_reply_to_user_id, 
         tvit.retweet_count, 
         tvit.retweeted)
    print sqlQuery
    db.executeQuery(sqlQuery)
    db._connectMySQL__connection.commit()
    nrItem += 1
