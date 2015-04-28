__author__ = 'erkrenz'

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from pprint import pprint
import sys
import MySQLdb
import uuid

#Variables that contains the user credentials to access Twitter API
access_token = "2260829143-4hASsCa1kdKsVxqThkByldtxyfjcNtrCJmsafLe"
access_token_secret = "zCLtyYG8qNQkuxZrYxxHgmiwBjG0yUOCkdGFdczx3AebA"
consumer_key = "7R0mWOj81T37Ef15RXyhNXel3"
consumer_secret = "UaVi2YfeWYxOL7olex33qIM3r6yAJgxUvcCgoemcsInsMC8Gv7"

keywords = [
    'rain',
    'snow',
    'sleet',
    'hail',
    'winter',
    'sunshine',
    'cloudy',
    'clouds',
    'storm',
    'tornado',
    'hurricane',
    'typhoon',
    'lightning',
    'typhoon',
    'monsoon',
    'sunny',
    'snowy',
    'sunny',
    'earthquake']

import MySQLdb
conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="Shine1234",
                  db="twitter",
                  charset="utf8")
x = conn.cursor()

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):

        json_data = json.loads(data)
        try:
            if json_data["coordinates"] == None:
                return True
        except:
            return True

        # for key, item in json_data.items():
        #      print key, item
        #print(data)


        #print json.dumps(json_data, sort_keys=True,indent=4, separators=(',', ': '))
        # for key, value in json_data.items():
        #     print key
        #
        #     if key == "user":
        #         print value
        #         for key, value in value.items():
        #             print '\t', key
        #
        #     elif key == 'coordinates':
        #         print value
        #         for key, value in value.items():
        #             print '\t', key

        coor_uuid = uuid.uuid4()
        # print json_data["coordinates"]["coordinates"][1]

        try:
            x.execute("""INSERT INTO Coordinates VALUES (%s,%s,%s)""",
                  (
                      coor_uuid,
                      json_data["coordinates"]["coordinates"][0],
                      json_data["coordinates"]["coordinates"][1]
                  )
            )

            conn.commit()
            print "Coordinate Success"
        except Exception as e:
            conn.rollback()
            print "Coordinate Error"
            print str(e)


        try:
            x.execute("""INSERT INTO Users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    json_data["user"]['id'],
                    json_data["user"]['created_at'],
                    json_data["user"]['description'],
                    json_data["user"]['favourites_count'],
                    json_data["user"]['followers_count'],
                    json_data["user"]['friends_count'],
                    json_data["user"]['geo_enabled'],
                    json_data["user"]['lang'],
                    json_data["user"]['listed_count'],
                    json_data["user"]['location'],
                    json_data["user"]['name'],
                    json_data["user"]['protected'],
                    json_data["user"]['screen_name'],
                    json_data["user"]['statuses_count'],
                    json_data["user"]['time_zone'],
                    json_data["user"]['url'],
                    json_data["user"]['verified']
                )
            )

            conn.commit()
            print "User Success"
        except Exception as e:
            conn.rollback()
            print "User Error"
            print str(e)


        try:
            x.execute("""INSERT INTO Tweet VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (
                    coor_uuid,
                    json_data['created_at'],
                    json_data['filter_level'],
                    json_data['id'],
                    json_data['in_reply_to_status_id'],
                    json_data['in_reply_to_user_id'],
                    json_data['lang'],
                    json_data['possibly_sensitive'],
                    json_data['retweet_count'],
                    json_data['retweeted'],
                    None,
                    json_data['source'],
                    json_data['text'].encode('utf8', 'ignore'),
                    json_data['truncated'],
                    json_data['user']['id'],
                    json_data['favorite_count'],
                    json_data['favorited'],
                    False

                )
            )

            conn.commit()
            print "Tweet Success"

        except Exception as e:
            print "Tweet Error"
            conn.rollback()
            print str(e)

        print '\n'
        # json_data["coordinates int,
        # json_data["created_at nvarchar(255),
        # json_data["filter_level nvarchar(255),
        # json_data["id int,
        # json_data["in_reply_to_status_id int,
        # json_data["in_reply_to_user_id int,
        # json_data["lang nvarchar(20),
        # json_data["possibly_sensitive bool,
        # json_data["retweet_count int,
        # json_data["retweeted bool,
        # json_data["retweeted_status int,
        # json_data["source nvarchar(2184),
        # json_data["text nvarchar(2184),
        # json_data["truncated bool,
        # json_data["user int,
        # json_data["favorite_count int,
        # json_data["favorited bool,
        # json_data["witheld_copyright bool,


            # try:
            #     x.execute("""INSERT INTO Coordinates VALUES (%s,%s)""",(188,90))
            #     conn.commit()
            # except:
            #     conn.rollback()














        # for key, value in json_data.items():
        #     print key + ": " + value
        #     # try:
        #     #     json.loads(value)
        #     #
        #     #     for sub_key, sub_value in value:
        #     #         print sub_value
        #     # except:
        #     #     pass



        #sys.exit()

        #print type(data)
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)



    #This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=keywords)









