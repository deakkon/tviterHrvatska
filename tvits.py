from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from pprint import pprint
from mysqlUtilities import connectMySQL

#tags = ['izboriRH','izboriHR','izbori2015','izbori']
tags = ['izboriRH']

import sqlite3
conn = sqlite3.connect('dummyFile.sqlite')
c = conn.cursor()

#consumer key, consumer secret, access token, access secret.
ckey = "YaV9e065RrS7GDG7ZPOeCHl3c"
csecret = "ttfJ3oaGuViY2QnrB4AjtY259ow5uDef5CiK0GMOTVQW1kNDyF"
atoken = "2926971581-qhxdUJThotm8Jpmy9Ks5P2XWivDcYSeCtvaDCpj"
asecret = "eLd0UWqoFt5riom4hzKukk1jVrpK6zFdm5dPLVSJnfnz9"


class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        pprint(all_data)
        #=======================================================================
        # for item in all_data:
        #=======================================================================
        print all_data['user']
        print all_data['user']['description']
        print all_data["user"]['screen_name']
        print all_data['text']
        print all_data['entities']['hashtags'][0]['text']
        print '-----------'
        return True

    def on_error(self, status):
        print status
        
        

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=['izboriRH','izboriHR','izbori2015','politikahr'])