


import hashlib
import redis
import logging
import traceback


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
        print("Welcome to url shortener !! please enter your email to proceed\n"); 
        self.user_id = input()
        print("\n Hi ", self.user_id,"\n")
        print("enter the url you like to shorten \n") 
        self.url = input()
        print("\n")
        md5 = hashlib.md5()
        md5.update(self.url.encode())
        to_add = md5.hexdigest()
        self.shortened_url = self.base_url + to_add 
        self.process_query()   

    def add_counter_url_to_user(self):
        self.redis_serv.hset(self.user_id, "userUrls",1)

    def incr_user_counter(self):
        self.redis_serv.hincrby(self.user_id, "userUrls", 1)
        
    def url_in_users_data(self): 
        return self.redis_serv.hexists(self.user_id, self.shortened_url)

    def url_in_data_base(self, url): 
        return self.redis_serv.exists(url)

    def incr_access_counter(self):
        self.redis_serv.incr("totalUrls",1)

    def incr_access_to_url(self):
        self.redis_serv.incr(self.shortened_url, 1)

    def add_user_to_db(self):
        if(not self.redis_serv.exists(self.user_id)) :
            self.redis_serv.hset(self.user_id, self.shortened_url, self.url)
            self.add_counter_url_to_user()
            print("Added ", self.user_id, "to users\n")
            print("Here is the url shortened ", self.shortened_url,"\n")
            if(not self.url_in_data_base(self.shortened_url)):
                self.redis_serv.set(self.shortened_url, 1)
                self.incr_access_counter()
            else : 
                self.incr_access_to_url()
            return True
        return False

    def process_query (self) :
        if(not self.add_user_to_db()):
            if(not self.url_in_data_base(self.shortened_url)):
                self.redis_serv.set(self.shortened_url, 1)
                self.incr_access_counter()
            else : 
                self.incr_access_to_url()
            if(self.url_in_users_data()):
                long_url = self.redis_serv.hget(self.user_id, self.shortened_url)
                print("the url has already been shortened here is the long version ",long_url) 
            else : 
                self.incr_user_counter()
                self.redis_serv.hset(self.user_id, self.shortened_url, self.url)
                print("Here is the url shortened ", self.shortened_url,"\n")

us = UrlShortener()