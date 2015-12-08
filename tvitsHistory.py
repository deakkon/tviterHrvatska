#===============================================================================
# http://stackoverflow.com/questions/28267640/tweepy-get-old-tweets-now-possible-with-twitter-search-api
# how to get old tweets 
#===============================================================================

from tweepy.models import Status
import tweepy
from pprint import pprint
import json
import time
from mysqlUtilities import connectMySQL

db = connectMySQL(db='crolections', port=3366)

ckey = "YaV9e065RrS7GDG7ZPOeCHl3c"
csecret = "ttfJ3oaGuViY2QnrB4AjtY259ow5uDef5CiK0GMOTVQW1kNDyF"
atoken = "2926971581-qhxdUJThotm8Jpmy9Ks5P2XWivDcYSeCtvaDCpj"
asecret = "eLd0UWqoFt5riom4hzKukk1jVrpK6zFdm5dPLVSJnfnz9"

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)
query = '#izboriRH OR #izborirh OR #izbori2015 OR #izbori15 OR #politikahr'


for all_data in tweepy.Cursor(api.search, q=query).items():
     
    sqlExists = 'select count(*) from izbori2015 where izbori2015_tweet_id = %d'%(all_data.id)
    db.executeQuery(sqlExists)
    #===========================================================================
    # print sqlExists
    #===========================================================================
    #===========================================================================
    # print '1',db._connectMySQL__results[0][0]
    #===========================================================================
    
    if db._connectMySQL__results[0][0] == 0:
        
        tagsUsed = ', '.join([item['text'] for item in all_data.entities['hashtags']])
        ts = all_data.created_at
        URLs = ', '.join([item['url'] for item in all_data.entities['urls']])

        text = all_data.text.replace('"',"'")
        
        if all_data.place is None:
            geo = all_data.place
        else:
            geo = all_data.place.full_name
        
        #===================================================================
        # print '1\t',all_data['text']
        #===================================================================
        text = all_data.text.replace('"',"'")
        
        if all_data.in_reply_to_user_id is None:
            in_reply_to_user_id = 0
        else:
            in_reply_to_user_id = all_data.in_reply_to_user_id
         
        if all_data.in_reply_to_status_id is None:
            in_reply_to_status_id = 0
        else:
            in_reply_to_status_id = all_data.in_reply_to_status_id
     
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
        izbori2015_retweeted,
        izbori2015_URLs)
        VALUES
        (%d,'%s',%d,"%s",'%s','%s','%s','%s', %d, %d, %d, %s,'%s');
        '''%(all_data.id,
         all_data.user.screen_name,
         all_data.user.id, 
         text, 
         ts,
         geo, 
         tagsUsed,
         all_data.in_reply_to_screen_name, 
         in_reply_to_status_id, 
         in_reply_to_user_id, 
         all_data.retweet_count, 
         all_data.retweeted,
         URLs)
        db.executeQuery(sqlQuery)
        db._connectMySQL__connection.commit()
        print 'New'
    else:
        print "Update"
        if all_data.place is None:
            geo = all_data.place
        else:
            geo = all_data.place.full_name
            
        sqlUpdate = 'update izbori2015 set izbori2015_geo = "%s" where izbori2015_tweet_id = %d'%(geo, all_data.id)
        db.executeQuery(sqlUpdate)
        db._connectMySQL__connection.commit()
    
    #===========================================================================
    # print all_data.id,'\n',all_data.user.screen_name,'\n',all_data.user.id,'\n', all_data.text,'\n', ts,'\n',all_data.geo,'\n', tagsUsed,'\n',all_data.in_reply_to_screen_name,'\n', in_reply_to_status_id,'\n', in_reply_to_user_id,'\n', all_data.retweet_count,'\n', all_data.retweeted,'\n',URLs
    #===========================================================================
