from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from mysqlUtilities import connectMySQL
from pprint import pprint
import time
import traceback

#tags = ['izboriRH','izboriHR','izbori2015','izbori']
tags = ['izboriRH']

from mysqlUtilities import connectMySQL
db = connectMySQL(db='crolections', port=3366)

#consumer key, consumer secret, access token, access secret.
ckey = "YaV9e065RrS7GDG7ZPOeCHl3c"
csecret = "ttfJ3oaGuViY2QnrB4AjtY259ow5uDef5CiK0GMOTVQW1kNDyF"
atoken = "2926971581-qhxdUJThotm8Jpmy9Ks5P2XWivDcYSeCtvaDCpj"
asecret = "eLd0UWqoFt5riom4hzKukk1jVrpK6zFdm5dPLVSJnfnz9"


class listener(StreamListener):

    def on_data(self, data):
        
        try:
            
            all_data = json.loads(data)
            #===================================================================
            # pprint(all_data)
            #===================================================================
            tagsUsed = ', '.join([item['text'] for item in all_data['entities']['hashtags']])
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(all_data['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            URLs = ', '.join([item['url'] for item in all_data['entities']['urls']])
            
            
            #=======================================================================
            # if type(all_data['in_reply_to_user_id']) == None else in_reply_to_user_id = all_data['in_reply_to_user_id']
            #=======================================================================
            if all_data['in_reply_to_user_id'] is None:
                in_reply_to_user_id = 0
            else:
                in_reply_to_user_id = all_data['in_reply_to_user_id']
                
            if all_data['in_reply_to_status_id'] is None:
                in_reply_to_status_id = 0
            else:
                in_reply_to_status_id = all_data['in_reply_to_status_id']

            if all_data['place'] is None:
                geo = all_data['place']
            else:
                geo = all_data['place']['full_name']
            
            #===================================================================
            # print '1\t',all_data['text']
            #===================================================================
            text = all_data['text'].replace('"',"'")
            #===================================================================
            # print '2\t',text
            #===================================================================
            
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
            '''%(all_data['id'],
                 all_data['user']['screen_name'],
                 all_data['user']['id'], 
                 text, 
                 ts,
                 geo, 
                 tagsUsed,
                 all_data['in_reply_to_screen_name'], 
                 in_reply_to_status_id, 
                 in_reply_to_user_id, 
                 all_data['retweet_count'], 
                 all_data['retweeted'],
                 URLs)
            #=======================================================================
            # print sqlQuery
            #=======================================================================
            db.executeQuery(sqlQuery)
            db._connectMySQL__connection.commit()
            
            print 'ID\t', all_data['id']
            print 'SN\t', all_data['user']['screen_name']
            print 'UID\t', all_data['user']['id']
            print 'TXT\t', text
            print 'Time\t', ts
            print 'GEO\t', geo
            print 'TAG\t', tagsUsed
            print 'Reply1\t', all_data['in_reply_to_screen_name']
            print 'Reply2\t', in_reply_to_status_id
            print 'Reply3\t', in_reply_to_user_id
            print 'ReTweet\t', all_data['retweet_count']
            print 'Retweeted\t', all_data['retweeted']
            print 'URLs\t', URLs
            print '--------------'
            
            
        except (AttributeError,TypeError):
            traceback.print_exc()
            pass
        except:
            traceback.print_exc()
            pass
            
        return True
            

    def on_error(self, status):
        print status
        
        

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=['izboriRH','izboriHR','izbori2015','politikahr'])
