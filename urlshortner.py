


import hashlib
from pickle import FALSE
import redis
import logging
import traceback
import argparse
import re

#parse the arguments passed to the urlShortener
parser = argparse.ArgumentParser(description='URL shortener , your email must match this regex ^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}')

#argument to show the number of Urls stored and the number of Users
parser.add_argument('-s','--stats', action='store_true', help='show stats of the data base')
#argument to show the number of urls stored per user
parser.add_argument('-us','--userstats', action='store_true', help='show stats of the user')
#argument to show how much a shortened url was requested
parser.add_argument('-qs','--querystats', action='store_true', help='show the number of times an url was requested')
#argument to list all users present in the database
parser.add_argument('-lu','--listusers',action = 'store_true', help = 'list all users')


args = parser.parse_args()

#Class that implements the Url Shortener 
class UrlShortener(object) :
    redis_serv  = None #redis server to connect to
    base_url = 'https://urlshort.ly/' #base Url to use 
    user_id = None #user id in the form of an email 
    url = None #Url to be shortened
    shortened_url = None #url shortened


    def __init__(self) :
        #connecting to the server
        try:
            self.redis_serv = redis.Redis(host='localhost', port=6379)
        except Exception as e : 
            print("something went wrong see error below\n")
            logging.error(traceback.format_exc())      

        #creating fields to store stats 
        if (not self.redis_serv.exists("totalUrls")):
            self.redis_serv.set("totalUrls", 0)
       
        if (not self.redis_serv.exists("totalUsers")):
            self.redis_serv.set("totalUsers", 0)

        #getting the user information
        print("Welcome to url shortener !! please enter your email to proceed\n"); 
        self.user_id = self.validate_user_id()
        print("\n Hi ", self.user_id,"\n")
        print("enter the url you like to shorten \n") 
        self.url = input()
        print("\n")
        #computing a shortened version 
        md5 = hashlib.md5()
        md5.update(self.url.encode())
        to_add = md5.hexdigest()
        self.shortened_url = self.base_url + to_add 
        #process the query 
        self.process_query()   

    #list all users in the database
    def list_all_users(self):
        print("here are all the users of the database")
        for key in self.redis_serv.scan_iter("*@*"):
            # delete the key
            print(key.decode('utf-8'),"\n")


    #validate the user_id
    def validate_user_id(self):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        invalid = True
        email = ""
        while(invalid):
            email = input()
            if(re.search(regex, email)):
                invalid = False
                break
            print("\n invalid email pls insert valid email ex : toto@gmail.com \n")
        return email

    #check if the url is in short form 
    def check_not_shortened_url(self ):
        return self.base_url != self.url[:20]

    #fetch the db stats
    def show_db_stats(self):
        print("There are currently ",self.redis_serv.get('totalUrls').decode('utf-8')," Urls stored in the data base \n")
        print("There are currently ",self.redis_serv.get("totalUsers").decode('utf-8')," users in the data base \n")

    #fetch the user stats 
    def show_user_stats(self):
        print("User ",self.user_id, "has ", self.redis_serv.hget(self.user_id, "userUrls").decode('utf-8')," URLs stored \n")

    #fetch query stats  
    def show_query_stats(self):
        if(self.redis_serv.hexists(self.user_id, self.url)):
                print("this URL was accessed ", self.redis_serv.get(self.url).decode('utf-8')," times\n")            
        elif(self.redis_serv.hexists(self.user_id, self.shortened_url)):
                print("this URL was accessed ", self.redis_serv.get(self.shortened_url).decode('utf-8')," times\n")
                
    #add the shortened url to the database or increase its counter  
    def post_add_process(self):
        if(not self.redis_serv.exists(self.shortened_url)):
            self.redis_serv.set(self.shortened_url,1)
        else :
            self.redis_serv.incr(self.shortened_url,1)
    
    #adds user to db if he doesn't exist
    def add_user_to_db(self):
        if (not self.redis_serv.exists(self.user_id)):
            if(self.check_not_shortened_url()):  
                self.redis_serv.hset(self.user_id, self.shortened_url, self.url)
                self.redis_serv.incr("totalUsers", 1)
                self.redis_serv.hset(self.user_id, "userUrls",1)
                self.post_add_process()
                self.redis_serv.incr("totalUrls", 1)
                print("Added ", self.user_id, "to users\n")
                print("Here is the url shortened ", self.shortened_url,"\n")
                return True
            else: 
                print("An error occured you cannot give a short url to shorten")
                exit(0)
        return False

    #process the query
    def process_query (self) :
        #check if user exists
        if(not self.add_user_to_db()):
            #if the url was already shortened by the user we give the long url
            if(self.redis_serv.hexists(self.user_id, self.url)):
                print("URL was shortened here is the long URL ", self.redis_serv.hget(self.user_id, self.url))
                self.redis_serv.incr(self.url, 1)
            #if the url was shortened before we give a notification that it was
            elif(self.redis_serv.hexists(self.user_id, self.shortened_url)):
                print("Here is a short version of the URL note that this URL was shortened before ", self.shortened_url)
                self.post_add_process()
            #if the url was not shortened wee shorten is if it's not of shortened form
            elif (self.check_not_shortened_url()):
                self.redis_serv.hset(self.user_id, self.shortened_url, self.url)
                self.redis_serv.hincrby(self.user_id, "userUrls", 1)
                self.redis_serv.incr("totalUrls",1)
                self.post_add_process()
                print("Here is the url shortened ", self.shortened_url,"\n")
            #if the url is of shortened form we output an error 
            else :
                print("An error occured you cannot give a short url to shorten")
                exit(0)



#main function
if __name__ == '__main__' :
    us = UrlShortener()
    if (args.stats):
        us.show_db_stats()
    if (args.userstats):
        us.show_user_stats()
    if (args.querystats):
        us.show_query_stats()
    if(args.listusers):
        us.list_all_users()