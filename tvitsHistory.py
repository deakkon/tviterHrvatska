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
    print tvit.id
    print tvit.text
    print tvit.user.screen_name
    print tvit.created_at
    print tvit.in_reply_to_status_id
    print tvit.coordinates
    print tvit.in_reply_to_screen_name
    print tvit.geo
    print type(tvit)
    print nrItem, '--------'
    sqlQuery = '''
    INSERT INTO crolections.izbori2015
    (izbori2015TvitID,
    izbori2015Autor,
    izbori2015Text,
    izbori2015TvitTime,
    izbori2015Geo,
    izbori2015Rted,
    izbori2015Answer2)
    VALUES
    (
    '%s',
    '%s',
    '%s',
    '%s',
    '%s',
    '%s',
    '%s');
    '''%(tvit.id,tvit.user.screen_name, tvit.text, tvit.created_at,tvit.geo, tvit.retweeted,tvit.in_reply_to_status_id)
    print sqlQuery
    db.executeQuery(sqlQuery)
    db._connectMySQL__connection.commit()
    nrItem += 1


#===============================================================================
# ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__getstate__', 
# '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
# '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_api', '_json', 'author', 'contributors', 'coordinates', 
# 'created_at', 'destroy', 'entities', 'favorite', 'favorite_count', 'favorited', 'geo', 'id', 'id_str', 
# 'in_reply_to_screen_name', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 
# 'in_reply_to_user_id_str', 'is_quote_status', 'lang', 'metadata', 'parse', 'parse_list', 'place', 
# 'possibly_sensitive', 'retweet', 'retweet_count', 'retweeted', 'retweeted_status', 'retweets', 
# 'source', 'source_url', 'text', 'truncated', 'user']
#===============================================================================