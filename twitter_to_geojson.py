__author__ = 'erkrenz'

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import geojson
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
    'earthquake'
    ]


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):

        #Load the data into json format
        json_data = json.loads(data)

        #If the file does not contain coordinates, it is not relevant, skip and move on
        try:
            if json_data["coordinates"] == None:
                return True
        except:
            return True

        #Fetch coordinates from data
        coordinates = (json_data["coordinates"]["coordinates"][0], json_data["coordinates"]["coordinates"][1])

        #Fetch tweet text from data
        tweet_text = json_data["text"]

        #Change our respective file to contain this value
        for keyword in keywords:
            if keyword in tweet_text:
                self.modify_file(keyword, coordinates, tweet_text)

        print coordinates, tweet_text

        return True

    def on_error(self, status):
        print status

    def modify_file(self, file_name, coordinates, tweet_text):

        try:

            json_file = None

            #Read in the current GeoJSON File
            with open('/home/erkrenz/TwitterMap/' + str(file_name), 'r') as file:

                json_file = json.load(file)

                json_file["features"].append(geojson.Feature(geometry=geojson.Point(coordinates), properties={"tweet": tweet_text}))

                #print json_file

            #Print out the new GeoJSON File
            with open('/home/erkrenz/TwitterMap/' + str(file_name), 'w') as file:
                json.dump(json_file, file)

        except Exception as e:
            print "Error on file modification", str(e)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)



    #This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=keywords)









