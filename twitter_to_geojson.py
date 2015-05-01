__author__ = 'erkrenz'

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import geojson
import os
from pprint import pprint
import sys
import MySQLdb
import uuid
from datetime import datetime, tzinfo, timedelta
from dateutil import parser

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
                #print "no coordinates on", json_data["text"]
                return True
        except:
            #print "no coordinates on", json_data["text"]
            return True

        #Fetch coordinates from data
        coordinates = (json_data["coordinates"]["coordinates"][0], json_data["coordinates"]["coordinates"][1])

        #Fetch tweet text from data
        tweet_text = json_data["text"]

        #date created
        created_at = json_data["created_at"]

        #username
        user = json_data["user"]["screen_name"]
        date_object = parser.parse(created_at)#, '%a %b %d %X %Y')


        #Change our respective file to contain this value
        for keyword in keywords:
            if keyword in tweet_text:
                self.modify_file(keyword, coordinates, tweet_text, date_object, user)

        #Purge records older than 4 hours
        for keyword in keywords:
            self.purge_old_tweets(keyword)

        #print date_object
            
        return True

    def on_error(self, status):
        print status

    def purge_old_tweets(self, file_name):
        #Read in the current GeoJSON File
        file_path = 'json_data/' + str(file_name)

        json_file = None
        
        try:
            with open(file_path, 'r') as file:
    
                json_file = json.load(file)
    
                #print len(json_file["features"])
    
                #append to the existing featurecollection
                for feature in json_file["features"]:
                    time_then =  parser.parse(feature["properties"]["time"]).replace(tzinfo=None)
                    time_now =  datetime.utcnow()
                    time_delta = time_then - time_now
                    if time_delta > timedelta(hours=4):
                        print "old tweet purged from", file_name
                        json_file["features"].remove(feature)
                        
                #print len(json_file["features"])        
                    
                    
            with open(file_path, 'w') as file:
                
                geojson.dump(json_file, file)
                
        except Exception as e:
            print "Error on purge", e


    def modify_file(self, file_name, coordinates, tweet_text, date_object, user):


            
        file_path = 'json_data/' + str(file_name)
        json_file = None

        feature = geojson.Feature(geometry=geojson.Point(coordinates),
          properties={
              "tweet": tweet_text,
              "user": user,
              "time": str(date_object)
            }
          )


        #Read in the current GeoJSON File
        try:
            with open(file_path, 'r') as file:

                json_file = json.load(file)

                #append to the existing featurecollection
                json_file["features"].append(feature)

        #Create it, and a Feature Collection if it does not exist
        except (IOError):
            with open(file_path, 'w') as file:

                feature_collection = geojson.FeatureCollection([feature])

                json.dump(feature_collection, file)

                json_file = feature_collection

        #Print out the new GeoJSON File
        with open(file_path, 'w') as file:
            geojson.dump(json_file, file)



if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=keywords)









