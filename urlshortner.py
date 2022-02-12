
from concurrent.futures import process
from genericpath import exists
import hashlib
from typing_extensions import Self
import redis
import logging
import traceback


redis_client = None
base_url = 'https://urlshort.ly/'

def url_exits(redis_client, user_id, shortened_url): 
    return redis_client.hexists(user_id,shortened_url)

def incr_stats(redis_client, shortened_url):
    redis_client.incr(shortened_url)

def add_shortened_url_to_user_data(redis_client, user_id, shortened_url, long_url): 
    redis_client.hset(user_id, shortened_url, long_url)

def add_shortened_url_to_db(redis_client, shortened_url) :
    if(not redis_client.exists(shortened_url)):
        redis_client.set(shortened_url, 1)
    


try:
    redis_client = redis.Redis(host='localhost', port=6379)
except Exception as e : 
    print("something went wrong see error below\n")
    logging.error(traceback.format_exc())

print("Welcome to url shortener !! please enter your email to proceed\n"); 
user_id = input()



print("Hi ", user_id,"\n")
print("enter the url you like to shorten \n") 
url = input()

md5 = hashlib.md5()
md5.update(url.encode())
to_add = md5.hexdigest()
shortened_url = base_url + to_add ; 

# if(not redis_client.exists(user_id)) : 
#     print("Added ", user_id, "to users\n")
#     add_shortened_url_to_user_data(redis_client, user_id, shortened_url, url)
#     add_shortened_url_to_db(redis_client, shortened_url)
#     print("Here is the url shortened ", shortened_url,"\n")
#     redis_client.hset(user_id, "total_url",1)
# elif(url_exits(redis_client, user_id, shortened_url)):
#     long_url = redis_client.hget(user_id, shortened_url)
#     incr_stats(redis_client, shortened_url)
#     print("the url has already been shortened here is the long version ",long_url)
# else: 
#     add_shortened_url_to_db(user_id, shortened_url)
#     add_shortened_url_to_user_data(redis_client, user_id, shortened_url, url)
#     print("Here is the url shortened ", shortened_url,"\n")

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
        print("Hi ", self.user_id,"\n")
        print("enter the url you like to shorten \n") 
        self.url = input()
        md5 = hashlib.md5()
        md5.update(url.encode())
        to_add = md5.hexdigest()
        self.shortened_url = self.base_url + to_add 
        self.process_query()   

    def add_user_to_db(self):
        if(not self.redis_serv.exists(self.user_id)) :
            self.redis_serv.hset(self.user_id, shortened_url, self.url)
            print("Added ", user_id, "to users\n")
            print("Here is the url shortened ", shortened_url,"\n")
            if(not self.url_in_data_base(shortened_url)):
                self.redis_serv.set(self.shortened_url, self.url)
            else : 
                self.incr_access_to_url(self)
            return True
        return False

    def url_in_users_data(self): 
        return self.redis_serv.hexists(self.user_id, self.shortened_url)

    def url_in_data_base(self, url): 
        return self.redis_serv.exists(url)

    def incr_access_counter(self):
        self.redis_serv.incr("totalUrls",1)

    def incr_access_to_url(self):
        self.redis_serv.incr(shortened_url, 1)

    def process_query (self) :
        if(not self.add_user_to_db(self)):
            if(not self.url_in_data_base(shortened_url)):
                self.redis_serv.set(self.shortened_url, self.url)
            else : 
                self.incr_access_to_url(self)
            if(self.url_in_users_data(self)):
                self.incr_access_to_url(self)
                long_url = self.redis_serv.hget(self.user_id, self.shortened_url)
                print("the url has already been shortened here is the long version ",long_url) 
            else : 
                self.redis_serv.hset(self.user_id, self.shortened_url, self.url)
                print("Here is the url shortened ", shortened_url,"\n")