


import hashlib
from pickle import FALSE
import redis
import logging
import traceback
import argparse
import re


parser = argparse.ArgumentParser(description='URL shortener , your email must match this regex ^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}')

parser.add_argument('-s','--stats', action='store_true', help='show stats of the data base')
parser.add_argument('-us','--userstats', action='store_true', help='show stats of the user')
parser.add_argument('-qs','--querystats', action='store_true', help='show the number of times an url was requested')


args = parser.parse_args()

class UrlShortener(object) :
    redis_serv  = None 
    base_url = 'https://urlshort.ly/'
    user_id = None 
    url = None
    shortened_url = None 


    def __init__(self) :
        try:
            self.redis_serv = redis.Redis(host='localhost', port=6379)
        except Exception as e : 
            print("something went wrong see error below\n")
            logging.error(traceback.format_exc())      

        if (not self.redis_serv.exists("totalUrls")):
            self.redis_serv.set("totalUrls", 0)
       
        if (not self.redis_serv.exists("totalUsers")):
            self.redis_serv.set("totalUsers", 0)

        print("Welcome to url shortener !! please enter your email to proceed\n"); 
        self.user_id = self.validate_user_id()
        print("\n Hi ", self.user_id,"\n")
        print("enter the url you like to shorten \n") 
        self.url = input()
        print("\n")
        md5 = hashlib.md5()
        md5.update(self.url.encode())
        to_add = md5.hexdigest()
        self.shortened_url = self.base_url + to_add 
        self.process_query()   

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

    def check_not_shortened_url(self ):
        return self.base_url != self.url[:20]

    def show_db_stats(self):
        print("There are currently ",self.redis_serv.get('totalUrls')," Urls stored in the data base \n")
        print("There are currently ",self.redis_serv.get("totalUsers")," users in the data base \n")

    def show_user_stats(self):
        print("User ",self.user_id, "has ", self.redis_serv.hget(self.user_id, "userUrls")," URLs stored \n")
 
    def show_query_stats(self):
        if(self.redis_serv.hexists(self.user_id, self.url)):
                print("this URL was accessed ", self.redis_serv.get(self.url)," times\n")            
        elif(self.redis_serv.hexists(self.user_id, self.shortened_url)):
                print("this URL was accessed ", self.redis_serv.get(self.shortened_url)," times\n")
                
        
    def post_add_process(self):
        if(not self.redis_serv.exists(self.shortened_url)):
            self.redis_serv.set(self.shortened_url,1)
        else :
            self.redis_serv.incr(self.shortened_url,1)
  
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




    def process_query (self) :
        #check if user exists
        if(not self.add_user_to_db()):
            if(self.redis_serv.hexists(self.user_id, self.url)):
                print("URL was shortened here is the long URL ", self.redis_serv.hget(self.user_id, self.url))
                self.redis_serv.incr(self.url, 1)
            elif(self.redis_serv.hexists(self.user_id, self.shortened_url)):
                print("Here is a short version of the URL note that this URL was shortened before ", self.shortened_url)
                self.post_add_process()
            elif (self.check_not_shortened_url()):
                self.redis_serv.hset(self.user_id, self.shortened_url, self.url)
                self.redis_serv.hincrby(self.user_id, "userUrls", 1)
                self.redis_serv.incr("totalUrls",1)
                self.post_add_process()
                print("Here is the url shortened ", self.shortened_url,"\n")
            else :
                print("An error occured you cannot give a short url to shorten")
                exit(0)




if __name__ == '__main__' :
    us = UrlShortener()
    if (args.stats):
        us.show_db_stats()
    if (args.userstats):
        us.show_user_stats()
    if (args.querystats):
        us.show_query_stats()